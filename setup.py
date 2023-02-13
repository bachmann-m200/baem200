import setuptools
import sys
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baem200",
    version="0.0.13",
    author="Sven Neumann",
    author_email="sven.neumann@bachmann.info",
    description="Bachmann electronic Python Util Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bachmann-m200/baem200",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
