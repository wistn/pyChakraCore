# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-10-20
LastEditTime:,:2020-10-22
LastEditors:,:Do not edit
Description:
"""
import codecs
import os
import re

from setuptools import setup, find_packages

VERSION = "0.1.1dev0"
PACKAGES = find_packages(
    where=".", exclude=(), include=("*",)
)  # where不能写实际src文件夹不然找不到子包
KEYWORDS = ["javascript-engine", "runtime", "chakracore"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = []


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.rst"), encoding="utf-8") as fs:
    dataArr = fs.read().splitlines()
    LONG_DESCRIPTION = dataArr[0] + dataArr[1]


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as fs:
        return fs.read()


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), "META_FILE", re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name="pyChakraCore",
        version=VERSION,
        author="wistn",
        author_email="wistn@qq.com",
        url="https://github.com/wistn/pyChakraCore",
        description="pyChakraCore is a JavaScript engine on python bridges to Microsoft ChakraCore.",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/x-rst",
        classifiers=CLASSIFIERS,
        platforms=["Windows", "Linux", " MacOS"],
        license="MIT",
        keywords=KEYWORDS,
        packages=PACKAGES,
        # package_dir={"": "pyChakraCore"},
        # This field lists other packages that your project depends on to run.
        # Any package you put here will be installed by pip when your project is
        # installed, so they must be valid existing projects.
        install_requires=INSTALL_REQUIRES,
        include_package_data=False,  # True就是坑
        # package_data={"pyChakraCore": [ "./test.py"],},
        package_data={
            "pyChakraCore": [
                os.path.join(HERE, "test.py")
            ],  # 文件在包同级目录，sdist不包含，只能在源代码包用
            "pyChakraCore.windowsx86": [
                os.path.join(HERE, "pyChakraCore/windowsx86/ChakraCore.dll")
            ],
            "pyChakraCore.windowsx64": [
                os.path.join(HERE, "pyChakraCore/windowsx64/ChakraCore.dll")
            ],
            "pyChakraCore.osx": [
                os.path.join(HERE, "pyChakraCore/osx/libChakraCore.dylib")
            ],
            "pyChakraCore.linux": [
                os.path.join(HERE, "pyChakraCore/linux/libChakraCore.so")
            ],
        },
        # data_files=[('pyChakraCore', [os.path.join(HERE, "test.py")]),],写在这里无效
    )
"""
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('my_data', ['data/data_file'])],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={"dev": ["check-manifest"], "test": ["coverage"],},  # Optional
"""
