# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-08-03
LastEditors:Do not edit
LastEditTime:2021-03-16
Description:
"""
from .ChakraCore import *
from .ChakraCommon import *
import ctypes
import json

__version__ = "0.2.0"
pretty = r"""
    var backslashN = '\n';
    function pretty(obj, space) {
        var indent = '',
            subIndents = '';
        if (space == null) space = 4;
        if (typeof space == 'number') {
            for (var i = 0; i < space; i++) {
                indent += ' ';
            }
        } else if (typeof space == 'string') {
            indent = space;
        }
        function str(obj) {
            var jsType = Object.prototype.toString.call(obj);
            if (
                jsType.match(/object (String|Date|Function|JSON|Math|RegExp)/)
            ) {
                return JSON.stringify(String(obj));
            } else if (jsType.match(/object (Number|Boolean|Null)/)) {
                return JSON.stringify(obj);
            } else if (jsType.match(/object Undefined/)) {
                return JSON.stringify('undefined');
            } else {
                if (jsType.match(/object (Array|Arguments|Map|Set)/)) {
                    if (jsType.match(/object (Map|Set)/)) {
                        /* es6新增的方法和参数类型 */
                        obj = Array.from(obj);
                    }
                    var partial = [];
                    subIndents = subIndents + indent;
                    var len = obj.length;
                    for (var i = 0; i < len; i++) {
                        partial.push(str(obj[i]));
                    }
                    var result =
                        len == 0
                            ? '[]'
                            : indent.length
                            ? '[' +
                              backslashN +
                              subIndents +
                              partial.join(',' + backslashN + subIndents) +
                              backslashN +
                              subIndents.slice(indent.length) +
                              ']'
                            : '[' + partial.join(',') + ']';
                    subIndents = subIndents.slice(indent.length);
                    return result;
                } else if (
                    jsType.match(
                        /object (Object|Error|global|Window|HTMLDocument)/i
                    ) ||
                    obj instanceof Error
                ) {
                    var partial = [];
                    subIndents = subIndents + indent;
                    var ownProps = Object.getOwnPropertyNames(obj);
                    /* Object.keys 为自身非继承属性(不用for in因为for遍历继承的祖先属性)，Object.getOwnPropertyNames 在前者基础上包括不可枚举属性  */
                    var len = ownProps.length;
                    for (var i = 0; i < len; i++) {
                        partial.push(
                            str(ownProps[i]) +
                                (indent.length ? ': ' : ':') +
                                str(obj[ownProps[i]])
                        );
                    }
                    var result =
                        len == 0
                            ? '{}'
                            : indent.length
                            ? '{' +
                              backslashN +
                              subIndents +
                              partial.join(',' + backslashN + subIndents) +
                              backslashN +
                              subIndents.slice(indent.length) +
                              '}'
                            : '{' + partial.join(',') + '}';
                    subIndents = subIndents.slice(indent.length);
                    return result;
                } else {
                    return JSON.stringify(String(obj));
                }
            }
        }
        function decycle(obj) {
            /* the function can solve circular structure like JSON.decycle, the return value can be decoded by JSON.retrocycle(JSON.parse()) */
            var arrParents = [];
            return (function derez(obj, path) {
                var jsType = Object.prototype.toString.call(obj);
                if (
                    jsType.match(
                        /object (String|Date|Function|JSON|Math|RegExp|Number|Boolean|Null|Undefined)/
                    )
                ) {
                    return obj;
                } else {
                    if (jsType.match(/object (Array|Arguments|Map|Set)/)) {
                        var len = arrParents.length;
                        for (var i = 0; i < len; i++) {
                            /* arr like [obj, '$'] */
                            var arr = arrParents[i];
                            if (obj === arr[0]) {
                                return { $ref: arr[1] };
                            }
                        }
                        arrParents.push([obj, path]);
                        var newObj = [];
                        if (jsType.match(/object (Map|Set)/)) {
                            /* es6新增的方法和参数类型 */
                            obj = Array.from(obj);
                        }
                        var length = obj.length;
                        for (var i = 0; i < length; i++) {
                            newObj[i] = derez(obj[i], path + '[' + i + ']');
                        }
                        return newObj;
                    } else {
                        var len = arrParents.length;
                        for (var i = 0; i < len; i++) {
                            /* arr like [obj, '$'] */
                            var arr = arrParents[i];
                            if (obj === arr[0]) {
                                return { $ref: arr[1] };
                            }
                        }
                        arrParents.push([obj, path]);
                        var newObj = {};
                        var ownProps = Object.getOwnPropertyNames(obj);
                        var length = ownProps.length;
                        for (var i = 0; i < length; i++) {
                            newObj[ownProps[i]] = derez(
                                obj[ownProps[i]],
                                path + '[' + JSON.stringify(ownProps[i]) + ']'
                            );
                        }
                        return newObj;
                    }
                }
            })(obj, '$');
        }
        return str(decycle(obj));
    }
