# AI-Docker-Linter

A lightweight, specialized linter designed to audit and optimize Dockerfiles for **Machine Learning and Computer Vision** projects.

## Why this exists?
Standard linters check for syntax. **AI-Docker-Linter** checks for **performance**. 

AI containers are notoriously heavy (often 5GB+ due to PyTorch/TensorFlow). Poorly structured Dockerfiles lead to:
* **Wasted Storage:** Massive image layers that could be slimmed down.
* **Broken Workflows:** Missing NVIDIA drivers or CUDA toolkit references.
* **Inefficient Caching:** Re-downloading heavy AI libraries every time you change a single line of Python code.

## Key Features
* **Layer-Cache Analysis:** Detects if you are copying source code before installing dependencies.
* **GPU Awareness:** Scans for AI libraries and ensures you're using a compatible `nvidia/cuda` base.
* **Size Optimization:** Recommends `-slim` variants and automated `apt-get` cleanup.
* **Zero-Install Mode:** Run it directly via Docker so you don't mess up your host environment.

## Usage

### Quick Start (using Docker)
The most "meta" way to use a Docker linter is via Docker itself:
```bash
docker run --rm -v $(pwd)/Dockerfile:/app/Dockerfile ashishrai12/ai-docker-linter
