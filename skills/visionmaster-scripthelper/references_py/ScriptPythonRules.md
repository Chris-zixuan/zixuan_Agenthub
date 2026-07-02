
# 明确不支持

遇到以下请求时，直接说明不支持，避免继续展开：

- 控制器 IO 发送
- 全局变量的读写操作
- 界面层操作 / UI 自动化

# 变量输入与输出

读写输入输出变量的方式如下：

- 输入变量为只读，无法修改。假设输入变量名为in0，类型为int，可通过tmp = moduleVar.in0读取该变量的值。

- 输出变量为只写，无法读取。 假设输出变量名为out0，类型为int，可通过moduleVar.out = 9设置该变量的值。

变量都要先采用构建变量列表，然后赋值的架构形式。例如

```python
    #创建空列表
    matchPointX = []
    matchPointY = []
    #输入变量赋值到列表
    matchPointX = moduleVar.in0
    matchPointY = moduleVar.in1
```

## 结构体的定义和解析

python脚本的结构体定义参考文件[Script.pyDataStruct.py](./Script.pyDataStruct.py)

# 默认python脚本模板

```python
# coding: utf-8
import sys
from ioHelper import *


def Process(data) -> int:

    moduleVar = IoHelper(data, INIT_MODULE_VAR)
    globalVar = IoHelper(data, INIT_GLOBAL_VAR)
    localVar = IoHelper(data, INIT_LOCAL_VAR)


    try:
        
    except BaseException as e:
        PrintMsg(e)
    return 0

```

所有的脚本代码都要在模板代码的框架内，写在try-except 语句中。
可参考示例代码[python-template](../examples/python/01-template.py)
代码中ioHelper的定义在[ioHelper.py](./Script.ioHelper.py)

# 代码生成工作流

当用户请求生成、修改、补全脚本代码时，**严格按以下步骤执行**。

## 1. 向用户询问输入变量的变量名与结构

明确向用户提问得到所有的输入变量的变量名称和数据结构。
让用户以 in0,int;in1,float  这样的结构进行输入，将这个结构发送给用户进行提示。
当用户输入“完毕”时，开始进行下一步。

## 2. 向用户询问要输出变量的变量名与结构

明确向用户提问得到所有的输出变量的变量名称和数据结构。
让用户以 out0,int;out1,float  这样的结构进行输入，将这个结构发送给用户进行提示。
当用户输入“完毕”时，开始进行下一步。

## 3. 分析用户输入和输出的数据需求

根据数据结构定义的文档，来分析输入输出的变量类型和信息。
并且要注意到，用户输入的都不是数组类型，但是默认要映射为数组类型。
赋值时要严格按照要求，先定义数组再赋值的方式进行赋值。

```python
# 算法平台变量类型到Python变量类型的映射
dict_type = {'int': "int", 
             'int[]': "int",
             'float': "float", 
             'float[]': "float",
             'string': "str",
             'string[]': "str", 
             'byte': "bytes",
             'IMAGE': "ImageData",
             'ROIBOX': "RoiBox",
             'ROIANNULUS': "RoiAnnulus",
             'ROIPOLYGON': "RoiPolygon",
             'POINT': "Point",
             'LINE': "Line", 
             'FIXTURE':"Fixture",
             'CIRCLE': "Circle",
             'ANNULUS': "RoiAnnulus",
             'Rect': "Rect",
             'ELLIPSE': "ELLIPSE", 
             'pointset': "PointSet"}
```

## 4. 确认用户需求

自检脚本的变量输入输出，如果有疑问则向用户确认，
如果没有，则根据输入输出的变量名称，推测用户目的，询问用户脚本编写的需求和目的。
得到回复后，完成脚本的编写。

1. 脚本编写应当清晰无歧义
2. 做好脚本的缩进规范
3. 做到高内聚低耦合，用到的方法如果有必要应该封装为独立函数。
4. 注释清晰明了

## 5. 完成脚本的编写

对脚本的输出做一次检查，包括格式化、缩进等。最终向用户输出完整的python代码。

---

## 命名约定说明

Python 数据结构定义中的命名风格来自 VM 底层 C++ 到 Python 的映射约定，与 PEP 8 存在偏差：

- **字段名**使用 snake_case（如 `center_x`、`point_x`、`start_point_x`），直接映射自 VM 内部字段名
- **类名**使用 PascalCase（如 `RoiBox`、`ImageData`、`PointSet`），与 VM C# 侧类型名保持一致
- `ELLIPSE` 类名全大写是历史遗留，在 `dict_type` 中对应 `"ELLIPSE"` 键，代码中引用时需保持一致

编写脚本时请遵循以上约定，不要自行"修正"为 PEP 8 风格，否则会导致类型映射失败。
