# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-10-20
LastEditors:Do not edit
LastEditTime:2021-03-16
Description:
"""
from setuptools import setup, find_packages
import os
import sys

if os.path.dirname(os.path.realpath(__file__)) not in sys.path:
    path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, path)
from pyChakraCore import __version__

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """==========================
Unsupported Python version
==========================
This version of pyChakraCore requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install pyChakraCore
This will install the latest version of pyChakraCore which works on your
version of Python.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Natural Language :: English
License :: OSI Approved :: MIT License
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
Operating System :: MacOS
Programming Language :: Python :: 3
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development :: Libraries :: Python Modules
"""
HERE = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(HERE, "pyChakraCore", "README_EN.md"), encoding="utf-8") as fs:
    dataArr = fs.read().splitlines()
    LONG_DESCRIPTION = (
        dataArr[2]
        + "\n\n[ [README-EN](https://github.com/wistn/pyChakraCore/blob/main/pyChakraCore/README_EN.md)]"
    )
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
# package_dir is a dictionary with package names for keys and directories for values. An empty package name represents the “root package” — the directory in the project that contains all Python source files for the package — so in this case the src directory is designated the root package.
PACKAGE_DIR = {"pyChakraCore": "pyChakraCore"}  # or {"": "."}
# Set packages to a list of all packages in your project, including their subpackages, sub-subpackages, etc. Although the packages can be listed manually, setuptools.find_packages() finds them automatically. Use the include keyword argument to find only the given packages. Use the exclude keyword argument to omit packages that are not intended to be released and installed.
PACKAGES = find_packages(
    where=".", exclude=(), include=("*")
)  # where="src" if structure like src/packageXX
PACKAGE_DATA = {
    "pyChakraCore": ["CHANGELOG.md", "README_CN.*", "README_EN.*"],
    "pyChakraCore.windowsx86": ["*.dll", "*.so", "*.dylib"],
    "pyChakraCore.windowsx64": ["*.dll", "*.so", "*.dylib"],
    "pyChakraCore.linux": ["*.dll", "*.so", "*.dylib"],
    "pyChakraCore.osx": ["*.dll", "*.so", "*.dylib"],
}
DATA_FILES = []
if __name__ == "__main__":
    metadata = dict(
        name="pyChakraCore",
        version=__version__,
        author="wistn",
        author_email="wistn@qq.com",
        license="MIT",
        description="pyChakraCore is a Python encapsulation of ChakraCore which is a JavaScript engine.",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/wistn/pyChakraCore",
        keywords=["javascript-engine", "runtime", "chakracore"],
        platforms=["Windows", "Linux", " MacOS"],
        classifiers=[_ for _ in CLASSIFIERS.splitlines() if _],
        package_dir=PACKAGE_DIR,
        packages=PACKAGES,
        # Don't include_package_data=True.
        include_package_data=False,
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        python_requires=">=3." + str(REQUIRED_PYTHON[1]) + ", <4",
        # “install_requires” should be used to specify what dependencies a project minimally needs to run. When the project is installed by pip, this is the specification that is used to install its dependencies.
        install_requires=[],
        # entry_points={"console_scripts": ["xx=xx.__main__:main"]},
    )
    setup(**metadata)
