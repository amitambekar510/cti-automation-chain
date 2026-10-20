import unittest
from scripts.plan_environment import build
class TestPlan(unittest.TestCase):
 def test_plan(self):
  d={"siem":"ELK","intel_sources":["sample"],"goal":"brief","sector":"finance","region":"India","telemetry":["firewall"],"ai_runtime":"manual","approval":"required"}
  self.assertIn("R4 Response",build(d))
 def test_missing(self):
  with self.assertRaises(ValueError): build({"siem":"ELK"})
 def test_escape(self):
  d={"siem":"<bad>","intel_sources":[],"goal":"brief","sector":"finance","region":"India","telemetry":[],"ai_runtime":"manual","approval":"required"}
  self.assertNotIn("<bad>",build(d))
