import unittest

from diagnose_e1_failures import check_buffered_metadata, check_evaluation_clock
from run_e1 import dependency_status


class InfrastructureReproductionTests(unittest.TestCase):
    def test_buffered_reply_failure_and_byte_buffer_control(self):
        result = check_buffered_metadata()
        self.assertEqual(result["legacy"]["outcome"], "TimeoutError")
        self.assertIn("without another fd poll", result["explicit_byte_buffer_control"])

    @unittest.skipUnless(dependency_status()["installed"], "Pinned optional Shinka dependency required")
    def test_proposal_clock_failure_and_true_evaluation_clock_controls(self):
        result = check_evaluation_clock()
        self.assertEqual(result["evaluation_clock_0s_control"], "Kept running")
        self.assertEqual(result["evaluation_clock_61s_control"], "Killed at real evaluation limit")
