from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dlpfs",
    version="0.1.0",
    description="An example of Data Leakage Prevention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IBM/data-leakage-prevention-file-system",
    author="Stefano Braghin",
    author_email="stefanob@ie.ibm.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests", "scripts", "build"]),
    python_requires=">=3.8",
    install_requires=[
        "diffprivlib==0.5.1",
        "fusepy==3.0.1",
        "pyre2==0.3.6"
    ],
    project_urls={
        "Bug Reports": "https://github.com/IBM/data-leakage-prevention-file-system/issues",
        "Source": "https://github.com/IBM/data-leakage-prevention-file-system",
    },
)
