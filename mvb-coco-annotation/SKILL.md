---
name: mvb-coco-annotation
description: Use when given a directory containing only image files (.jpg/.jpeg/.png) and asked to generate MVB-COCO format annotation files for image classification. Applies when the user wants to auto-label, annotate, or create dataset.json/train.json and per-image JSON files from a folder of images.
---

# MVB-COCO 图像分类标注

## 概述

将一个只含图片的目录自动转换为完整的 MVB-COCO 格式分类数据集，包括主清单文件和每张图片的单独标注文件。

## 执行步骤

### 第一步：扫描目录，确认类别

1. 列出目录中所有图片文件（`.jpg`、`.jpeg`、`.png`）
2. **从文件名推断类别**：MVB 命名规范中，文件名通常包含类别名称（如 `1_Y1536423_xxx.jpg`）。若文件名含类别信息，直接提取；否则询问用户提供类别列表及每张图片对应的类别。
3. 确认类别列表（`id` 从 1 开始递增）

### 第二步：生成 per-image JSON

每张图片生成一个同名 JSON 文件（扩展名改为 `.json`），内容为单元素数组：

```json
[
  {
    "id": 1,
    "image_id": <图片id>,
    "category_id": <类别id>
  }
]
```

- `id` 固定为 `1`（每个文件只有一条标注）
- `image_id` 与主清单中该图片的 `id` 一致
- `category_id` 对应该图片所属类别

### 第三步：生成主清单 train.json / dataset.json

两个文件内容完全相同，结构如下：

```json
{
  "categories": [
    { "id": 1, "name": "类别A", "label_color": "#136dde19" },
    { "id": 2, "name": "类别B", "label_color": "#fb007219" }
  ],
  "images": [
    {
      "id": 1,
      "file_name": "1_类别B_xxx.jpg",
      "height": <像素高>,
      "width": <像素宽>,
      "image_type": "train",
      "labeled": true,
      "license": 1
    }
  ],
  "info": {
    "calib_type": 1,
    "contributor": "ai_train",
    "date_created": "<YYYY-MM-DD HH:MM:SS>",
    "description": "MVB_COCO格式数据集",
    "url": "MVBTORCH_TRAIN_DATA\\V4.0",
    "version": "1.1",
    "year": <当前年份>
  },
  "licenses": [
    { "id": 1, "name": "MVB License" }
  ]
}
```

**注意：** 主清单中 **不包含** `annotations` 数组，标注信息仅存于 per-image JSON 文件中。

### 第四步：获取图片尺寸

使用 Python 读取每张图片的实际宽高：

```python
from PIL import Image
import os

img_dir = r"<目录路径>"
for fname in sorted(os.listdir(img_dir)):
    if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        with Image.open(os.path.join(img_dir, fname)) as img:
            width, height = img.size
            print(fname, width, height)
```

若 PIL 不可用，可用 ImageMagick 的 `identify` 命令。

## 颜色分配规则

| 类别序号 | label_color |
|---------|-------------|
| 第 1 个类别 | `#136dde19`（蓝色系） |
| 第 2 个类别 | `#fb007219`（红色系） |
| 更多类别 | 可自行指定或沿用上述两色循环 |

## 文件命名规范

- per-image JSON 文件名与图片文件名完全一致，仅将扩展名替换为 `.json`
  - `1_Y1536423_ayan0.jpg` → `1_Y1536423_ayan0.json`
- 主清单固定命名为 `train.json` 和 `dataset.json`

## 从文件名自动推断类别

MVB 文件名格式通常为：`<序号>_<类别名>_<随机串>.jpg` 或 `<序号>_<类别名> (<编号>).jpg`

```python
import re
def extract_category(filename):
    m = re.match(r'^\d+_([^_\s(]+)', filename)
    return m.group(1) if m else None
```

## 常见错误

| 错误 | 解决方式 |
|------|---------|
| per-image JSON 中 `id` 写成图片序号 | 固定为 `1`，不是图片 id |
| 主清单包含 `annotations` 数组 | MVB 格式不在主清单中放标注，删除该字段 |
| 图片宽高填写顺序颠倒 | PIL 返回 `(width, height)`，JSON 字段顺序为 `height` 在前 |
| 两个主清单内容不同步 | `train.json` 和 `dataset.json` 必须完全相同 |
