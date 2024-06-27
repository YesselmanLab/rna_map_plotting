#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open("README.md", "r", encoding="UTF-8") as f:
    readme = f.read()

with open("requirements.txt", "r", encoding="UTF-8") as f:
    requirements = f.read().splitlines()

setup(
    name="rna_map_plotting",
    version="0.1.0",
    description="some common plotting to analyze DMS-MaPseq data",
    long_description=readme,
    long_description_content_type="test/markdown",
    author="Joe Yesselman",
    author_email="jyesselm@unl.edu",
    url="https://github.com/jyesselm/rna_map_plotting",
    packages=[
        "rna_map_plotting",
    ],
    package_dir={"rna_map_plotting": "rna_map_plotting"},
    py_modules=[
        "rna_map_plotting/logger",
        "rna_map_plotting/plotting",
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="rna_map_plotting",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": []},
)
