from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = [req.strip() for req in f.read().split() if len(req) and not req.strip().startswith("#")]


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
    install_requires=requirements,
    project_urls={
        "Bug Reports": "https://github.com/IBM/data-leakage-prevention-file-system/issues",
        "Source": "https://github.com/IBM/data-leakage-prevention-file-system",
    },
)
