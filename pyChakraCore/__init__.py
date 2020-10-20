# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-08-03
LastEditTime:2020-10-20
LastEditors:Do not edit
Description:
"""
import ctypes
import json
import os
import sys
import platform

if __package__ == "" or __package__ == None:
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)
from pyChakraCore.ChakraCommon import failCheck

if sys.platform == "darwin":
    pathChakraCore = "/../pyChakraCore/osx/libChakraCore.dylib"
elif sys.platform.startswith("linux"):
    pathChakraCore = "/../pyChakraCore/linux/libChakraCore.so"
elif sys.platform == "win32":
    if platform.architecture()[0].startswith("64"):
        pathChakraCore = "/../pyChakraCore/windowsx64/ChakraCore.dll"
    else:
        pathChakraCore = "/../pyChakraCore/windowsx86/ChakraCore.dll"


if sys.platform != "win32":
    chakraCore = ctypes.CDLL(
        os.path.split(os.path.realpath(__file__))[0] + pathChakraCore
    )
else:
    chakraCore = ctypes.WinDLL(
        os.path.split(os.path.realpath(__file__))[0] + pathChakraCore
    )


pretty = """
    /* 转义符作为字符串被eval执行时需要双倍反斜杠 */
    var backslashN = '\\n';
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
        var maxLength = 300; /* 限制字符串、对象数组序列化JSON长度 */
        function str(obj) {
            var jsType = Object.prototype.toString.call(obj);
            if (
                jsType.match(/object (String|Date|Function|JSON|Math|RegExp)/)
            ) {
                return JSON.stringify(
                    String(obj).length > maxLength
                        ? String(obj).slice(0, maxLength) + '...'
                        : String(obj)
                );
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
                    return JSON.stringify(
                        String(obj).length > maxLength
                            ? String(obj).slice(0, maxLength) + '...'
                            : String(obj)
                    );
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
        chakraCore.JsSetCurrentContext(self.context)
        chakraCore.JsDisposeRuntime(self.runtime)

    def __init__(self):
        if sys.platform != "win32":
            # You are expected to call DllMain manually on non-Windows
            chakraCore.DllMain(0, 1, 0)  # Attach process
            chakraCore.DllMain(0, 2, 0)  # Attach main thread
        self.runtime = ctypes.c_void_p()  # Create Javascript Runtime.
        chakraCore.JsCreateRuntime(
            0x00000000, ctypes.c_void_p(), ctypes.byref(self.runtime)
        )
        self.context = ctypes.c_void_p()
        chakraCore.JsCreateContext(
            self.runtime, ctypes.byref(self.context)
        )  # Create an execution context.一个Runtime可包含多个Context
        chakraCore.JsSetCurrentContext(self.context)
        # Now set the current execution context.
        self.jGlobal = ctypes.c_void_p()
        chakraCore.JsGetGlobalObject(ctypes.byref(self.jGlobal))
        self.jUndefined = ctypes.c_void_p()
        chakraCore.JsGetUndefinedValue(ctypes.byref(self.jUndefined))
        self.jNull = ctypes.c_void_p()
        chakraCore.JsGetNullValue(ctypes.byref(self.jNull))
        self.jSourceContextCookie = 0
        self.run("var getType = (obj) => Object.prototype.toString.call(obj);")
        cfunctype_JsNativeFunction = ctypes.CFUNCTYPE(
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_bool,
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_ushort,
            ctypes.POINTER(ctypes.c_void_p),
        )  # ChakraCore的JsNativeFunction要求类型
        self.c_EchoCallback = cfunctype_JsNativeFunction(self.EchoCallback)
        self.registerMethod(self.c_EchoCallback, "console.log")
        self.registerMethod(self.c_EchoCallback, "WScript.Echo")
        self.registerMethod(self.c_EchoCallback, "print")

    def run(self, code):
        chakraCore.JsSetCurrentContext(self.context)
        jResult = self.getJValue(code)
        return self.jValueToNativeStr(jResult)

    def getJValue(self, code):
        chakraCore.JsSetCurrentContext(self.context)
        sourceUrl = "sourceUrl:" + code.strip()[0:15]
        jSourceUrl = ctypes.c_void_p()  # create JsValueRef from sourceUrl
        chakraCore.JsCreateString(
            sourceUrl.encode("UTF-8"),
            len(sourceUrl.encode("UTF-8")),
            ctypes.byref(jSourceUrl),
        )
        cBufferScriptSource = ctypes.create_string_buffer(code.encode("UTF-16"))
        jScriptSource = ctypes.c_void_p()  # Create ArrayBuffer from script
        chakraCore.JsCreateExternalArrayBuffer(
            cBufferScriptSource,
            len(cBufferScriptSource),
            ctypes.c_void_p(),
            ctypes.c_void_p(),
            ctypes.byref(jScriptSource),
        )
        jResult = ctypes.c_void_p()
        failCheck(
            chakraCore.JsRun(
                jScriptSource,
                self.jSourceContextCookie,
                jSourceUrl,
                0x2,
                ctypes.byref(jResult),
            )
        )
        return jResult

    def jValueToNativeStr(self, jValue):
        # chakraCore.JsSetCurrentContext(self.context)
        # Convert result to String in JavaScript; redundant if script returns a String
        jString = ctypes.c_void_p()
        chakraCore.JsConvertValueToString(jValue, ctypes.byref(jString))
        cLenString = ctypes.c_size_t()
        # Get buffer size needed for the result string
        chakraCore.JsCopyString(jString, ctypes.c_void_p(), 0, ctypes.byref(cLenString))
        cBuffer = ctypes.create_string_buffer(
            cLenString.value + 1
        )  # buffer is big enough to store the result
        # Get String from JsValueRef
        chakraCore.JsCopyString(
            jString, ctypes.byref(cBuffer), cLenString.value + 1, ctypes.c_void_p()
        )
        # Set `null-ending` to the end
        cBufferLastByte = (ctypes.c_char * cLenString.value).from_address(
            ctypes.addressof(cBuffer)
        )
        cBufferLastByte = b"\0"
        return cBuffer.value.decode("UTF-8")

    def _jValueToJson(self, jValue):
        jResult = self._callFunctionWithJArgs(
            "JSON.stringify", (ctypes.c_void_p * 2)(self.jUndefined, jValue),
        )
        strJSON = self.jValueToNativeStr(jResult)
        return strJSON

    def _jValueToPretty(self, jValue):
        jResult = self._callFunctionWithJArgs(
            "pretty", (ctypes.c_void_p * 2)(self.jUndefined, jValue),
        )
        return self.jValueToNativeStr(jResult)

    def callFunction(self, funName, *pyArgs):
        chakraCore.JsSetCurrentContext(self.context)
        jFunArgs = (ctypes.c_void_p * (len(pyArgs) + 1))(self.jUndefined)
        for i in range(len(pyArgs)):
            jFunArgs[i + 1] = self.getJValue(repr(pyArgs[i]))
        jResult = self._callFunctionWithJArgs(funName, jFunArgs)
        return self.jValueToNativeStr(jResult)

    def getTypeToNativeStr(self, jValue):
        jResult = self._callFunctionWithJArgs(
            "getType", (ctypes.c_void_p * 2)(self.jUndefined, jValue),
        )  # 因为本py方法调用 Object.prototype.toString.call 失败，所以在本py构造函数定义该js函数提供调用。
        jsType = self.jValueToNativeStr(jResult)
        return jsType

    def _callFunctionWithJArgs(self, funName, jFunArgs):
        chakraCore.JsSetCurrentContext(self.context)
        jResult = ctypes.c_void_p()
        jFunction = self.getJValue(funName)

        # 或者global.funName调用
        # jResult = ctypes.c_void_p()
        # funNameComponent = funName.split(".")
        # jId = ctypes.c_void_p()
        # jObj = self.jGlobal
        # jValue = ctypes.c_void_p()
        # for i in range(len(funNameComponent)):
        #     chakraCore.JsCreatePropertyId(
        #         funNameComponent[i].encode("UTF-8"),
        #         len(funNameComponent[i].encode("UTF-8")),
        #         ctypes.byref(jId),
        #     )
        #     chakraCore.JsGetProperty(jObj, jId, ctypes.byref(jValue))
        #     jObj = jValue
        # jFunction = jValue

        failCheck(
            chakraCore.JsCallFunction(
                jFunction, ctypes.byref(jFunArgs), len(jFunArgs), ctypes.byref(jResult),
            )
        )
        return jResult

    def callFunctionToJson(self, funName, *pyArgs):
        # jsonArgs = json.dumps(pyArgs)
        # return self.run(
        #     "JSON.stringify("
        #     + """{0}(...JSON.parse({1}))""".format(funName, repr(jsonArgs))
        #     + ")"
        # )
        chakraCore.JsSetCurrentContext(self.context)
        jFunArgs = (ctypes.c_void_p * (len(pyArgs) + 1))(self.jUndefined)
        for i in range(len(pyArgs)):
            jFunArgs[i + 1] = self.getJValue(repr(pyArgs[i]))
        try:
            jResult = self._callFunctionWithJArgs(funName, jFunArgs)
        except Exception as ex:
            raise ex
        return self._jValueToJson(jResult)

    def registerMethod(self, nativeFunction, funName):
        # chakraCore.JsSetCurrentContext(self.context)
        jFunction = ctypes.c_void_p()
        chakraCore.JsCreateFunction(
            # nativeFunction, ctypes.c_void_p(), ctypes.byref(jFunction),
            nativeFunction,
            ctypes.byref(self.jNull),
            ctypes.byref(jFunction),
        )
        funNameComponents = funName.split(".")
        jId = ctypes.c_void_p()
        jObj = self.jGlobal
        jValue = ctypes.c_void_p()
        for component in funNameComponents[0:-1]:
            chakraCore.JsCreatePropertyId(
                component.encode("UTF-8"),
                len(component.encode("UTF-8")),
                ctypes.byref(jId),
            )
            chakraCore.JsGetProperty(jObj, jId, ctypes.byref(jValue))
            if self.getTypeToNativeStr(jValue) == "[object Undefined]":
                jValue = ctypes.c_void_p()
                chakraCore.JsCreateObject(ctypes.byref(jValue))
                chakraCore.JsSetProperty(jObj, jId, jValue, True)
            jObj = jValue
        jValue = jFunction
        chakraCore.JsCreatePropertyId(
            funNameComponents[-1].encode("UTF-8"),
            len(funNameComponents[-1].encode("UTF-8")),
            ctypes.byref(jId),
        )
        chakraCore.JsSetProperty(jObj, jId, jValue, True)

    def EchoCallback(
        self,
        valueJCallee,
        isConstructCall,
        ptrArguments,
        argumentCount,
        ptrCallbackState,
    ):
        # chakraCore虚拟机里，注册方法第一个参数都是undefined。当参数not defined 时，不会进入本原生函数，而是JsRun返回空字符串''回调用处。
        for i in range(1, argumentCount):
            jString = ctypes.c_void_p(ptrArguments[i])
            string = self.jValueToNativeStr(jString)
            if i > 1:
                print(" ", end="")
            print(string, end="")
        print("\n", end="")
        return self.jUndefined.value
