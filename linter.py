import re
import sys
import os

def lint_dockerfile(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return

    with open(filepath, 'r') as f:
        lines = f.readlines()

    full_text = "".join(lines)
    issues = []
    
    # 1. Base Image Optimization
    if "FROM ubuntu" in lines[0] or "FROM python:latest" in lines[0]:
        issues.append("[SIZE] Using heavy base image (ubuntu/python:latest). Suggestion: Use python:3.10-slim.")

    # 2. GPU and CUDA validation
    if "nvidia" not in lines[0].lower() and ("torch" in full_text or "tensorflow" in full_text):
        issues.append("[GPU] AI libraries detected without NVIDIA base image. Suggestion: Use nvidia/cuda base.")

    # 3. Layer Caching Strategy
    copy_all_index = -1
    pip_install_index = -1
    for i, line in enumerate(lines):
        if re.search(r'COPY \. \.', line): copy_all_index = i
        if "pip install" in line: pip_install_index = i

    if copy_all_index != -1 and pip_install_index != -1 and copy_all_index < pip_install_index:
        issues.append("[CACHE] Global COPY before pip install. Suggestion: COPY requirements.txt first to cache dependencies.")

    # 4. Cleanup Logic
    if "apt-get install" in full_text and "rm -rf /var/lib/apt/lists/*" not in full_text:
        issues.append("[SIZE] apt-get install without cleanup. Suggestion: Add 'rm -rf /var/lib/apt/lists/*' in the same RUN command.")

    # 5. Dockerignore check
    if not os.path.exists(".dockerignore"):
        issues.append("[BUILD] Missing .dockerignore file. This may lead to large build contexts including local caches and git history.")

    # Results Output
    print(f"Linter Results for {filepath}:")
    if not issues:
        print("Success: No critical optimizations found.")
    else:
        for issue in issues:
            print(f"- {issue}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "Dockerfile"
    lint_dockerfile(target)
