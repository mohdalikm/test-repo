#!/usr/bin/env python3
"""
Setup script for the Performance Issues package.

This setup.py is kept for backward compatibility. The main configuration
is now in pyproject.toml following modern Python packaging standards.
"""

from setuptools import setup, find_packages
import os
import sys

# Ensure we're using Python 3.9+
if sys.version_info < (3, 9):
    print("Python 3.9 or higher is required.")
    sys.exit(1)

# Read the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from a file."""
    requirements = []
    try:
        with open(os.path.join(here, filename), "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
    return requirements

# Core requirements
install_requires = [
    "pandas>=1.5.0",
    "numpy>=1.24.0", 
    "requests>=2.28.0",
    "click>=8.0.0",
]

# Development requirements
dev_requires = [
    "pytest>=7.0.0",
    "pytest-benchmark>=4.0.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

# Visualization requirements
viz_requires = [
    "matplotlib>=3.6.0",
    "seaborn>=0.12.0",
    "plotly>=5.0.0",
]

# Profiling requirements  
profiling_requires = [
    "memory-profiler>=0.60.0",
    "line-profiler>=4.0.0",
    "py-spy>=0.3.0",
]

# Database requirements
db_requires = [
    "sqlalchemy>=1.4.0",
]

setup(
    name="performance-issues",
    use_scm_version={
        "write_to": "src/performance_issues/_version.py",
    },
    author="Performance Issues Demo",
    author_email="demo@example.com",
    description="Python application with intentional performance issues for AI analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/performance-issues",
    project_urls={
        "Bug Tracker": "https://github.com/example/performance-issues/issues",
        "Documentation": "https://performance-issues.readthedocs.io",
        "Source": "https://github.com/example/performance-issues",
    },
    
    # Package configuration
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Include additional files
    include_package_data=True,
    package_data={
        "performance_issues": [
            "config/*.json",
            "data/*.csv", 
            "data/*.json",
        ],
    },
    
    # Requirements
    python_requires=">=3.9",
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "viz": viz_requires,
        "profiling": profiling_requires,
        "db": db_requires,
        "all": dev_requires + viz_requires + profiling_requires + db_requires,
    },
    
    # Entry points
    entry_points={
        "console_scripts": [
            "performance-issues=performance_issues.cli:main",
            "perf-test=performance_issues.cli:run_performance_test",
            "perf-analyze=performance_issues.cli:analyze_performance",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers", 
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10", 
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Benchmark",
        "Topic :: Education",
    ],
    
    # Keywords
    keywords="performance optimization ai analysis benchmarking",
    
    # Setup requirements
    setup_requires=[
        "setuptools>=45",
        "wheel",
        "setuptools_scm>=6.2",
    ],
    
    # Zip safety
    zip_safe=False,
)