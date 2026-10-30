"""Tests for integrity and scope of the read-only G02 hybrid preview."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import warnings
from zipfile import ZipFile

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "evaluation_calibration"))
from hybrid_review_preview import (
    DEFAULT_PACKET, REQUIRED, PacketError, build_preview, load_packet, verify,
)

PACKET = DEFAULT_PACKET

class PreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PACKET.exists():
            raise unittest.SkipTest('Frozen ignored G02 pilot packet is not available locally')
        cls.raw, cls.docs = load_packet(PACKET)

    def test_packet_traceability(self):
        checks = verify(self.raw, self.docs)
        self.assertEqual(checks['manifest_artifact_hashes_verified'], 8)
        self.assertEqual(checks['source_pointers_verified'], 203)
        self.assertEqual(checks['statements_verified'], 21)
        self.assertEqual(checks['units_verified'], 75)

    def test_no_semantic_scoring_or_approval(self):
        out = build_preview(PACKET)
        self.assertIsNone(out['accuracy_score'])
        self.assertIsNone(out['candidate_ranking'])
        self.assertEqual(len(out['claim_level_and_whole_statement_review']), 21)
        self.assertTrue(all(s['whole_statement_review']['verdict'] is None
                            for s in out['claim_level_and_whole_statement_review']))
        self.assertTrue(all(u['human_review_status']=='not_reviewed'
                            for s in out['claim_level_and_whole_statement_review']
                            for u in s['atomic_review']))

    def test_overlap_preserved_without_whole_statement_pass(self):
        out = build_preview(PACKET)
        target = next(s for s in out['claim_level_and_whole_statement_review']
                      if s['candidate_id']=='hosted' and s['json_pointer']=='/rationale/statement')
        by_id = {u['unit_id']:u for u in target['atomic_review']}
        self.assertEqual(by_id['H003']['proposed_input_support'], 'supported')
        self.assertEqual(by_id['H004']['proposed_input_support'], 'not_established')
        self.assertIn('P01_PROFILE_ATTRIBUTION', target['whole_statement_review']['candidate_issue_groups_for_review'])
        self.assertIsNone(target['whole_statement_review']['verdict'])

    def test_same_issue_multiple_occurrences_not_independent_penalties(self):
        out = build_preview(PACKET)
        grp = next(g for g in out['recurring_issue_groups_to_review']
                   if g['group_id']=='P01_PROFILE_ATTRIBUTION')
        self.assertEqual(grp['affected_statement_occurrences'], 2)
        self.assertEqual(grp['review_unit_ids'], ['H004','H034'])

    def test_changed_span_is_rejected(self):
        modified = copy.deepcopy(self.docs)
        modified['claim_annotations.draft.json']['units'][0]['location']['start'] = 100000
        with self.assertRaises(PacketError):
            verify(self.raw, modified)

    def test_fake_human_approval_is_rejected(self):
        modified = copy.deepcopy(self.docs)
        modified['claim_annotations.draft.json']['units'][0]['human_review_status'] = 'approved'
        with self.assertRaises(PacketError):
            verify(self.raw, modified)

    def test_modified_candidate_zip_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'packet.zip'
            with ZipFile(out,'w') as z:
                for name, blob in self.raw.items():
                    if name == 'hosted_candidate.json': blob += b'\n'
                    z.writestr(name, blob)
            with self.assertRaises(PacketError):
                build_preview(out)

    def test_source_value_mismatch_is_rejected(self):
        modified = copy.deepcopy(self.docs)
        u = next(u for u in modified['claim_annotations.draft.json']['units'] if u['unit_id']=='H004')
        u['context_input'][0]['observed_value'] = '100000.00'
        with self.assertRaises(PacketError):
            verify(self.raw, modified)

    def test_parsed_documents_cannot_diverge_from_frozen_bytes(self):
        modified=copy.deepcopy(self.docs)
        modified['source_inventory.draft.json']['recorded_observations'][0]['text']='Changed'
        with self.assertRaisesRegex(PacketError,'differs from supplied bytes'):
            verify(self.raw,modified)

    def test_self_consistent_fake_top_level_review_and_scores_are_rejected(self):
        for field,value in [('human_review_status','approved'),('scores',{'accuracy':1}),
                            ('performance_ranking',['hosted','baseline'])]:
            with self.subTest(field=field):
                docs=copy.deepcopy(self.docs)
                raw=dict(self.raw)
                docs['claim_annotations.draft.json'][field]=value
                raw['claim_annotations.draft.json']=json.dumps(docs['claim_annotations.draft.json']).encode()
                with self.assertRaisesRegex(PacketError,'cannot claim human review'):
                    verify(raw,docs)

    def test_fake_adjudicator_is_rejected_before_preview(self):
        docs=copy.deepcopy(self.docs)
        raw=dict(self.raw)
        docs['claim_annotations.draft.json']['disagreement_log']['adjudicator']='invented reviewer'
        raw['claim_annotations.draft.json']=json.dumps(docs['claim_annotations.draft.json']).encode()
        with self.assertRaisesRegex(PacketError,'fabricated adjudication'):
            verify(raw,docs)


class PacketLoadingTests(unittest.TestCase):
    """Portable adapter checks do not depend on ignored G02 artifacts."""

    def write_packet(self,path):
        raw={name:json.dumps({'file':name}).encode() for name in REQUIRED}
        path.mkdir()
        for name,blob in raw.items():
            (path/name).write_bytes(blob)
        return raw

    def test_directory_and_zip_return_identical_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet'
            raw=self.write_packet(path)
            archive=Path(directory)/'packet.zip'
            with ZipFile(archive,'w') as z:
                for name,blob in raw.items():
                    z.writestr(name,blob)
            self.assertEqual(load_packet(path),load_packet(archive))
            self.assertEqual(load_packet(path)[0],raw)

    def test_missing_directory_member_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet'
            self.write_packet(path)
            (path/'hosted_candidate.json').unlink()
            with self.assertRaises(PacketError):
                load_packet(path)

    def test_extra_directory_member_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet'
            self.write_packet(path)
            (path/'unexpected.json').write_text('{}',encoding='utf-8')
            with self.assertRaises(PacketError):
                load_packet(path)

    def test_directory_in_place_of_json_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet'
            self.write_packet(path)
            target=path/'hosted_candidate.json'
            target.unlink()
            target.mkdir()
            with self.assertRaises(PacketError):
                load_packet(path)

    def test_duplicate_zip_members_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet.zip'
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',UserWarning)
                with ZipFile(path,'w') as z:
                    z.writestr('hosted_candidate.json','{}')
                    z.writestr('hosted_candidate.json','{}')
            with self.assertRaisesRegex(PacketError,'duplicate entries'):
                load_packet(path)

    def test_malformed_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet'
            self.write_packet(path)
            (path/'hosted_candidate.json').write_bytes(b'{')
            with self.assertRaisesRegex(PacketError,'Invalid JSON'):
                load_packet(path)

if __name__=='__main__':
    unittest.main(verbosity=2)
