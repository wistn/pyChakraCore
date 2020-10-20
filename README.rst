js虚拟机ChakraCore（版本1.11.20）的python版封装。本py项目可在 windowsx86、windowsx64(未测试)、linux(未测试)、osx 环境运行，已包含[ChakraCore](https://github.com/Microsoft/ChakraCore/releases)发布的 .dll/.so/.dylib 依赖库文件。优点：支持es6语法、记忆上下文环境变量、console.log、有异常处理机制和错误的调用栈。


本库的主要命令 run 即可得到字符串格式结果

```py
from pyChakraCore import pyChakraCore
vm=pyChakraCore()
print(vm.run("js代码字符串"))
```