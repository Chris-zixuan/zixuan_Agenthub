# VisionMaster 接口检索说明

本目录保留原始 C# 参考文件，用于确认接口签名、数据结构字段和类型转换细节。

> v2.5.0 起变量读写使用直接赋值范式，Get/Set 接口降级为遗留兼容（仅动态变量名访问时使用）。

## 文件说明

| 文件 | 用途 |
|------|------|
| [Script.Interface.cs](./Script.Interface.cs) | 脚本生命周期、全局变量、通信模块、流程模块和脚本基类接口定义 |
| [Script.DataStruct.cs](./Script.DataStruct.cs) | 几何形状、图像数据等数据结构定义 |
| [Script.ExMethods.cs](./Script.ExMethods.cs) | OpenCvSharp `Mat` / `System.Drawing.Bitmap` 与 `ImageData` 互转实现 |

## 检索优先级

1. **Script.Interface.cs** — 确认接口名、参数顺序、返回值、`ref` / `out`
2. **Script.DataStruct.cs** — 确认数据结构字段名和类型
3. **Script.ExMethods.cs** — 了解 `Mat` / `Bitmap` ↔ `ImageData` 的转换逻辑和像素格式处理

## 检索原则

- 以原始 `.cs` 文件为准，保持大小写精确
- `Get` / `Set` 遗留接口返回 `int` 时：`0` 表示成功，非 `0` 表示异常
- `GetXxxArrayValue` 通常使用 `ref 数组 + out count`
- `SetXxxArrayValue` 通常使用 `(key, valueArray, index, len)`
- `SetXxxValueByIndex` 通常使用 `(key, value, index, total)`
- 注意 `GetIMAGEValue` 与 `SetImageValue` 的大小写差异

## 补充说明

- `Script.ExMethods.cs` 中，`ImageDataToMat` 会根据 `ImagePixelFormate` 转换 RGB/BGR 并释放临时指针
- `Script.ExMethods.cs` 中，`BitmapToImageData` / `ImageDataToBitmap` 处理 `System.Drawing.Bitmap` 与 `ImageData` 的互转，自动处理 stride 对齐和 BGR/RGB 通道交换；支持 `Format8bppIndexed`（MONO8）和 `Format24bppRgb`（RGB24）两种像素格式
- `Script.DataStruct.cs` 定义了 `ImageData`、几何对象（Point/Circle/Rect/Line/Roibox）等核心数据结构
- 3D 相关数据结构（`PointCloudData` 等）已预留但暂不在 skill 支持范围内
