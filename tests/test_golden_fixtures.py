"""Reference-fixture consistency tests; not the full forthcoming Pydantic contract."""
import json
import unittest
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "data" / "golden_cases"


def read(path):
    return json.loads(path.read_text())


def validate_fixture(data):
    assert data['schema_version'] == '1.0'
    cust_id = data['customer']['customer_id']
    accs = [a['account_id'] for a in data['accounts']]
    tids = [t['transaction_id'] for t in data['transactions']]
    eids = [e['evidence_id'] for e in data['evidence']]
    ckids = [c['check_id'] for c in data['verification_checks']]
    for name, ids in [('account', accs), ('transaction', tids), ('evidence', eids), ('verification check', ckids)]:
        duplicate = [i for i, count in Counter(ids).items() if count > 1]
        if duplicate: raise ValueError(f'duplicate {name} ID: {duplicate}')
    assert data['case']['primary_alert_id'] == data['alert']['alert_id']
    assert data['alert']['customer_id'] == cust_id
    assert data['case']['policy_id'] == 'POLICY-AML-V1'
    cp_ids = {c['counterparty_id'] for c in data['counterparties']}
    for account in data['accounts']:
        assert account['customer_id'] == cust_id
    for t in data['transactions']:
        assert t['account_id'] in accs
        assert t['currency'] == 'USD'
        if t['counterparty_id'] is not None: assert t['counterparty_id'] in cp_ids
        try: amount = Decimal(t['amount'])
        except InvalidOperation: raise ValueError('invalid monetary string')
        assert amount.is_finite() and amount > 0
        timestamp = datetime.fromisoformat(t['occurred_at'].replace('Z', '+00:00'))
        assert timestamp.tzinfo is not None
    assert data['alert']['transaction_ids'] and set(data['alert']['transaction_ids']) <= set(tids)
    for e in data['evidence']:
        assert set(e['related_transaction_ids']) <= set(tids)
    for c in data['verification_checks']:
        assert set(c['subject_evidence_ids']) <= set(eids)
    # These input files must never carry the expected model answers.
    forbidden = {'expected_action', 'recommended_action', 'reference_rationale', 'rubric_version'}
    assert not (forbidden & set(data))


class TestGoldenFixtures(unittest.TestCase):
    def test_all_five_valid_inputs(self):
        for tag in ('G01','G02','G03','G04','G05'):
            with self.subTest(case=tag):
                validate_fixture(read(ROOT/'inputs'/f'{tag}.json'))

    def test_reference_identifiers_resolve(self):
        for tag in ('G01','G02','G03','G04','G05'):
            with self.subTest(case=tag):
                x = read(ROOT/'inputs'/f'{tag}.json')
                y = read(ROOT/'references'/f'{tag}_reference.json')
                self.assertEqual(x['case']['case_id'], y['case_id'])
                tids={t['transaction_id'] for t in x['transactions']}
                eids={e['evidence_id'] for e in x['evidence']}
                cids={c['check_id'] for c in x['verification_checks']}
                for finding in y['required_findings']:
                    self.assertTrue(set(finding['transaction_ids']) <= tids)
                    self.assertTrue(set(finding['evidence_ids']) <= eids)
                    self.assertTrue(set(finding['check_ids']) <= cids)

    def test_invalid_duplicate_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate transaction ID'):
            validate_fixture(read(ROOT/'inputs'/'G05_invalid_duplicate.json'))

    def test_financial_totals(self):
        expected={'G01':'34150.00','G04':'37300.00'}
        for tag, total in expected.items():
            x=read(ROOT/'inputs'/f'{tag}.json')
            deposits=sum((Decimal(t['amount']) for t in x['transactions'] if t['transaction_type']=='cash_deposit'),Decimal(0))
            self.assertEqual(deposits,Decimal(total))
        x=read(ROOT/'inputs'/'G03.json')
        outgoing=sum((Decimal(t['amount']) for t in x['transactions'] if t['direction']=='debit'),Decimal(0))
        self.assertEqual(outgoing,Decimal('35500.00'))

    def test_reference_labels_and_policy(self):
        labels={'G01':'close','G02':'investigate','G03':'escalate','G04':'investigate','G05':'investigate'}
        policy=read(REPO_ROOT/'specs'/'labeling_policy_v1.json')
        policy_ids={x['id'] for x in policy['referral_criteria']}
        for tag,expected in labels.items():
            y=read(ROOT/'references'/f'{tag}_reference.json')
            self.assertEqual(y['expected_action'], expected)
            self.assertTrue(y['human_review_required'])
            self.assertTrue(set(y['escalation_criteria_met']) <= policy_ids)
        self.assertEqual(read(ROOT/'references'/'G03_reference.json')['escalation_criteria_met'],['REF-01'])

if __name__ == '__main__':
    unittest.main()
