"""Development generator regression tests; no adjudicated AML labels are assigned."""

from collections import Counter
from datetime import datetime
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from aml_triage.contracts import InvestigationInput
from aml_triage.synthetic_generator import (
    DevelopmentBatch,
    FAMILIES,
    GENERATOR_VERSION,
    TEMPLATE_VERSION,
    generate_development_batch,
    write_development_batch,
)


ROOT = Path(__file__).resolve().parents[1]
SEED = 20261027


class TestSyntheticGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = generate_development_batch(seed=SEED, count=50)
        cls.manifest = json.loads(cls.batch.manifest)
        cls.cases = [json.loads(payload) for payload in cls.batch.investigations.values()]

    def test_exactly_fifty_cases_validate_through_existing_json_contract(self):
        self.assertEqual(len(self.batch.investigations), 50)
        for filename, payload in self.batch.investigations.items():
            with self.subTest(filename=filename):
                record = InvestigationInput.model_validate_json(payload)
                self.assertEqual(filename, f"{record.case.case_id}.json")

    def test_same_seed_and_configuration_give_identical_bytes_and_digests(self):
        repeated = generate_development_batch(seed=SEED, count=50)
        self.assertEqual(repeated, self.batch)
        self.assertEqual(sha256(repeated.manifest).hexdigest(),
                         sha256(self.batch.manifest).hexdigest())

    def test_global_random_state_neither_affects_nor_is_changed_by_generation(self):
        original = random.getstate()
        try:
            random.seed(8675309)
            state = random.getstate()
            self.assertEqual(generate_development_batch(seed=SEED), self.batch)
            self.assertEqual(random.getstate(), state)
        finally:
            random.setstate(original)

    def test_different_seed_changes_source_conditions_and_not_only_ids(self):
        different = generate_development_batch(seed=SEED + 1)
        other = json.loads(different.manifest)
        self.assertNotEqual([entry["source_condition"] for entry in self.manifest["cases"]],
                            [entry["source_condition"] for entry in other["cases"]])
        self.assertNotEqual([record["transactions"][0]["occurred_at"] for record in self.cases],
                            [json.loads(raw)["transactions"][0]["occurred_at"]
                             for raw in different.investigations.values()])

    def test_record_identifiers_are_unique_across_entire_batch(self):
        seen = set()
        for case in self.cases:
            identifiers = [case["case"]["case_id"], case["alert"]["alert_id"],
                           case["customer"]["customer_id"]]
            for collection, key in (
                ("accounts", "account_id"), ("counterparties", "counterparty_id"),
                ("transactions", "transaction_id"), ("evidence", "evidence_id"),
                ("verification_checks", "check_id"),
            ):
                identifiers.extend(record[key] for record in case[collection])
            for identifier in identifiers:
                self.assertNotIn(identifier, seen)
                seen.add(identifier)

    def test_chronology_and_timezones_are_coherent(self):
        for case in self.cases:
            model = InvestigationInput.model_validate(case)
            timestamps = [transaction.occurred_at for transaction in model.transactions]
            self.assertEqual(timestamps, sorted(timestamps))
            self.assertLess(max(timestamps), model.alert.created_at)
            self.assertLess(model.alert.created_at, model.case.opened_at)
            self.assertLessEqual(model.customer.onboarding_date,
                                 model.customer.profile_last_verified)
            self.assertLessEqual(model.customer.profile_last_verified, min(timestamps).date())
            for stamp in timestamps + [model.alert.created_at, model.case.opened_at]:
                self.assertIsNotNone(stamp.utcoffset())
            for account in model.accounts:
                self.assertLessEqual(account.opened_at, min(timestamps).date())
            for evidence in model.evidence:
                if evidence.evidence_type == "information_request":
                    requested = datetime.fromisoformat(evidence.facts["requested_at"])
                    self.assertLess(max(timestamps), requested)
                    self.assertLess(requested, model.case.opened_at)

    def test_all_explicit_record_references_resolve(self):
        for case in self.cases:
            transactions = {record["transaction_id"] for record in case["transactions"]}
            accounts = {record["account_id"] for record in case["accounts"]}
            parties = {record["counterparty_id"] for record in case["counterparties"]}
            evidence = {record["evidence_id"] for record in case["evidence"]}
            self.assertEqual(case["case"]["primary_alert_id"], case["alert"]["alert_id"])
            self.assertEqual(case["customer"]["customer_id"], case["alert"]["customer_id"])
            self.assertTrue(set(case["alert"]["transaction_ids"]) <= transactions)
            for record in case["transactions"]:
                self.assertIn(record["account_id"], accounts)
                if record["counterparty_id"] is not None:
                    self.assertIn(record["counterparty_id"], parties)
            for record in case["evidence"]:
                self.assertTrue(set(record["related_transaction_ids"]) <= transactions)
            for record in case["verification_checks"]:
                self.assertTrue(set(record["subject_evidence_ids"]) <= evidence)

    def test_all_five_families_have_ten_development_cases(self):
        counts = Counter(entry["scenario_family_id"] for entry in self.manifest["cases"])
        self.assertEqual(counts, dict.fromkeys(FAMILIES, 10))
        self.assertEqual(self.manifest["scenario_family_counts"], counts)

    def test_each_family_varies_material_source_conditions(self):
        for family in FAMILIES:
            conditions = {entry["source_condition"] for entry in self.manifest["cases"]
                          if entry["scenario_family_id"] == family}
            self.assertGreaterEqual(len(conditions), 3, family)
        by_family = {family: [] for family in FAMILIES}
        for entry in self.manifest["cases"]:
            by_family[entry["scenario_family_id"]].append(
                json.loads(self.batch.investigations[entry["input_path"]])
            )
        inventory = [{item["evidence_type"] for item in case["evidence"]}
                     for case in by_family["incoming_transfer"]]
        self.assertTrue(any("dispatch_record" in types for types in inventory))
        self.assertTrue(any("supplier_invoice" not in types for types in inventory))
        unmatched = [
            item["facts"]["unmatched_amount"] for case in by_family["cash_sales"]
            for item in case["evidence"] if item["evidence_type"] == "deposit_reconciliation"
        ]
        self.assertIn("0.00", unmatched)
        self.assertTrue(any(Decimal(amount) > 0 for amount in unmatched))
        comparisons = []
        for case in by_family["beneficiary_comparison"]:
            invoice, wire = case["evidence"][1:]
            left = invoice["facts"]["beneficiary_account_ref"]
            right = wire["facts"]["beneficiary_account_ref"]
            comparisons.append(None if left is None else left == right)
        self.assertEqual(set(comparisons), {True, False, None})

    def test_supplier_timing_accounts_and_authorized_changes_match_modes(self):
        for entry in self.manifest["cases"]:
            if entry["scenario_family_id"] != "supplier_authorization":
                continue
            case = json.loads(self.batch.investigations[entry["input_path"]])
            register, instruction, ledger = case["evidence"][1:4]
            notice = datetime.fromisoformat(instruction["facts"]["issued_at"])
            payments = ledger["facts"]["payments"]
            after = [datetime.fromisoformat(record["occurred_at"]) > notice for record in payments]
            mode = entry["source_condition"]
            self.assertEqual(after, [False, False] if mode == "before_instruction" else
                             [False, True] if mode == "split_timing" else [True, True])
            self.assertEqual(register["facts"]["authorized_change_recorded"],
                             mode == "authorized_change")
            self.assertEqual(payments[0]["payee_account_ref"] == payments[1]["payee_account_ref"],
                             mode != "different_accounts_same_supplier")
            if mode == "authorized_change":
                effective = datetime.fromisoformat(register["facts"]["change_effective_at"])
                self.assertLess(effective, min(datetime.fromisoformat(item["occurred_at"])
                                               for item in payments))

    def test_cash_amounts_reconcile_to_supplied_coverage_not_invented_sales(self):
        for case in self.cases:
            reconciliation = next((item for item in case["evidence"]
                                   if item["evidence_type"] == "deposit_reconciliation"), None)
            if reconciliation is None:
                continue
            facts = reconciliation["facts"]
            profile = case["evidence"][0]["facts"]
            self.assertTrue(profile["seasonal_activity_reported"])
            for record in case["transactions"]:
                deposit_day = datetime.fromisoformat(record["occurred_at"]).strftime("%A")
                self.assertIn(deposit_day, profile["operating_days"])
            deposits = sum((Decimal(record["amount"]) for record in case["transactions"]),
                           Decimal(0))
            self.assertEqual(Decimal(facts["deposit_total"]), deposits)
            accounted = Decimal(facts["reconciled_deposits"]) + Decimal(facts["unmatched_amount"])
            self.assertEqual(accounted, deposits)

    def test_manifest_is_separate_and_records_exact_hashes_versions_and_lineage(self):
        self.assertEqual(self.manifest["dataset_partition"], "development")
        self.assertEqual(self.manifest["seed"], SEED)
        self.assertEqual(self.manifest["generator_version"], GENERATOR_VERSION)
        self.assertFalse(self.manifest["lineage"]["independently_authored_cases"])
        self.assertTrue(self.manifest["lineage"]["shared_generator_templates"])
        self.assertFalse(self.manifest["lineage"]["reference_answers_used"])
        self.assertEqual(len(self.manifest["lineage"]["templates"]), 5)
        for entry in self.manifest["cases"]:
            self.assertEqual(entry["template_version"], TEMPLATE_VERSION)
            self.assertTrue(entry["case_family_id"].startswith("development-"))
            self.assertEqual(entry["input_sha256"],
                             sha256(self.batch.investigations[entry["input_path"]]).hexdigest())
            self.assertEqual(Path(entry["input_path"]).name, entry["input_path"])

    def test_inputs_have_no_expected_answers_annotations_or_verdict_statuses(self):
        forbidden = {
            "expected_action", "recommended_action", "reference_rationale", "rubric_version",
            "reference_answer", "reference_answers", "evaluation_annotations", "manifest",
            "source_condition", "scenario_family_id", "model_output",
        }
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden & value.keys())
                for nested in value.values():
                    inspect(nested)
            elif isinstance(value, list):
                for nested in value:
                    inspect(nested)
        for case in self.cases:
            inspect(case)
            self.assertEqual({record["status"] for record in case["verification_checks"]},
                             {"recorded"})
            self.assertEqual({record["verification_status"] for record in case["evidence"]},
                             {"recorded"})

    def test_incomplete_nullable_contextual_and_heterogeneous_records_are_preserved(self):
        self.assertTrue(any(not case["counterparties"] for case in self.cases))
        self.assertTrue(any(record["counterparty_id"] is None for case in self.cases
                            for record in case["transactions"]))
        self.assertTrue(any(record["facts"].get("beneficiary_account_ref", "absent") is None
                            for case in self.cases for record in case["evidence"]))
        for case in self.cases:
            context = case["evidence"][0]
            self.assertEqual(context["related_transaction_ids"], [])
            self.assertIsInstance(context["facts"]["operating_days"], list)
            self.assertIsInstance(context["facts"]["staff_count"], int)
            self.assertIsInstance(context["facts"]["seasonal_activity_reported"], bool)
            self.assertIsNone(context["facts"]["premises"]["visit_record"])

    def test_money_is_positive_two_decimal_string_without_float_arithmetic(self):
        for case in self.cases:
            for record in case["transactions"]:
                self.assertRegex(record["amount"], r"^[0-9]+\.[0-9]{2}$")
                self.assertGreater(Decimal(record["amount"]), 0)

    def test_configurable_counts_and_negative_seed_remain_reproducible(self):
        for count in (1, 4, 7, 51):
            with self.subTest(count=count):
                batch = generate_development_batch(seed=-17, count=count)
                self.assertEqual(len(batch.investigations), count)
                self.assertEqual(json.loads(batch.manifest)["case_count"], count)
                self.assertEqual(batch, generate_development_batch(seed=-17, count=count))

    def test_invalid_counts_and_seeds_are_rejected(self):
        for count in (0, -1, True, 1.5, "50", None):
            with self.subTest(count=count), self.assertRaises(ValueError):
                generate_development_batch(seed=SEED, count=count)
        for seed in (True, 1.5, "seed", None):
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                generate_development_batch(seed=seed)

    def test_generation_has_no_file_network_policy_reference_or_model_access(self):
        import socket
        with patch("builtins.open", side_effect=AssertionError("Unexpected read")), patch.object(
            Path, "open", side_effect=AssertionError("Unexpected file access")
        ), patch.object(socket, "socket", side_effect=AssertionError("Unexpected network")):
            self.assertEqual(generate_development_batch(seed=SEED), self.batch)

    def test_existing_golden_artifacts_are_not_mutated(self):
        paths = list((ROOT / "data" / "golden_cases").rglob("*.json"))
        before = {path: path.read_bytes() for path in paths}
        generate_development_batch(seed=SEED)
        self.assertEqual({path: path.read_bytes() for path in paths}, before)

    def test_batch_values_are_independent_between_calls(self):
        changed = generate_development_batch(seed=SEED)
        changed.investigations.clear()
        self.assertEqual(generate_development_batch(seed=SEED), self.batch)


