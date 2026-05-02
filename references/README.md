# VisionMaster 接口检索说明

本目录保留原始 C# 参考文件，帮助快速查找接口、数据结构和 OpenCvSharp 图像转换方案。

## 目录说明

- [Script.Interface.cs](./Script.Interface.cs)：脚本生命周期、全局变量、通信模块、流程模块和脚本基类接口定义
- [Script.DataStruct.cs](./Script.DataStruct.cs)：几何形状、图像数据、点云数据等数据结构定义
- [Script.ExMethods.cs](./Script.ExMethods.cs)：OpenCvSharp `Mat` 与 `ImageData` 互转实现
- `汽车框架/`：汽车行业相关框架参考
- `python-script/`：Python 脚本参考或示例

## 使用优先级

1. 先看 `Script.Interface.cs`：确认接口名、参数顺序、返回值、`ref` / `out`
2. 再看 `Script.DataStruct.cs`：确认数据结构字段名和类型
3. 最后看 `Script.ExMethods.cs`：了解 `Mat` ↔ `ImageData` 的转换逻辑和像素格式处理

## 检索原则

- 以原始 `.cs` 文件为准，保持大小写精确
- `Get` / `Set` 接口返回 `int` 时：`0` 表示成功，非 `0` 表示异常
- `GetXxxArrayValue` 通常使用 `ref 数组 + out count`
- `SetXxxArrayValue` 通常使用 `(key, valueArray, index, len)`
- `SetXxxValueByIndex` 通常使用 `(key, value, index, total)`
- 注意 `GetIMAGEValue` 与 `SetImageValue` 的大小写差异

## 说明补充

- 本目录当前没有 `Script.referenceMethods.md` 文件，已改为直接使用现有 `.cs` 文件进行检索
- `Script.ExMethods.cs` 示例中，`ImageDataToMat` 会根据 `ImagePixelFormate` 转换 RGB/BGR 并释放临时指针
- `Script.DataStruct.cs` 定义了包括 `ImageData`、`PointCloudData`、几何对象等在内的核心数据结构
