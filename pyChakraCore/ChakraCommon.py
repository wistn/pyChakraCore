# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-10-10
LastEditors:Do not edit
LastEditTime:2021-03-16
Description:
"""
from .ChakraCore import ChakraCore
import ctypes
from enum import IntEnum, auto


class JsErrorCode(IntEnum):
    # <summary>
    #     Success error code.
    # </summary>
    JsNoError = 0
    # <summary>
    #     Category of errors that relates to incorrect usage of the API itself.
    # </summary>
    JsErrorCategoryUsage = 0x10000
    # <summary>
    #     An argument to a hosting API was invalid.
    # </summary>
    JsErrorInvalidArgument = auto()
    # <summary>
    #     An argument to a hosting API was null in a context where null is not allowed.
    # </summary>
    JsErrorNullArgument = auto()
    # <summary>
    #     The hosting API requires that a context be current, but there is no current context.
    # </summary>
    JsErrorNoCurrentContext = auto()
    # <summary>
    #     The engine is in an exception state and no APIs can be called until the exception is
    #     cleared.
    # </summary>
    JsErrorInExceptionState = auto()
    # <summary>
    #     A hosting API is not yet implemented.
    # </summary>
    JsErrorNotImplemented = auto()
    # <summary>
    #     A hosting API was called on the wrong thread.
    # </summary>
    JsErrorWrongThread = auto()
    # <summary>
    #     A runtime that is still in use cannot be disposed.
    # </summary>
    JsErrorRuntimeInUse = auto()
    # <summary>
    #     A bad serialized script was used, or the serialized script was serialized by a
    #     different version of the Chakra engine.
    # </summary>
    JsErrorBadSerializedScript = auto()
    # <summary>
    #     The runtime is in a disabled state.
    # </summary>
    JsErrorInDisabledState = auto()
    # <summary>
    #     Runtime does not support reliable script interruption.
    # </summary>
    JsErrorCannotDisableExecution = auto()
    # <summary>
    #     A heap enumeration is currently underway in the script context.
    # </summary>
    JsErrorHeapEnumInProgress = auto()
    # <summary>
    #     A hosting API that operates on object values was called with a non-object value.
    # </summary>
    JsErrorArgumentNotObject = auto()
    # <summary>
    #     A script context is in the middle of a profile callback.
    # </summary>
    JsErrorInProfileCallback = auto()
    # <summary>
    #     A thread service callback is currently underway.
    # </summary>
    JsErrorInThreadServiceCallback = auto()
    # <summary>
    #     Scripts cannot be serialized in debug contexts.
    # </summary>
    JsErrorCannotSerializeDebugScript = auto()
    # <summary>
    #     The context cannot be put into a debug state because it is already in a debug state.
    # </summary>
    JsErrorAlreadyDebuggingContext = auto()
    # <summary>
    #     The context cannot start profiling because it is already profiling.
    # </summary>
    JsErrorAlreadyProfilingContext = auto()
    # <summary>
    #     Idle notification given when the host did not enable idle processing.
    # </summary>
    JsErrorIdleNotEnabled = auto()
    # <summary>
    #     The context did not accept the enqueue callback.
    # </summary>
    JsCannotSetProjectionEnqueueCallback = auto()
    # <summary>
    #     Failed to start projection.
    # </summary>
    JsErrorCannotStartProjection = auto()
    # <summary>
    #     The operation is not supported in an object before collect callback.
    # </summary>
    JsErrorInObjectBeforeCollectCallback = auto()
    # <summary>
    #     Object cannot be unwrapped to IInspectable pointer.
    # </summary>
    JsErrorObjectNotInspectable = auto()
    # <summary>
    #     A hosting API that operates on symbol property ids but was called with a non-symbol property id.
    #     The error code is returned by JsGetSymbolFromPropertyId if the function is called with non-symbol property id.
    # </summary>
    JsErrorPropertyNotSymbol = auto()
    # <summary>
    #     A hosting API that operates on string property ids but was called with a non-string property id.
    #     The error code is returned by existing JsGetPropertyNamefromId if the function is called with non-string property id.
    # </summary>
    JsErrorPropertyNotString = auto()
    # <summary>
    #     Module evaluation is called in wrong context.
    # </summary>
    JsErrorInvalidContext = auto()
    # <summary>
    #     Module evaluation is called in wrong context.
    # </summary>
    JsInvalidModuleHostInfoKind = auto()
    # <summary>
    #     Module was parsed already when JsParseModuleSource is called.
    # </summary>
    JsErrorModuleParsed = auto()
    # <summary>
    #     Argument passed to JsCreateWeakReference is a primitive that is not managed by the GC.
    #     No weak reference is required, the value will never be collected.
    # </summary>
    JsNoWeakRefRequired = auto()
    # <summary>
    #     The <c>Promise</c> object is still in the pending state.
    # </summary>
    JsErrorPromisePending = auto()
    # <summary>
    #     Module was not yet evaluated when JsGetModuleNamespace was called.
    # </summary>
    JsErrorModuleNotEvaluated = auto()
    # <summary>
    #     Category of errors that relates to errors occurring within the engine itself.
    # </summary>
    JsErrorCategoryEngine = 0x20000
    # <summary>
    #     The Chakra engine has run out of memory.
    # </summary>
    JsErrorOutOfMemory = auto()
    # <summary>
    #     The Chakra engine failed to set the Floating Point Unit state.
    # </summary>
    JsErrorBadFPUState = auto()
    # <summary>
    #     Category of errors that relates to errors in a script.
    # </summary>
    JsErrorCategoryScript = 0x30000
    # <summary>
    #     A JavaScript exception occurred while running a script.
    # </summary>
    JsErrorScriptException = auto()
    # <summary>
    #     JavaScript failed to compile.
    # </summary>
    JsErrorScriptCompile = auto()
    # <summary>
    #     A script was terminated due to a request to suspend a runtime.
    # </summary>
    JsErrorScriptTerminated = auto()
    # <summary>
    #     A script was terminated because it tried to use <c>eval</c> or <c>function</c> and eval
    #     was disabled.
    # </summary>
    JsErrorScriptEvalDisabled = auto()
    # <summary>
    #     Category of errors that are fatal and signify failure of the engine.
    # </summary>
    JsErrorCategoryFatal = 0x40000
    # <summary>
    #     A fatal error in the engine has occurred.
    # </summary>
    JsErrorFatal = auto()
    # <summary>
    #     A hosting API was called with object created on different javascript runtime.
    # </summary>
    JsErrorWrongRuntime = auto()
    # <summary>
    #     Category of errors that are related to failures during diagnostic operations.
    # </summary>
    JsErrorCategoryDiagError = 0x50000
    # <summary>
    #     The object for which the debugging API was called was not found
    # </summary>
    JsErrorDiagAlreadyInDebugMode = auto()
    # <summary>
    #     The debugging API can only be called when VM is in debug mode
    # </summary>
    JsErrorDiagNotInDebugMode = auto()
    # <summary>
    #     The debugging API can only be called when VM is at a break
    # </summary>
    JsErrorDiagNotAtBreak = auto()
    # <summary>
    #     Debugging API was called with an invalid handle.
    # </summary>
    JsErrorDiagInvalidHandle = auto()
    # <summary>
    #     The object for which the debugging API was called was not found
    # </summary>
    JsErrorDiagObjectNotFound = auto()
    # <summary>
    #     VM was unable to perform the request action
    # </summary>
    JsErrorDiagUnableToPerformAction = auto()


class JsRuntimeAttributes(IntEnum):
    # <summary>
    #     No special attributes.
    # </summary>
    JsRuntimeAttributeNone = 0x00000000
    # <summary>
    #     The runtime will not do any work (such as garbage collection) on background threads.
    # </summary>
    JsRuntimeAttributeDisableBackgroundWork = 0x00000001
    # <summary>
    #     The runtime should support reliable script interruption. This increases the number of
    #     places where the runtime will check for a script interrupt request at the cost of a
    #     small amount of runtime performance.
    # </summary>
    JsRuntimeAttributeAllowScriptInterrupt = 0x00000002
    # <summary>
    #     Host will call <c>JsIdle</c>, so enable idle processing. Otherwise, the runtime will
    #     manage memory slightly more aggressively.
    # </summary>
    JsRuntimeAttributeEnableIdleProcessing = 0x00000004
    # <summary>
    #     Runtime will not generate native code.
    # </summary>
    JsRuntimeAttributeDisableNativeCodeGeneration = 0x00000008
    # <summary>
    #     Using <c>eval</c> or <c>function</c> constructor will throw an exception.
    # </summary>
    JsRuntimeAttributeDisableEval = 0x00000010
    # <summary>
    #     Runtime will enable all experimental features.
    # </summary>
    JsRuntimeAttributeEnableExperimentalFeatures = 0x00000020
    # <summary>
    #     Calling <c>JsSetException</c> will also dispatch the exception to the script debugger
    #     (if any) giving the debugger a chance to break on the exception.
    # </summary>
    JsRuntimeAttributeDispatchSetExceptionsToDebugger = 0x00000040
    # <summary>
    #     Disable Failfast fatal error on OOM
    # </summary>
    JsRuntimeAttributeDisableFatalOnOOM = 0x00000080
    # <summary>
    #     Runtime will not allocate executable code pages
    #     This also implies that Native Code generation will be turned off
    #     Note that this will break JavaScript stack decoding in tools
    #      like WPA since they rely on allocation of unique thunks to
    #      interpret each function and allocation of those thunks will be
    #      disabled as well
    # </summary>
    JsRuntimeAttributeDisableExecutablePageAllocation = 0x00000100


class JsParseScriptAttributes(IntEnum):
    # <summary>
    #     Default attribute
    # </summary>
    JsParseScriptAttributeNone = 0x0
    # <summary>
    #     Specified script is internal and non-user code. Hidden from debugger
    # </summary>
    JsParseScriptAttributeLibraryCode = 0x1
    # <summary>
    #     ChakraCore assumes ExternalArrayBuffer is Utf8 by default.
    #     This one needs to be set for Utf16
    # </summary>
    JsParseScriptAttributeArrayBufferIsUtf16Encoded = 0x2


class JsValueType(IntEnum):
    # <summary>
    #     The value is the <c>undefined</c> value.
    # </summary>
    JsUndefined = 0
    # <summary>
    #     The value is the <c>null</c> value.
    # </summary>
    JsNull = 1
    # <summary>
    #     The value is a JavaScript number value.
    # </summary>
    JsNumber = 2
    # <summary>
    #     The value is a JavaScript string value.
    # </summary>
    JsString = 3
    # <summary>
    #     The value is a JavaScript Boolean value.
    # </summary>
    JsBoolean = 4
    # <summary>
    #     The value is a JavaScript object value.
    # </summary>
    JsObject = 5
    # <summary>
    #     The value is a JavaScript function object value.
    # </summary>
    JsFunction = 6
    # <summary>
    #     The value is a JavaScript error object value.
    # </summary>
    JsError = 7
    # <summary>
    #     The value is a JavaScript array object value.
    # </summary>
    JsArray = 8
    # <summary>
    #     The value is a JavaScript symbol value.
    # </summary>
    JsSymbol = 9
    # <summary>
    #     The value is a JavaScript ArrayBuffer object value.
    # </summary>
    JsArrayBuffer = 10
    # <summary>
    #     The value is a JavaScript typed array object value.
    # </summary>
    JsTypedArray = 11
    # <summary>
    #     The value is a JavaScript DataView object value.
    # </summary>
    JsDataView = 12


cfunctype_JsNativeFunction = ctypes.CFUNCTYPE(
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_bool,
    ctypes.POINTER(ctypes.c_void_p),
    ctypes.c_ushort,
    # ctypes.c_void_p,
    ctypes.py_object,
)  # ChakraCommon.h JsNativeFunction 要求类型


def CreatePropertyIdFromString(str, j_Id):
    return ChakraCore.JsCreatePropertyId(
        str.encode("UTF-8"), len(str.encode("UTF-8")), ctypes.byref(j_Id)
    )


def getValueType(jValue):
    jsType = ctypes.c_int()
    ChakraCore.JsGetValueType(jValue, ctypes.byref(jsType))
    return JsValueType(jsType.value).name


def jValueToNativeInt(jValue):
    c_nativeValue = ctypes.c_int()
    ChakraCore.JsNumberToInt(jValue, ctypes.byref(c_nativeValue))
    return c_nativeValue.value


def jValueToNativeStr(jValue):
    # Convert result to String in JavaScript; redundant if script returns a String
    jString = ctypes.c_void_p()
    ChakraCore.JsConvertValueToString(jValue, ctypes.byref(jString))
    cLenString = ctypes.c_size_t()
    # Get buffer size needed for the result string
    ChakraCore.JsCopyString(jString, ctypes.c_void_p(), 0, ctypes.byref(cLenString))
    cBuffer = ctypes.create_string_buffer(
        cLenString.value + 1
    )  # buffer is big enough to store the result
    # Get String from JsValueRef
    ChakraCore.JsCopyString(
        jString, ctypes.byref(cBuffer), cLenString.value + 1, ctypes.c_void_p()
    )
    # Set `null-ending` to the end
    # cBufferLastByte = (ctypes.c_char * cLenString.value).from_address(
    #     ctypes.addressof(cBuffer)
    # )
    # cBufferLastByte = b"\0"
    return cBuffer.value.decode("UTF-8")


def getPropertyIdFromName(name):
    j_result = ctypes.c_void_p()
    ChakraCore.JsGetPropertyIdFromName(name, ctypes.byref(j_result))
    return j_result


def jGetProperty(jObj, str_propertyId):
    j_result = ctypes.c_void_p()
    ChakraCore.JsGetProperty(
        jObj, getPropertyIdFromName(str_propertyId), ctypes.byref(j_result)
    )
    return j_result


def jSetProperty(jObj, str_propertyId, jValue, useStrictRules=True):
    return ChakraCore.JsSetProperty(
        jObj, getPropertyIdFromName(str_propertyId), jValue, useStrictRules
    )


def failCheck(expr):
    def PrintException(ptr_fileName, jCode):
        try:
            nameJsErrorCode = JsErrorCode(jCode).name
        except Exception as ex:
            nameJsErrorCode = "Unexpected JsErrorCode"
        jException = ctypes.c_void_p()
        ChakraCore.JsGetAndClearException(ctypes.byref(jException))
        if jException.value:
            if (
                jCode.name == "JsErrorScriptCompile"
                or jCode.name == "JsErrorScriptException"
            ):
                errorMessage = jValueToNativeStr(jException)
                if jCode.name == "JsErrorScriptCompile":
                    jId = ctypes.c_void_p()
                    ChakraCore.JsCreatePropertyId(
                        "line".encode("UTF-8"),
                        len("line".encode("UTF-8")),
                        ctypes.byref(jId),
                    )
                    jLine = ctypes.c_void_p()
                    ChakraCore.JsGetProperty(jException, jId, ctypes.byref(jLine))
                    jId = ctypes.c_void_p()
                    ChakraCore.JsCreatePropertyId(
                        "column".encode("UTF-8"),
                        len("column".encode("UTF-8")),
                        ctypes.byref(jId),
                    )
                    jColumn = ctypes.c_void_p()
                    ChakraCore.JsGetProperty(jException, jId, ctypes.byref(jColumn))
                    print(
                        "{}\n\tat code ('':{}:{})".format(
                            errorMessage,
                            jValueToNativeInt(jLine) + 1,
                            jValueToNativeInt(jColumn) + 1,
                        )
                    )
                else:
                    jId = ctypes.c_void_p()
                    ChakraCore.JsCreatePropertyId(
                        "stack".encode("UTF-8"),
                        len("stack".encode("UTF-8")),
                        ctypes.byref(jId),
                    )
                    jStack = ctypes.c_void_p()
                    ChakraCore.JsGetProperty(jException, jId, ctypes.byref(jStack))
                    valueType = ctypes.c_int()
                    errorCode = ChakraCore.JsGetValueType(
                        jStack, ctypes.byref(valueType)
                    )
                    if errorCode != 0 or valueType.value == 0:
                        fName = (
                            ptr_fileName.value
                            if ptr_fileName.value != None
                            else "(unknown)"
                        )
                        jId = ctypes.c_void_p()
                        ChakraCore.JsCreatePropertyId(
                            "source".encode("UTF-8"),
                            len("source".encode("UTF-8")),
                            ctypes.byref(jId),
                        )
                        jSource = ctypes.c_void_p()
                        ChakraCore.JsGetProperty(jException, jId, ctypes.byref(jSource))
                        scriptSource = jValueToNativeStr(jSource)
                        print("thrown at {}:\n^".format(fName))
                        print(
                            errorMessage
                            if len(scriptSource) == 0
                            else errorMessage + ". Source: " + scriptSource
                        )
                    else:
                        print(jValueToNativeStr(jStack))
            else:
                print(nameJsErrorCode)
            return True
        else:
            print(nameJsErrorCode)
        return False

    try:
        jCode = JsErrorCode(expr)
    except Exception:
        jCode = IntEnum("unknownJsErrorCode", {"(unknown)": expr})(expr)
    if jCode != JsErrorCode.JsNoError:
        hasException = ctypes.c_bool()
        ChakraCore.JsHasException(ctypes.byref(hasException))
        if hasException.value:
            PrintException(ctypes.c_wchar_p(None), JsErrorCode.JsErrorScriptException)
        raise Exception(
            "ERROR: {} failed. JsErrorCode=0x{:x} ({})".format(
                str(expr), jCode.value, jCode.name
            )
        )
    return jCode.value
