# pyChakraCore

pyChakraCore is a Python encapsulation of ChakraCore which is a C project. ChakraCore is a JavaScript engine that Microsoft Edge browser ever used.

[ [中文说明](README_CN.md)]

---

## Features

-   Add support for Javascript to any Python project on `Windows x86/Windows x64/Linux/macOS` environment
-   Support `es6 syntax`, `memory of context variables`, `console.log`
-   Has `exception handling method`, `call stack includes error`

---

## API

```python
# 1. Instance method
"""
* (1.1 Method recommended) Run js script code, return string result(maybe "null"/"undefined").
* @param script: The js script code to run.
"""
run(script: str): str

# (1.2 Methods help develop):
"""
* Convert code string to a js value, the value also is python module's fundamental ctypes data type, cannot be handled directly by normal python functions.
* @param code: The js code string.
"""
getJValue(code: str): ctypes._SimpleCData

"""
* Execute a js function, return a string converted from ctypes data.
* @param funName: The string represents js function's name.
* @param code_arguments: The sequence of string which represents js value argument in the function, may be empty.
"""
callFunction(funName: str, *code_arguments: str): str

"""
* Execute a js function, return a JSON format string converted from ctypes data.
* @param funName: The string represents js function's name.
* @param code_arguments: The sequence of string which represents js value argument in the function, may be empty.
"""
callFunctionToJson(funName: str, *code_arguments: str): JSON str

"""
* Bind a C function to a js function.
* @param nativeFunction: The C callable function to call when the js function is executed, wrapped a python function by ctypes.CFUNCTYPE。
* @param funName: The string represents js function's name.
* @param callbackState: User provided state that will be passed back to the callback.
"""
registerMethod(nativeFunction: Any, funName: str, callbackState?: ctypes._SimpleCData): None

# 2. Static method
"""
* Get the JavaScript type of js value, from names of enumerations class JsValueType in the module.
* @param jValue: A js value.
"""
getValueType(jValue: ctypes._SimpleCData): str

"""
* Get python int value from a js value.
* @param jValue: A js value.
"""
jValueToNativeInt(jValue: ctypes._SimpleCData): int

"""
* Get python str value from a js value.
* @param jValue: A js value.
"""
jValueToNativeStr(jValue: ctypes._SimpleCData): str

"""
* Get a js property ID associated with a name.
* @param name: The name of the property ID to get or create, the name may consist of only digits.
"""
getPropertyIdFromName(name: str): ctypes._SimpleCData

"""
* Get an object's property.
* @param jObj: A js object has properties.
* @param str_propertyId: The name string of the property ID.
"""
jGetProperty(jObj: ctypes._SimpleCData, str_propertyId: str): ctypes._SimpleCData

"""
* Set an object's property，return the code number represents the operation succeeded or failed.
* @param jObj: A js object has properties.
* @param str_propertyId: The name string of the property ID.
* @param jValue: New value of the property.
* @param useStrictRules: The property set should follow strict mode rules or not.
"""
jSetProperty(jObj: ctypes._SimpleCData, str_propertyId: str, jValue: ctypes._SimpleCData, useStrictRules: bool): int
```

### [ [Features](#Features)|[ API ](#API)|[Usage](#Usage)|[Configuration](#Configuration)|[Dependencies](#Dependencies)|[CHANGELOG.md](CHANGELOG.md)]

## Usage

After pip installs the project as `python -m pip install pyChakraCore`

```python
>>> from pyChakraCore import pyChakraCore
>>> vm=pyChakraCore()
>>> jscode = "console.log('run: typeof 1 is', typeof 1)"
>>> vm.run(jscode)
run: typeof 1 is number
```

## Configuration

-   Dependent libraries .dll/.so/.dylib files which [ChakraCore](https://github.com/chakra-core/ChakraCore) v1.11.20 releases, save in windowsx86/windowsx64/linux/osx folders under project directory.

---

## Dependencies

-   [python](https://www.python.org/) 3.4 or above
