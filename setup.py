"""
Setup script for the Superintelligence Multi-Modal Agentic AI Framework.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="superintelligence-multimodal-agents",
    version="0.1.0",
    author="Superintelligence AI Research Team",
    author_email="contact@superintelligence-ai.org",
    description="A comprehensive framework for developing superintelligent AI systems through multi-modal agentic architectures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/superintelligence-multimodal-agents",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "isort>=5.12.0",
            "mypy>=1.6.0",
            "flake8>=6.1.0",
            "pre-commit>=3.5.0",
        ],
        "gpu": [
            "flash-attn>=2.3.0",
            "bitsandbytes>=0.41.0",
        ],
        "all": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0", 
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "isort>=5.12.0",
            "mypy>=1.6.0",
            "flake8>=6.1.0",
            "pre-commit>=3.5.0",
            "flash-attn>=2.3.0",
            "bitsandbytes>=0.41.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "superintelligence-cli=superintelligence.cli:main",
            "superintelligence-server=superintelligence.deployment.api_server:main",
            "superintelligence-train=superintelligence.training.train:main",
        ],
    },
    include_package_data=True,
    package_data={
        "superintelligence": [
            "configs/*.yaml",
            "benchmarks/*.json",
            "examples/*.py",
        ],
    },
    zip_safe=False,
    keywords=[
        "artificial intelligence",
        "superintelligence", 
        "multi-modal",
        "agentic ai",
        "constitutional ai",
        "machine learning",
        "deep learning",
        "transformers",
        "vision language models",
        "autonomous agents",
        "ai safety",
        "ai alignment"
    ],
    project_urls={
        "Bug Reports": "https://github.com/your-username/superintelligence-multimodal-agents/issues",
        "Source": "https://github.com/your-username/superintelligence-multimodal-agents",
        "Documentation": "https://superintelligence-ai.readthedocs.io/",
        "Research Papers": "https://github.com/your-username/superintelligence-multimodal-agents/blob/main/docs/research_papers.md",
    },
)