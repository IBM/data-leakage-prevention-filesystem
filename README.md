# Data Leakage Prevention File System

[![Build Status](https://app.travis-ci.com/IBM/data-leakage-prevention-filesystem.svg?branch=main)](https://app.travis-ci.com/IBM/data-leakage-prevention-filesystem)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/IBM/data-leakage-prevention-filesystem.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/IBM/data-leakage-prevention-filesystem/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/IBM/data-leakage-prevention-filesystem.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/IBM/data-leakage-prevention-filesystem/context:python)
[![codecov](https://codecov.io/gh/IBM/data-leakage-prevention-filesystem/branch/main/graph/badge.svg)](https://codecov.io/gh/IBM/data-leakage-prevention-filesystem)

This project contains the code demonstrating an implementation of the techniques presented in [DLPFS: The Data Leakage Prevention FileSystem](https://arxiv.org/abs/2108.13785)

## Requirements

The execution of `DLPFS` requires the following dependencies to be available:
- re2, [https://github.com/google/re2](https://github.com/google/re2)
- FUSE [https://github.com/libfuse/libfuse](https://github.com/libfuse/libfuse)
