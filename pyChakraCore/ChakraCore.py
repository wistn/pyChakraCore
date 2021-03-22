# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-12-20
LastEditors:Do not edit
LastEditTime:2021-03-15
Description:
"""

import ctypes
import os
import sys
import platform
import types

if sys.platform == "darwin":
    pathChakraCore = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], "osx", "libChakraCore.dylib"
    )
elif sys.platform.startswith("linux"):
    pathChakraCore = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], "linux", "libChakraCore.so"
    )
elif sys.platform == "win32":
    if platform.architecture()[0].startswith("64"):
        pathChakraCore = os.path.join(
            os.path.split(os.path.realpath(__file__))[0], "windowsx64", "ChakraCore.dll"
        )
    else:
        pathChakraCore = os.path.join(
            os.path.split(os.path.realpath(__file__))[0], "windowsx86", "ChakraCore.dll"
        )

if sys.platform != "win32":
    ChakraCore = ctypes.CDLL(pathChakraCore)
else:
    ChakraCore = ctypes.WinDLL(pathChakraCore)
if sys.platform != "win32":
    # You are expected to call DllMain manually on non-Windows
    ChakraCore.DllMain(0, 1, 0)  # Attach process
    ChakraCore.DllMain(0, 2, 0)  # Attach main thread


def JsGetPropertyIdFromName(self, name, ptr_propertyId):
    return ChakraCore.JsCreatePropertyId(
        name.encode("UTF-8"), len(name.encode("UTF-8")), ptr_propertyId
    )


ChakraCore.JsGetPropertyIdFromName = types.MethodType(
    JsGetPropertyIdFromName, ChakraCore
)


def JS_INVALID_REFERENCE():
    # 要函数创建，不能直接赋值变量 JS_INVALID_REFERENCE = ctypes.c_void_p()，否则其他变量引用后被ctypes.byref操作后会影响 JS_INVALID_REFERENCE 的值。
    return ctypes.c_void_p()


class AutoRestoreContext:
    def __init__(self, newContext):
        self.oldContext = ctypes.c_void_p()
        self.contextChanged = False
        ChakraCore.JsGetCurrentContext(ctypes.byref(self.oldContext))
        if self.oldContext.value != newContext.value:
            ChakraCore.JsSetCurrentContext(newContext)
            self.contextChanged = True
        else:
            self.contextChanged = False

    def __del__(self):
        if (
            self.contextChanged
            and self.oldContext.value != JS_INVALID_REFERENCE().value
        ):
            ChakraCore.JsSetCurrentContext(self.oldContext)
