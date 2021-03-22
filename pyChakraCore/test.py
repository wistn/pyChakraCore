# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2021-03-14
LastEditors:Do not edit
LastEditTime:2021-03-16
Description:
"""
import unittest
import os
import sys

if __package__ == "" or __package__ == None:
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    sys.path.insert(0, path)
from pyChakraCore import pyChakraCore, failCheck

# print(sys.modules["pyChakraCore"])
testObj = pyChakraCore()
# the class below cann't be defined in any function if uses unittest.main method.
class TestCase(unittest.TestCase):
    def setUp(self):
        self.vm = testObj

    def tearDown(self):
        pass  # Method called immediately after the test method has been called and the result recorded, to cleanup resources used during the test like writes 'self.widget.dispose()'. This method will only be called if the internal setUp() succeeds, regardless of the outcome of the test method.

    def test_callFunction(self):
        ret = self.vm.callFunction("String", "1+1")
        # print("test_callFunction", "2")
        self.assertEqual(ret, "2")

    def test_callFunctionToJson(self):
        ret = self.vm.callFunctionToJson("new Array", "'str1'")
        # print("test_callFunctionToJson", repr('["str1"]'))
        self.assertEqual(ret, '["str1"]')

    def test_getJValue(self):
        ret = self.vm.getJValue("undefined")
        # print("test_getJValue", type(ret))
        self.assertEqual(ret.value, self.vm.jUndefined.value)

    def test_getValueType(self):
        ret = self.vm.getValueType(self.vm.jNull)
        # print("test_getValueType", ret)
        self.assertEqual(ret, "JsNull")

    def test_jGet_jSetProperty(self):
        failCheck(
            self.vm.jSetProperty(
                self.vm.getJValue("console"),
                "alsoLog",
                self.vm.jGetProperty(self.vm.getJValue("console"), "log"),
            )
        )
        ret = self.vm.run("console.alsoLog")
        # print("test_jGet_jSetProperty", ret)
        self.assertEqual(ret, "function () { [native code] }")

    def test_jValueToNativeInt(self):
        ret = self.vm.jValueToNativeInt(self.vm.getJValue("1"))
        # print("test_jValueToNativeInt", type(ret))
        self.assertEqual(ret, 1)

    def test_jValueToNativeStr(self):
        ret = self.vm.jValueToNativeStr(self.vm.getJValue("1"))
        # print("test_jValueToNativeStr", type(ret))
        self.assertEqual(ret, "1")

    def test_registerMethod(self):
        self.vm.registerMethod(self.vm.c_EchoCallback, "console.info")
        ret = self.vm.run("console.info('test_registerMethod','hi')")
        self.assertEqual(ret, "undefined")

    def test_run(self):
        ret = self.vm.run("console.log('test_run: typeof 1 is', typeof 1)")
        self.assertEqual(ret, "undefined")


def main():
    fullname = os.path.realpath(__file__)
    unittest.main(
        module=os.path.basename(os.path.dirname(fullname))
        + "."
        + os.path.basename(fullname).replace(".py", ""),
        exit=False,
        verbosity=2,
    )
    """the following commented-out code equals unittest.main(module="PackageName.ModuleName", exit=True, verbosity=2)"""
    # suite = unittest.TestSuite()
    # arr = [
    #     TestCase("test_run"),
    #     TestCase("test_getJValue"),
    #     TestCase("test_callFunction"),
    #     TestCase("test_callFunctionToJson"),
    #     TestCase("test_registerMethod"),
    #     TestCase("test_getValueType"),
    #     TestCase("test_jValueToNativeInt"),
    #     TestCase("test_jValueToNativeStr"),
    #     TestCase("test_jGet_jSetProperty"),
    # ]
    # suite.addTests(arr)
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)


if __name__ == "__main__":
    main()
    pass
