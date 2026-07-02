# VisionMaster 脚本示例与参考

## C# 脚本（[csharp/](csharp/)）

### 完整脚本示例

| 文件 | 说明 |
|------|------|
| [01-basic-template.cs](csharp/01-basic-template.cs) | 基础脚本模板 — Init/Process/Dispose 生命周期、数据读写、全局变量、模块控制 |
| [02-canny-edge-detection.cs](csharp/02-canny-edge-detection.cs) | OpenCV 图像处理 — Canny 边缘检测、ImageData↔Mat 转换、轮廓查找 |
| [03-roi.cs](csharp/03-roi.cs) | ROI 网格分割 — ROIBOX 数据处理、网格划分逻辑 |
| [04-trans-CAD-file.cs](csharp/04-trans-CAD-file.cs) | CAD 文件转换 — DXF 文件加载与 PNG 渲染 |
| [05-stereo-depth-pointcloud.cs](csharp/05-stereo-depth-pointcloud.cs) | 3D 深度图转点云 — StereoImageData 逐行提取、物理坐标转换 |

### 代码生成参考

| 文件 | 说明 |
|------|------|
| [interface-quickref.md](csharp/interface-quickref.md) | 变量类型映射 + 接口速查索引 — 确认类型和接口时查阅 |
| [code-patterns.md](csharp/code-patterns.md) | 代码模式库（14 种场景模板） — 按场景匹配代码片段 |

## Python 脚本（[python/](python/)）

| 文件 | 说明 |
|------|------|
| [01-template.py](python/01-template.py) | Python 脚本模板 — IoHelper 框架、变量生命周期、try-except 结构 |

## 使用方式

### 人工使用

1. 复制对应语言的模板到 VM 脚本编辑器
2. 根据需求修改输入输出变量名和业务逻辑
3. C#：点击**预编译**检查语法，点击**执行**测试功能

### Agent 代码生成

生成脚本前，按语言路径查找参考：

**C# 脚本：**

1. **确认类型映射** → 查阅 [interface-quickref.md](csharp/interface-quickref.md) 第 1 节
2. **匹配代码模式** → 查阅 [code-patterns.md](csharp/code-patterns.md) 中的 14 种模式
3. **参考完整示例** → 选择场景相近的 `.cs` 文件作为代码骨架
4. **组合与调整** → 根据用户实际的 `UserProperty.cs` 替换变量名和类型

**Python 脚本：**

1. **确认数据结构** → 查阅 [ScriptPythonRules.md](../references_py/ScriptPythonRules.md) 中的类型映射
2. **参考模板** → 以 [01-template.py](python/01-template.py) 为骨架
3. **组合与调整** → 根据输入输出变量名和业务逻辑修改
