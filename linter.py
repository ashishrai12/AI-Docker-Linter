import re
import argparse
import os
import sys

# Dictionary-based rule system
RULES = {
    "AID01": {
        "name": "GPU Base Image Check",
        "message": "NVIDIA base image is recommended when PyTorch or TensorFlow is installed.",
        "level": "Warning"
    },
    "AID02": {
        "name": "Layer Caching Efficiency",
        "message": "Global 'COPY . .' detected before 'pip install'. Move COPY after dependency installation to improve cache hits.",
        "level": "Optimization"
    },
    "AID03": {
        "name": "Image Size Management",
        "message": "apt-get caches should be cleared to reduce image size (e.g., rm -rf /var/lib/apt/lists/*).",
        "level": "Size"
    }
}

class AIDockerLinter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self.full_text = ""
        self.issues = []

    def load_dockerfile(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Dockerfile not found at: {self.file_path}")
        
        with open(self.file_path, 'r') as f:
            self.lines = f.readlines()
            self.full_text = "".join(self.lines)

    def check_aid01(self):
        """Check for NVIDIA base image if PyTorch/TensorFlow is preset."""
        first_line = self.lines[0].lower() if self.lines else ""
        if "nvidia" not in first_line and ("torch" in self.full_text or "tensorflow" in self.full_text):
            self.issues.append("AID01")

    def check_aid02(self):
        """Check if COPY . . is after pip install."""
        copy_all_index = -1
        pip_install_index = -1
        
        for i, line in enumerate(self.lines):
            if re.search(r'COPY \. \.', line):
                copy_all_index = i
            if "pip install" in line:
                pip_install_index = i

        if copy_all_index != -1 and pip_install_index != -1 and copy_all_index < pip_install_index:
            self.issues.append("AID02")

    def check_aid03(self):
        """Check if apt-get caches are cleared."""
        if "apt-get install" in self.full_text:
            if "rm -rf /var/lib/apt/lists/*" not in self.full_text:
                self.issues.append("AID03")

    def run_all_checks(self):
        self.check_aid01()
        self.check_aid02()
        self.check_aid03()

    def report(self):
        print(f"Scanning Dockerfile: {self.file_path}")
        print("-" * 50)
        
        if not self.issues:
            print("No issues found. Your Dockerfile follows AI best practices.")
            return

        for rule_id in self.issues:
            rule = RULES[rule_id]
            print(f"[{rule_id}] {rule['level']}: {rule['name']}")
            print(f"      {rule['message']}\n")

def main():
    parser = argparse.ArgumentParser(description="AI Docker Linter: Optimize Dockerfiles for AI/ML workloads.")
    parser.add_argument("--path", type=str, default="Dockerfile", help="Path to the Dockerfile to lint.")
    
    args = parser.parse_args()

    linter = AIDockerLinter(args.path)
    try:
        linter.load_dockerfile()
        linter.run_all_checks()
        linter.report()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
