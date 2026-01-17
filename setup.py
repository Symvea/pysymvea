from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pysymvea",
    version="0.1.0",
    description="Python client for Symvea server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Symvea",
    url="https://github.com/Symvea/symvea-client",
    packages=find_packages(),
    python_requires=">=3.6",
    license="MIT",
    entry_points={
        "console_scripts": [
            "pysymvea=pysymvea.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)