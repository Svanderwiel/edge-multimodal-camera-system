#!/usr/bin/env python3
"""
Setup script for Multimodal AI Camera Assistant
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#") and not line.startswith("git+")
        ]
else:
    requirements = []

setup(
    name="multimodal-camera",
    version="0.1.0",
    author="Scott Van der Wiel",
    description="Real-time intelligent camera system combining YOLO object detection with cloud-based vision-language models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Svanderwiel/edge-multimodal-camera-system",
    project_urls={
        "Bug Reports": "https://github.com/Svanderwiel/edge-multimodal-camera-system/issues",
        "Source": "https://github.com/Svanderwiel/edge-multimodal-camera-system",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "multimodal-camera-demo=scripts.run_demo:main",
        ],
    },
    include_package_data=True,
    package_data={
        "multimodal_camera": ["py.typed"],
    },
    zip_safe=False,
)
