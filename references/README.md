# VisionMaster 接口检索说明

本目录保留原始 C# 参考文件，同时补充适合 Claude 检索的说明。

## 使用优先级

1. 先看 [Script.Interface.cs](./Script.Interface.cs)：确认接口名、参数顺序、返回值、`ref` / `out`
2. 再看 [Script.DataStruct.cs](./Script.DataStruct.cs)：确认数据结构字段名和字段类型
3. 最后看 [Script.referenceMethods.md](./Script.referenceMethods.md)：快速定位常见模式、易错点和推荐写法

## 检索原则

- 以原始 `.cs` 文件为准，不要自行修正大小写
- 如果 `Get` / `Set` 接口返回 `int`，则 `0` 表示成功，非 `0` 表示异常
- `GetXxxArrayValue` 通常使用 `ref 数组 + out 个数`
- `SetXxxArrayValue` 通常使用 `(key, valueArray, index, len)`
- `SetXxxValueByIndex` 通常使用 `(key, value, index, total)`
- `GetIMAGEValue` 与 `SetImageValue` 大小写不对称，不能写错

## 当前目录文件

- [Script.Interface.cs](./Script.Interface.cs)：接口定义
- [Script.DataStruct.cs](./Script.DataStruct.cs)：数据结构定义
- [Script.referenceMethods.md](./Script.referenceMethods.md)：面向 Claude 的速查说明
