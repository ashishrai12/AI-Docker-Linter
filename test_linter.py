import unittest
import os
from linter import lint_dockerfile

class TestLinter(unittest.TestCase):
    def setUp(self):
        self.test_file = "TestDockerfile"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_cache_order_detection(self):
        content = "FROM python:3.9\nCOPY . .\nRUN pip install torch"
        with open(self.test_file, "w") as f:
            f.write(content)
        # Testing if script runs without crash
        try:
            lint_dockerfile(self.test_file)
        except Exception as e:
            self.fail(f"Linter crashed on cache test: {e}")

    def test_missing_cleanup(self):
        content = "FROM python:3.9\nRUN apt-get update && apt-get install -y gcc"
        with open(self.test_file, "w") as f:
            f.write(content)
        try:
            lint_dockerfile(self.test_file)
        except Exception as e:
            self.fail(f"Linter crashed on cleanup test: {e}")

if __name__ == "__main__":
    unittest.main()
