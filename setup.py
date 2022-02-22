"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dlpfs",  # Required
    version="0.1.0",  # Required
    description="An example of Data Leakage Prevention",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/IBM/data-leakage-prevention-file-system",  # Optional
    author="Stefano Braghin",  # Optional
    author_email="stefanob@ie.ibm.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.0",
    install_requires=[
        "fusepy",
        "diffprivlib"
    ],  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/IBM/data-leakage-prevention-file-system/issues",
        "Source": "https://github.com/IBM/data-leakage-prevention-file-system"
    },
)
