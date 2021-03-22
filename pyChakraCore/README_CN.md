# pyChakraCore

pyChakraCore 是一个 C 语言项目 ChakraCore 的 python 封装。ChakraCore 是微软 Edge 浏览器曾经使用的 js 虚拟机。

[ [README-EN](README_EN.md)]

---

## 特性

-   在 `Windows x86/Windows x64/Linux/macOS` 环境上对任意 Python 项目添加对 js 代码的支持
-   支持 `es6语法`, `记忆上下文环境变量`, `console.log`
-   拥有 `异常处理方法`, `包含错误的调用栈`

---

## 应用接口

```python
# 1. 实例方法
"""
* (1.1 推荐的方法) 运行 js 脚本代码，返回字符串结果(可能是 "null"/"undefined")
* @param script: 要运行的 js 脚本代码
"""
run(script: str): str

# (1.2 帮助开发的方法):
"""
* 转换代码字符串为一个 js 值，这个值也是 python 模块的基本 ctypes 数据类型, 一般的 python 方法不能直接处理
* @param code: js 脚本代码
"""
getJValue(code: str): ctypes._SimpleCData

"""
* 执行一个 js 函数，返回从 ctypes 数据转换的字符串
* @param funName: 表示 js 函数名字的字符串
* @param code_arguments: 表示 js 函数中 js 值参数的字符串序列, 可能为空
"""
callFunction(funName: str, *code_arguments: str): str

"""
* 执行一个 js 函数，返回从 ctypes 数据转换的 JSON 格式字符串
* @param funName: 表示 js 函数名字的字符串
* @param code_arguments: 表示 js 函数中 js 值参数的字符串序列, 可能为空
"""
callFunctionToJson(funName: str, *code_arguments: str): JSON str

"""
* 绑定一个 C 语言函数到一个 js 函数
* @param nativeFunction: C 可执行函数在 js 函数被执行时调用, 它由 ctypes.CFUNCTYPE 对 python 函数包裹得到
* @param funName: 表示函数名字的字符串
* @param callbackState: 用户提供的会传回给回调函数的状态
"""
registerMethod(nativeFunction: Any, funName: str, callbackState?: ctypes._SimpleCData): None

# 2. 静态方法
"""
* 获得 js 值的 JavaScript 类型, 来自本模块枚举类 JsValueType 的名字
* @param jValue: 一个 js 值
"""
getValueType(jValue: ctypes._SimpleCData): str

"""
* 从一个 js 值获得 python 数字值
* @param jValue: 一个 js 值
"""
jValueToNativeInt(jValue: ctypes._SimpleCData): int

"""
* 从一个 js 值获得 python 字符串值
* @param jValue: 一个 js 值
"""
jValueToNativeStr(jValue: ctypes._SimpleCData): str

"""
* 获得与一个名字关联的属性标识符
* @param name: 所获得或建立属性标识符的名字，名字可包含纯数字
"""
getPropertyIdFromName(name: str): ctypes._SimpleCData

"""
* 获得一个对象的属性
* @param jObj: 一个有属性的 js 对象
* @param str_propertyId: 属性标识符的字符串名字
"""
jGetProperty(jObj: ctypes._SimpleCData, str_propertyId: str): ctypes._SimpleCData

"""
* 设置一个对象的属性，返回表示操作成功失败的数字代码
* @param jObj: 一个有属性的 js 对象
* @param str_propertyId: 属性标识符的字符串名字
* @param jValue: 属性新的值
* @param useStrictRules: 属性设置是否跟随严格模式规则
"""
jSetProperty(jObj: ctypes._SimpleCData, str_propertyId: str, jValue: ctypes._SimpleCData, useStrictRules: bool): int
```

### [[特性](#特性)|[应用接口](#应用接口)|[使用](#使用)|[配置](#配置)|[依赖](#依赖)|[CHANGELOG.md](CHANGELOG.md)]

## 使用

以 `python -m pip install pyChakraCore` 在 pip 安装项目之后

```python
>>> from pyChakraCore import pyChakraCore
>>> vm=pyChakraCore()
>>> jscode = "console.log('run: typeof 1 is', typeof 1)"
>>> vm.run(jscode)
run: typeof 1 is number
```

## 配置

-   项目文件夹下 windowsx86/windowsx64/linux/osx 文件夹里存放依赖库，即 [ChakraCore](https://github.com/chakra-core/ChakraCore) （版本1.11.20）发布的 .dll/.so/.dylib 文件

---

## 依赖

-   [python](https://www.python.org/) 3.4 或以上
