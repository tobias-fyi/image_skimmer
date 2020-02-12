"""Image Skimmer :: Package Initializer"""

import os
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# List of required dependencies
REQUIRED = ["clize", "opencv-python<=4.1.2.30"]

# This call to setup() does all the work
setup(
    name="image-skimmer",
    version="0.0.1",
    description="A tool for visually skimming large numbers of images quickly.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tobias-fyi/image_skimmer",
    author="Tobias Reaper",
    author_email="tobyreaper@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    py_modules=["image_skimmer"],
    install_requires=REQUIRED,
    entry_points="""
        [console_scripts]
        skim=image_skimmer.skimmer:cli
    """,
)
