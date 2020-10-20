# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-10-20
LastEditTime:,:2020-10-20
LastEditors:,:Do not edit
Description:
"""
import sys
import os
# if __package__ == "" or __package__ == None:
#     path = os.path.dirname(os.path.dirname(__file__))
#     sys.path.insert(0, path)
from pyChakraCore import pyChakraCore


if sys.argv.__len__() > 1 and os.path.isfile(sys.argv[1]) and ".js" in sys.argv[1]:
    with open(sys.argv[1], "r", encoding="utf-8") as fs:
        jscode = fs.read()
else:
    jscode = "console.log(typeof (1 + 1) == 'number')"
vm = pyChakraCore()
vm.run(jscode)