"""


class pyChakraCore:
    def __del__(self):
        ChakraCore.JsSetCurrentContext(self.context)
        ChakraCore.JsDisposeRuntime(self.runtime)

    def __init__(self):
        self.runtime = ctypes.c_void_p()  # Create Javascript Runtime.
        ChakraCore.JsCreateRuntime(
            0x00000000, ctypes.c_void_p(), ctypes.byref(self.runtime)
        )
        self.context = ctypes.c_void_p()
        ChakraCore.JsCreateContext(
            self.runtime, ctypes.byref(self.context)
        )  # Create an execution context.一个Runtime可包含多个Context
        self.j_sourceContext = 0
        ChakraCore.JsSetCurrentContext(self.context)
        # Now set the current execution context.
        self.jGlobal = ctypes.c_void_p()
        ChakraCore.JsGetGlobalObject(ctypes.byref(self.jGlobal))
        # 避免展开WebAssembly对象时失败，所以直接删除对象。
        ChakraCore.JsDeleteProperty(
            self.jGlobal,
            pyChakraCore.getPropertyIdFromName("WebAssembly"),
            False,
            ctypes.byref(ctypes.c_void_p()),
        )
        self.jUndefined = ctypes.c_void_p()
        ChakraCore.JsGetUndefinedValue(ctypes.byref(self.jUndefined))
        self.jNull = ctypes.c_void_p()
        ChakraCore.JsGetNullValue(ctypes.byref(self.jNull))
        self.run(pretty)
        self.c_EchoCallback = cfunctype_JsNativeFunction(self.EchoCallback)
        self.registerMethod(self.c_EchoCallback, "print")
        # self.registerMethod(self.c_EchoCallback, "WScript.Echo")
        self.registerMethod(self.c_EchoCallback, "console.log")

    def run(self, code):
        j_result = self.getJValue(code)
        self.j_sourceContext += 1
        return pyChakraCore.jValueToNativeStr(j_result)

    def getJValue(self, code):
        ChakraCore.JsSetCurrentContext(self.context)
        j_sourceContext = self.j_sourceContext
        sourceUrl = "sourceUrl:" + code.strip()[0:15]
        j_sourceUrl = ctypes.c_void_p()  # create JsValueRef from sourceUrl
        ChakraCore.JsCreateString(
            sourceUrl.encode("UTF-8"),
            len(sourceUrl.encode("UTF-8")),
            ctypes.byref(j_sourceUrl),
        )
        cBuffer_scriptSource = ctypes.create_string_buffer(code.encode("UTF-16"))
        j_scriptSource = ctypes.c_void_p()  # Create ArrayBuffer from script
        ChakraCore.JsCreateExternalArrayBuffer(
            cBuffer_scriptSource,
            len(cBuffer_scriptSource),
            ctypes.c_void_p(),
            ctypes.c_void_p(),
            ctypes.byref(j_scriptSource),
        )
        j_result = ctypes.c_void_p()
        failCheck(
            ChakraCore.JsRun(
                j_scriptSource,
                j_sourceContext,
                j_sourceUrl,
                0x2,
                ctypes.byref(j_result),
            )
        )
        return j_result

    def _jValueToJson(self, jValue):
        j_result = self._callFunctionWithJArgs(
            "JSON.stringify", (ctypes.c_void_p * 2)(self.jUndefined, jValue),
        )
        strJSON = pyChakraCore.jValueToNativeStr(j_result)
        return strJSON

    def _jValueToPretty(self, jValue):
        j_result = self._callFunctionWithJArgs(
            "pretty", (ctypes.c_void_p * 2)(self.jUndefined, jValue),
        )
        return pyChakraCore.jValueToNativeStr(j_result)

    def callFunction(self, funName, *code_arguments):
        argsArray_code = "[" + ",".join(code_arguments) + "]"
        return self.run(funName + "(..." + argsArray_code + ")")
        # Do not use func.apply because not know the value of this provided for the call to func

    def _callFunctionWithJArgs(self, funName, j_arguments):
        j_result = ctypes.c_void_p()
        jFunction = self.getJValue(funName)
        # 或者global.funName调用
        # j_result = ctypes.c_void_p()
        # components = funName.split(".")
        # jObj = self.jGlobal
        # for i in range(len(components)):
        #     jValue = pyChakraCore.jGetProperty(jObj, components[i])
        #     jObj = jValue
        # jFunction = jValue
        failCheck(
            ChakraCore.JsCallFunction(
                jFunction,
                ctypes.byref(j_arguments),
                len(j_arguments),
                ctypes.byref(j_result),
            )
        )
        return j_result

    def _callConstructorWithJArgs(self, funName, j_arguments):
        j_result = ctypes.c_void_p()
        funName = funName.strip()
        if "new " in funName:
            funName = funName[4:].strip()
        jFunction = self.getJValue(funName)
        failCheck(
            ChakraCore.JsConstructObject(
                jFunction,
                ctypes.byref(j_arguments),
                len(j_arguments),
                ctypes.byref(j_result),
            )
        )
        return j_result

    def callFunctionToJson(self, funName, *code_arguments):
        argsArray_code = "[" + ",".join(code_arguments) + "]"
        strJSON = self.run("JSON.stringify(" + funName + "(..." + argsArray_code + "))")
        return strJSON

    def registerMethod(
        self, nativeFunction, funName, callbackState=ctypes.py_object(None)
    ):
        ChakraCore.JsSetCurrentContext(self.context)
        jFunction = ctypes.c_void_p()
        ChakraCore.JsCreateFunction(
            nativeFunction, callbackState, ctypes.byref(jFunction),
        )  # 匿名函数
        components = funName.split(".")
        jObj = self.jGlobal
        for i in range(len(components)):
            if i == len(components) - 1:
                pyChakraCore.jSetProperty(jObj, components[i], jFunction, True)
                break
            jValue = pyChakraCore.jGetProperty(jObj, components[i])
            if pyChakraCore.getValueType(jValue) == "JsUndefined":
                jValue = ctypes.c_void_p()
                ChakraCore.JsCreateObject(ctypes.byref(jValue))
                pyChakraCore.jSetProperty(jObj, components[i], jValue, True)
            jObj = jValue

    def EchoCallback(
        self, ptr_callee, isConstructCall, ptrj_arguments, argumentCount, callbackState,
    ):
        # chakraCore虚拟机里，注册方法第一个参数都是undefined。当其他参数出现not defined 时，不会进入本原生函数，而是JsRun返回空字符串''回调用处。
        for i in range(1, argumentCount):
            jString = ctypes.c_void_p(ptrj_arguments[i])
            string = pyChakraCore.jValueToNativeStr(jString)
            if i > 1:
                print(" ", end="")
            print(string, end="")
        print("\n", end="")
        # return self.jUndefined.value


pyChakraCore.getValueType = staticmethod(getValueType)
pyChakraCore.jValueToNativeInt = staticmethod(jValueToNativeInt)
pyChakraCore.jValueToNativeStr = staticmethod(jValueToNativeStr)
pyChakraCore.getPropertyIdFromName = staticmethod(getPropertyIdFromName)
pyChakraCore.jGetProperty = staticmethod(jGetProperty)
pyChakraCore.jSetProperty = staticmethod(jSetProperty)

