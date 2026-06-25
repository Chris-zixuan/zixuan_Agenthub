# Python 脚本参考文件说明

本目录保留 Python 脚本的规则文档、数据结构定义和运行时框架代码。

## 文件说明

| 文件 | 用途 |
|------|------|
| [ScriptPythonRules.md](./ScriptPythonRules.md) | Python 脚本开发规则，含完整 5 步代码生成工作流、类型映射表、默认模板 |
| [Script.pyDataStruct.py](./Script.pyDataStruct.py) | Python 数据结构定义（Point、Circle、RoiBox、Line、ImageData 等） |
| [Script.ioHelper.py](./Script.ioHelper.py) | IoHelper 变量管理框架（运行时库），含类型映射、变量校验、GetValue/SetValue 辅助方法 |

## 检索优先级

1. **ScriptPythonRules.md** — 确认开发规则、5 步工作流、类型映射 `dict_type`、默认模板
2. **Script.pyDataStruct.py** — 确认 Python 数据结构类的字段名和类型
3. **Script.ioHelper.py** — 了解 IoHelper 框架运行时行为、类型校验方法和内部数据流

## 检索原则

- 所有变量读写通过 `IoHelper` 框架，业务代码仅使用 `moduleVar`
- 输入变量一律按数组处理（即使 VM 中声明为标量类型）
- `dict_type` 字典为类型映射的权威来源，代码生成时必须严格遵守
- 字段名使用 snake_case 风格（如 `center_x`、`point_x`），来自 VM 底层映射约定
- 类名使用 PascalCase 风格（如 `RoiBox`、`ImageData`）

## 补充说明

- `IoHelper` 通过动态生成 `exec()` 代码完成变量初始化（`initVar`）、回写（`updateVar`）和清理（`clearVar`）
- `PrintMsg()` 将调试信息输出到 VM 脚本编辑界面，`DebugMsg()` 输出到 DebugView（需 `debug_print = True`）
- 模板中 `globalVar` / `localVar` 的初始化是框架惯例，业务逻辑不应使用它们读写变量
- `ANNULUS` 类型在 `dict_type` 中映射到 `RoiAnnulus`（复用圆环结构体）
