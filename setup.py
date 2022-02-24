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
    packages=find_packages(exclude=["contrib", "docs", "tests", "scripts", "build"]),
    python_requires=">=3.0",
    install_requires=[
        "diffprivlib==0.5.1",
        "fusepy==3.0.1",
        "joblib==1.1.0; python_version >= '3.6'",
        "numpy==1.22.2; python_version >= '3.8'",
        "pyre2==0.3.6",
        "scikit-learn==1.0.2; python_version >= '3.7'",
        "scipy==1.8.0; python_version < '3.11' and python_version >= '3.8'",
        "setuptools==60.9.3; python_version >= '3.7'",
        "threadpoolctl==3.1.0; python_version >= '3.6'",
    ],  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/IBM/data-leakage-prevention-file-system/issues",
        "Source": "https://github.com/IBM/data-leakage-prevention-file-system",
    },
)
