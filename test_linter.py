import unittest
import os
from linter import AIDockerLinter

class TestLinter(unittest.TestCase):
    def setUp(self):
        self.test_file = "TestDockerfile"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def run_linter(self, content):
        with open(self.test_file, "w") as f:
            f.write(content)
        linter = AIDockerLinter(self.test_file)
        linter.load_dockerfile()
        linter.run_all_checks()
        return linter.issues

    def test_cache_order_detection(self):
        content = "FROM python:3.9\nCOPY . .\nRUN pip install torch"
        issues = self.run_linter(content)
        self.assertIn("AID02", issues)

    def test_missing_cleanup(self):
        content = "FROM python:3.9\nRUN apt-get update && apt-get install -y gcc"
        issues = self.run_linter(content)
        self.assertIn("AID03", issues)

    def test_gpu_base_image_detection(self):
        content = "FROM python:3.9\nRUN pip install torch"
        issues = self.run_linter(content)
        self.assertIn("AID01", issues)

    def test_good_dockerfile(self):
        content = "FROM nvidia/cuda:11.0-base\nRUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*\nCOPY requirements.txt .\nRUN pip install torch\nCOPY . ."
        issues = self.run_linter(content)
        self.assertEqual(len(issues), 0)

if __name__ == "__main__":
    unittest.main()
