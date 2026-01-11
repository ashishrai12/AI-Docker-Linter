# AI Docker Linter

A specialized tool for auditing and optimizing Dockerfiles in AI, Machine Learning, and Computer Vision projects. This linter focuses on performance, image size, and GPU compatibility.

## How to Use

To run the linter locally, ensure you have Python installed. Use the following command to scan your Dockerfile:

```bash
python linter.py --path ./Dockerfile
```

The tool will analyze your configuration and provide specific recommendations based on AI development best practices.

## Supported Rules

| Rule ID | Name | Description |
|---------|------|-------------|
| AID01 | GPU Base Image | Ensures an NVIDIA base image is used when PyTorch or TensorFlow is detected. |
| AID02 | Caching Strategy | Checks if bulk source code is copied after dependency installation to optimize layer caching. |
| AID03 | Size Optimization | Verifies that apt-get caches are cleared to minimize the final image size. |

## Integration

### GitHub Actions

You can integrate AI Docker Linter into your CI/CD pipeline using GitHub Actions. Add the following step to your workflow file:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run AI Docker Linter
        run: python linter.py --path ./Dockerfile
```

## Professional Standards

This tool follows industry standards for AI containerization:
- **Efficiency**: Prioritizes build cache hits.
- **Portability**: Ensures GPU libraries are properly supported.
- **Cleanliness**: Enforces image size reduction techniques.

For contributions or reporting issues, please open a GitHub Issue.