class TestDevelopmentPublication(unittest.TestCase):
    def test_published_bytes_are_identical_across_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp) / "first", Path(temp) / "nested" / "second"
            result = write_development_batch(first, seed=SEED)
            self.assertEqual(write_development_batch(second, seed=SEED), result)
            left = {path.name: path.read_bytes() for path in first.iterdir()}
            right = {path.name: path.read_bytes() for path in second.iterdir()}
            self.assertEqual(left, right)
            self.assertEqual(len(left), 51)
            for entry in result["cases"]:
                self.assertEqual(sha256(left[entry["input_path"]]).hexdigest(),
                                 entry["input_sha256"])
            self.assertEqual(sorted(path.name for path in first.parent.iterdir()),
                             ["first", "nested"])

    def test_existing_empty_nonempty_and_file_destinations_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            empty, populated, file = (Path(temp) / name for name in ("empty", "populated", "file"))
            empty.mkdir()
            populated.mkdir()
            sentinel = populated / "keep.txt"
            sentinel.write_bytes(b"unchanged")
            file.write_bytes(b"unchanged-file")
            for target in (empty, populated, file):
                with self.subTest(target=target), self.assertRaises(FileExistsError):
                    write_development_batch(target, seed=SEED)
            self.assertEqual(list(empty.iterdir()), [])
            self.assertEqual(sentinel.read_bytes(), b"unchanged")
            self.assertEqual(file.read_bytes(), b"unchanged-file")

    def test_invalid_locations_and_counts_publish_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            file = parent / "file"
            file.write_bytes(b"keep")
            for target in (file / "child", parent / "bad\x00name"):
                with self.subTest(target=target), self.assertRaises((OSError, ValueError)):
                    write_development_batch(target, seed=SEED, count=1)
            target = parent / "invalid-count"
            with self.assertRaises(ValueError):
                write_development_batch(target, seed=SEED, count=0)
            self.assertFalse(target.exists())
            self.assertEqual(list(parent.iterdir()), [file])

    def test_validation_failure_prevents_publishing_or_creating_parent(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "new-parent" / "dataset"
            batch = DevelopmentBatch({"invalid.json": b"{}"}, json.dumps({"cases": [{
                "case_id": "invalid", "input_path": "invalid.json", "input_sha256": "wrong",
            }]}).encode())
            with patch("aml_triage.synthetic_generator.generate_development_batch",
                       return_value=batch):
                with self.assertRaises(ValidationError):
                    write_development_batch(target, seed=SEED, count=1)
            self.assertFalse(target.parent.exists())

    def test_manifest_digest_failure_prevents_publication(self):
        batch = generate_development_batch(seed=SEED, count=1)
        manifest = json.loads(batch.manifest)
        manifest["cases"][0]["input_sha256"] = "0" * 64
        damaged = DevelopmentBatch(batch.investigations, json.dumps(manifest).encode())
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            with patch("aml_triage.synthetic_generator.generate_development_batch",
                       return_value=damaged):
                with self.assertRaisesRegex(ValueError, "digest mismatch"):
                    write_development_batch(target, seed=SEED, count=1)
            self.assertFalse(target.exists())

    def test_write_failure_cleans_staging_and_leaves_no_published_dataset(self):
        original = Path.write_bytes
        written = []
        def fail_second(path, payload):
            written.append(path)
            if len(written) == 2:
                raise OSError("Simulated disk failure")
            return original(path, payload)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            with patch.object(Path, "write_bytes", new=fail_second):
                with self.assertRaisesRegex(OSError, "Simulated disk failure"):
                    write_development_batch(target, seed=SEED, count=3)
            self.assertFalse(target.exists())
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_duplicate_manifest_entries_cannot_leave_published_inputs_unvalidated(self):
        batch = generate_development_batch(seed=SEED, count=2)
        manifest = json.loads(batch.manifest)
        manifest["cases"][1] = manifest["cases"][0]
        damaged = DevelopmentBatch(batch.investigations, json.dumps(manifest).encode())
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            with patch("aml_triage.synthetic_generator.generate_development_batch",
                       return_value=damaged):
                with self.assertRaisesRegex(ValueError, "count"):
                    write_development_batch(target, seed=SEED, count=2)
            self.assertFalse(target.exists())

    def test_corrupted_staged_bytes_are_not_published(self):
        original = Path.write_bytes
        def truncate(path, payload):
            return original(path, payload[:-1])
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            with patch.object(Path, "write_bytes", new=truncate):
                with self.assertRaisesRegex(OSError, "Staged artifact bytes"):
                    write_development_batch(target, seed=SEED, count=1)
            self.assertFalse(target.exists())
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_existing_publication_lock_is_not_removed(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            lock = Path(temp) / ".dataset.generation.lock"
            lock.write_bytes(b"other-owner")
            with self.assertRaises(FileExistsError):
                write_development_batch(target, seed=SEED, count=1)
            self.assertEqual(lock.read_bytes(), b"other-owner")
            self.assertFalse(target.exists())

    def test_destination_created_during_staging_is_preserved(self):
        original = Path.write_bytes
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            def create_destination(path, payload):
                target.mkdir(exist_ok=True)
                return original(path, payload)
            with patch.object(Path, "write_bytes", new=create_destination):
                with self.assertRaises(FileExistsError):
                    write_development_batch(target, seed=SEED, count=1)
            self.assertEqual(list(target.iterdir()), [])

    def test_cli_generates_parseable_summary_and_refuses_a_second_publication(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            command = [sys.executable, str(ROOT / "scripts" / "generate_dev_cases.py"),
                       "--seed", str(SEED), "--count", "50", "--output-dir", str(target)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary["case_count"], 50)
            self.assertEqual(summary["manifest_sha256"],
                             sha256((target / "manifest.json").read_bytes()).hexdigest())
            before = {path.name: path.read_bytes() for path in target.iterdir()}
            refused = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(refused.returncode, 2)
            self.assertEqual(refused.stdout, "")
            self.assertIn("already exists", refused.stderr)
            self.assertEqual({path.name: path.read_bytes() for path in target.iterdir()}, before)

    def test_cli_invalid_count_returns_usage_error_without_publication(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "dataset"
            command = [sys.executable, str(ROOT / "scripts" / "generate_dev_cases.py"),
                       "--seed", str(SEED), "--count", "0", "--output-dir", str(target)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("positive integer", result.stderr)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
