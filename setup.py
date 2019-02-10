# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    desc = fh.read()
    long_description = desc[desc.find("# tt_demo"):]  # remove bagde

with open("tt_demo/requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="tt_demo",
    version="0.0.1",
    author="cle-b",
    author_email="cle@tictac.pm",
    description="My implementation of the Toucan Toco back test for technical interview.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cle-b/tt_demo",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License'
    ],
)
