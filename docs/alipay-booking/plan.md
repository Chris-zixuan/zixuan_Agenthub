# 支付宝交易流水记账 Skill 实现计划

> **For agentic workers:** 使用 subagent-driven-development 或 executing-plans 按任务执行。步骤使用 checkbox (`- [ ]`) 语法追踪。

**Goal:** 建立一个 skill，将支付宝 CSV 交易明细按照用户自定义映射规则自动填充到随手记模板中

**Architecture:** `init_template.py` 完成一次性初始化（转换 xls→xlsx 并创建映射 sheet），`process_alipay.py` 作为核心处理脚本读取 CSV + 映射配置，生成填充好的输出 xlsx。Skill 的 SKILL.md 指导 Claude 如何调用这两个脚本。

**Tech Stack:** Python 3, openpyxl, xlrd, csv

---

### Task 1: 创建 template.xlsx（初始化脚本）

**Files:**
- Create: `d:/OneDrive/Desktop/新建文件夹/init_template.py`

- [ ] **Step 1: 编写 init_template.py**

```python
"""一次性脚本：将 template.xls 转为 template.xlsx，并添加分类映射和账户映射 sheet。

用法：python init_template.py
输出：template.xlsx（与 template.xls 同级目录）
"""

import sys
import os
import xlrd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

def convert_xls_to_xlsx(xls_path, xlsx_path):
    """将 xls 的 3 个 sheet 复制到新的 xlsx 文件中。"""
    xls_book = xlrd.open_workbook(xls_path, formatting_info=True)
    xlsx_book = Workbook()
    xlsx_book.remove(xlsx_book.active)

    for sheet in xls_book.sheets():
        ws = xlsx_book.create_sheet(title=sheet.name)
        for r in range(sheet.nrows):
            for c in range(sheet.ncols):
                cell = sheet.cell(r, c)
                new_cell = ws.cell(row=r + 1, column=c + 1, value=cell.value)
                # 保留日期格式等简单格式
                if cell.ctype == 3 and cell.value:
                    new_cell.number_format = 'YYYY-MM-DD HH:MM:SS'

    return xlsx_book


def add_mapping_sheets(xlsx_book):
    """添加分类映射 sheet 和账户映射 sheet。"""
    header_font = Font(bold=True, size=11)
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    header_align = Alignment(horizontal="center")

    # --- 分类映射 ---
    categories = [
        "餐饮美食", "日用百货", "医疗健康", "退款", "收入",
        "投资理财", "文化休闲", "交通出行", "数码电器",
        "家居家装", "生活服务", "商业服务", "爱车养车",
        "亲友代付", "服饰装扮", "住房物业", "运动户外",
        "充值缴费", "信用借还", "转账红包", "其他",
    ]

    ws_cat = xlsx_book.create_sheet(title="分类映射")
    ws_cat.cell(row=1, column=1, value="CSV交易分类").font = header_font
    ws_cat.cell(row=1, column=1).fill = header_fill
    ws_cat.cell(row=1, column=1).alignment = header_align
    ws_cat.cell(row=1, column=2, value="一级分类").font = header_font
    ws_cat.cell(row=1, column=2).fill = header_fill
    ws_cat.cell(row=1, column=3, value="二级分类").font = header_font
    ws_cat.cell(row=1, column=3).fill = header_fill

    for i, cat in enumerate(categories):
        ws_cat.cell(row=i + 2, column=1, value=cat)
    ws_cat.column_dimensions['A'].width = 16
    ws_cat.column_dimensions['B'].width = 14
    ws_cat.column_dimensions['C'].width = 14

    # --- 账户映射 ---
    payment_methods = [
        "账户余额", "余额宝", "账户余额(个人余额)",
        "招商银行储蓄卡(XXXX)", "招商银行信用卡(XXXX)",
        "账户余额&红包", "账户余额&碰友日立减",
        "账户余额&优惠", "账户余额&焕新折扣",
        "账户余额&企业码员工优惠",
        "支付宝小荷包(XXX)&红包",
        "(空)",
    ]

    ws_acc = xlsx_book.create_sheet(title="账户映射")
    ws_acc.cell(row=1, column=1, value="CSV支付方式").font = header_font
    ws_acc.cell(row=1, column=1).fill = header_fill
    ws_acc.cell(row=1, column=1).alignment = header_align
    ws_acc.cell(row=1, column=2, value="你的账户名").font = header_font
    ws_acc.cell(row=1, column=2).fill = header_fill

    for i, method in enumerate(payment_methods):
        ws_acc.cell(row=i + 2, column=1, value=method)
    ws_acc.column_dimensions['A'].width = 30
    ws_acc.column_dimensions['B'].width = 20

    return xlsx_book


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    xls_path = os.path.join(base_dir, "template.xls")
    xlsx_path = os.path.join(base_dir, "template.xlsx")

    if not os.path.exists(xls_path):
        print(f"错误：找不到 {xls_path}")
        sys.exit(1)

    print("转换 template.xls → template.xlsx ...")
    book = convert_xls_to_xlsx(xls_path, xlsx_path)

    print("添加分类映射 + 账户映射 sheet ...")
    book = add_mapping_sheets(book)

    # 把映射 sheet 排到最后
    sheet_order = ["支出", "收入", "转账", "分类映射", "账户映射"]
    for i, name in enumerate(sheet_order):
        if name in book.sheetnames:
            ws = book[name]
            book.move_sheet(ws, offset=i - book.sheetnames.index(name))

    book.save(xlsx_path)
    print(f"完成！已生成：{xlsx_path}")
    print("下一步：用 Excel 打开 template.xlsx，填写「分类映射」和「账户映射」sheet 中的空列。")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 运行初始化脚本**

```bash
cd "d:/OneDrive/Desktop/新建文件夹" && python3 init_template.py
```

- [ ] **Step 3: 验证生成结果**

```bash
cd "d:/OneDrive/Desktop/新建文件夹" && python3 -c "
from openpyxl import load_workbook
wb = load_workbook('template.xlsx')
print('Sheet 列表:', wb.sheetnames)
for name in wb.sheetnames:
    ws = wb[name]
    print(f'  {name}: {ws.max_row} rows x {ws.max_column} cols')
"
```

预期输出：5 个 sheet，分类映射 22 行（1 表头 + 21 分类），账户映射 13 行（1 表头 + 12 支付方式）

---

### Task 2: 编写核心处理脚本 process_alipay.py

**Files:**
- Create: `d:/OneDrive/Desktop/新建文件夹/process_alipay.py`

- [ ] **Step 1: 编写 CSV 解析函数**

```python
"""支付宝交易流水处理脚本。

读取支付宝 CSV 和用户模板，按映射规则生成记账用 Excel 文件。
用法（通过 skill 调用）：python process_alipay.py <工作目录>
"""

import csv
import os
import sys
import re
import glob
from datetime import datetime
from copy import copy
from openpyxl import load_workbook

# 忽略阈值：投资理财收益低于此金额不记录
IGNORE_THRESHOLD = 0.05


def find_latest_csv(directory):
    """在目录中找最新的支付宝交易明细 CSV 文件。"""
    pattern = os.path.join(directory, "支付宝交易明细*.csv")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"在 {directory} 中找不到支付宝交易明细 CSV 文件")
    return max(files, key=os.path.getmtime)


def parse_csv(csv_path):
    """解析支付宝 CSV，返回记录列表。

    每条记录为 dict: {交易时间, 交易分类, 交易对方, 对方账号, 商品说明, 收/支, 金额, 收/付款方式, 交易状态, 交易订单号, 商家订单号, 备注}
    金额转换为 float。
    """
    records = []
    with open(csv_path, encoding="gbk") as f:
        lines = f.readlines()

    if len(lines) < 25:
        return records

    header_line = lines[23].strip().rstrip(",")
    headers = header_line.split(",")

    for line in lines[24:]:
        line = line.strip()
        if not line:
            continue

        # 处理制表符分隔的订单号字段
        line = line.replace("\t", ",")
        parts = line.split(",")
        if len(parts) < len(headers):
            continue

        record = {}
        for i, h in enumerate(headers):
            record[h] = parts[i].strip() if i < len(parts) else ""

        try:
            # CSV 金额可能带千分位逗号
            amount_str = record.get("金额", "0").replace(",", "").strip()
            record["金额"] = float(amount_str) if amount_str else 0.0
        except ValueError:
            record["金额"] = 0.0

        records.append(record)

    return records


def should_ignore(record):
    """判断记录是否应被忽略。"""
    status = record.get("交易状态", "")
    category = record.get("交易分类", "")
    pay_type = record.get("收/支", "")
    amount = record["金额"]

    # 投资理财收益 ≤ 0.04 忽略
    if pay_type == "不计收支" and "投资理财" in category and amount <= IGNORE_THRESHOLD:
        return True

    # 交易关闭的不计收支记录忽略
    if pay_type == "不计收支" and "关闭" in status:
        return True

    return False


def is_refund(record):
    """判断是否为退款。"""
    status = record.get("交易状态", "")
    category = record.get("交易分类", "")
    return "退款" in category or "退款" in status


def normalize_payment_method(method):
    """归一化支付方式——组合支付时取主账户。"""
    if not method:
        return "(空)"
    if "&" in method:
        return method.split("&")[0].strip()
    return method
```

- [ ] **Step 2: 编写映射加载和主处理逻辑**

```python
def load_mappings(template_path):
    """从 template.xlsx 加载分类映射和账户映射。

    返回: (category_map, account_map)
      category_map: {CSV交易分类: (一级分类, 二级分类)}
      account_map:  {CSV支付方式: 你的账户名}
    """
    wb = load_workbook(template_path, data_only=True)
    category_map = {}
    account_map = {}

    if "分类映射" in wb.sheetnames:
        ws = wb["分类映射"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            csv_cat = (row[0] or "").strip()
            level1 = (row[1] or "").strip()
            level2 = (row[2] or "").strip()
            if csv_cat:
                category_map[csv_cat] = (level1, level2)

    if "账户映射" in wb.sheetnames:
        ws = wb["账户映射"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            csv_method = (row[0] or "").strip()
            user_account = (row[1] or "").strip()
            if csv_method:
                account_map[csv_method] = user_account or csv_method  # 未填则用原值

    wb.close()
    return category_map, account_map


def process_records(records, category_map, account_map):
    """将原始记录分类处理为 支出/收入/转账 三个列表。

    支出记录字段:(交易类型, 日期, 一级分类, 二级分类, 支付账户, 金额, 成员, 商家, 项目, 备注)
    收入记录字段:(交易类型, 日期, 一级分类, 二级分类, 收入账户, 金额, 成员, 商家, 项目, 备注)
    转账记录字段:(交易类型, 日期, 转出账户, 转入账户, 金额, 成员, 商家, 项目, 备注)
    """
    expenses = []
    incomes = []
    transfers = []

    for rec in records:
        if should_ignore(rec):
            continue

        pay_type = rec.get("收/支", "")
        csv_cat = rec.get("交易分类", "")
        csv_method = rec.get("收/付款方式", "")
        status = rec.get("交易状态", "")

        date_str = rec.get("交易时间", "")
        counterparty = rec.get("交易对方", "")
        description = rec.get("商品说明", "")
        amount = rec["金额"]

        l1, l2 = category_map.get(csv_cat, ("", ""))
        normalized_method = normalize_payment_method(csv_method)
        account = account_map.get(normalized_method, normalized_method)
        note = f"{counterparty} {description}".strip()

        if pay_type == "支出" or (pay_type == "不计收支" and is_refund(rec)):
            # 退款金额取负
            final_amount = -amount if is_refund(rec) else amount
            expenses.append([
                csv_cat, date_str, l1, l2, account, final_amount,
                "", counterparty, "", note,
            ])

        elif pay_type == "收入":
            incomes.append([
                csv_cat, date_str, l1, l2, account, amount,
                "", counterparty, "", note,
            ])

        elif pay_type == "不计收支":
            # 不计收支的其余记录（如信用借还等），根据状态判断
            if "成功" not in status and "关闭" not in status:
                continue
            # 默认作为支出处理
            expenses.append([
                csv_cat, date_str, l1, l2, account, amount,
                "", counterparty, "", note,
            ])

    return expenses, incomes, transfers


def fill_output(expenses, incomes, transfers, template_xls_path, template_xlsx_path, output_path):
    """将处理好的数据填充到输出文件中。

    以 template.xls 为基础（复制其格式），然后写入数据。
    实际上我们用 template.xlsx 的格式，因为 openpyxl 不支持 .xls 写入。
    策略：从 template.xlsx 的 支出/收入/转账 sheet 获取表头和样式，重新写入。
    """
    # 加载 template.xlsx 作为格式参考
    ref_wb = load_workbook(template_xlsx_path)
    wb = load_workbook(template_xlsx_path)

    def fill_sheet(ws, data, column_count):
        """清空 sheet 的示例数据（保留表头），写入新数据。"""
        # 删除第 2 行到末尾的所有行
        if ws.max_row > 1:
            ws.delete_rows(2, ws.max_row - 1)
        for row_data in data:
            ws.append(row_data[:column_count])

    fill_sheet(wb["支出"], expenses, 10)
    fill_sheet(wb["收入"], incomes, 10)
    fill_sheet(wb["转账"], transfers, 9)

    # 删除映射 sheet（输出文件不需要这些配置）
    for s in ["分类映射", "账户映射"]:
        if s in wb.sheetnames:
            del wb[s]

    wb.save(output_path)
    wb.close()
    ref_wb.close()


def main():
    work_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    template_xls = os.path.join(work_dir, "template.xls")
    template_xlsx = os.path.join(work_dir, "template.xlsx")

    if not os.path.exists(template_xlsx):
        print(f"错误：找不到 template.xlsx，请先运行 init_template.py 初始化。")
        sys.exit(1)
    if not os.path.exists(template_xls):
        print(f"警告：找不到 template.xls（但 template.xlsx 存在，继续处理）")

    csv_path = find_latest_csv(work_dir)
    print(f"读取 CSV: {os.path.basename(csv_path)}")

    records = parse_csv(csv_path)
    print(f"解析 {len(records)} 条记录")

    category_map, account_map = load_mappings(template_xlsx)
    print(f"分类映射: {len(category_map)} 条规则")
    print(f"账户映射: {len(account_map)} 条规则")

    expenses, incomes, transfers = process_records(records, category_map, account_map)
    print(f"支出: {len(expenses)} 条, 收入: {len(incomes)} 条, 转账: {len(transfers)} 条")

    # 生成输出文件名
    dates = []
    for rec in records[:1]:
        ts = rec.get("交易时间", "")
        dates.append(ts[:10].replace("-", ""))
    date_prefix = dates[0] if dates else datetime.now().strftime("%Y%m%d")
    output_path = os.path.join(work_dir, f"输出-{date_prefix}.xlsx")

    fill_output(expenses, incomes, transfers, template_xls, template_xlsx, output_path)
    print(f"完成！输出：{output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 测试 CS 解析**

```bash
cd "d:/OneDrive/Desktop/新建文件夹" && python3 -c "
from process_alipay import parse_csv, find_latest_csv, should_ignore
import os, io

# 测试 CSV 解析
csv_path = find_latest_csv('.')
records = parse_csv(csv_path)
print(f'解析记录数: {len(records)}')
print(f'第一条: {records[0]}')
print(f'支出条数: {sum(1 for r in records if r.get(\"收/支\") == \"支出\")}')

# 测试忽略规则
for r in records:
    if '投资理财' in r.get('交易分类', ''):
        print(f'  投资: 金额={r[\"金额\"]}, 忽略={should_ignore(r)}')
        break
"
```

- [ ] **Step 4: 完整运行一次处理脚本**

```bash
cd "d:/OneDrive/Desktop/新建文件夹" && python3 process_alipay.py "d:/OneDrive/Desktop/新建文件夹"
```

---

### Task 3: 编写 Skill 的 SKILL.md

**Files:**
- Create: `C:/Users/yangz/.claude/skills/alipay-booking/SKILL.md`

- [ ] **Step 1: 创建 skill 目录和 SKILL.md**

首先创建目录：
```bash
mkdir -p "C:/Users/yangz/.claude/skills/alipay-booking"
```

然后编写 SKILL.md：

```markdown
---
name: alipay-booking
description: 将支付宝交易流水 CSV 导入随手记模板，生成可直接导入记账网站的 Excel 文件
---

# 支付宝流水记账

## 概述

将支付宝导出的 CSV 交易明细，按照用户自定义的分类和账户映射规则，自动填充到随手记模板中。

## 工作目录

处理脚本和模板文件均在用户的项目目录中（通常是 `~/Desktop/新建文件夹/` 或类似路径）。
先确认工作目录位置，再执行后续步骤。

## 前置条件

运行时检查以下文件是否存在：
- `template.xlsx` — 工作模板（含分类映射和账户映射 sheet）。如果不存在，运行 `python init_template.py` 初始化。
- `template.xls` — 原始模板（记账网站格式），只读不写。如果不存在，发出警告但继续。
- `支付宝交易明细*.csv` — 支付宝导出的交易数据（GBK 编码）

## 处理流程

1. 确认工作目录中有 `支付宝交易明细*.csv` 文件（取最新一个）
2. 确认 `template.xlsx` 存在且用户已填写映射规则
3. 运行 `python process_alipay.py <工作目录>`
4. 检查输出文件 `输出-YYYYMMDD.xlsx`，告知用户处理结果

## 用户需要手动维护的内容

在 `template.xlsx` 的以下 sheet 中填写映射：
- **分类映射** sheet：CSV 交易分类 → 一级分类 / 二级分类
- **账户映射** sheet：CSV 支付方式 → 你的账户名

映射规则只需填写一次，新增交易类别时补充即可。

## 处理规则说明

- 退款自动转为负数填入支出 sheet
- 投资理财收益 ≤ 0.04 元自动忽略
- 交易关闭的不计收支记录自动忽略
- 组合支付（如 `账户余额&红包`）自动取主账户
- CSV 中找不到映射分类的记录，分类留空
- 输出文件命名为 `输出-YYYYMMDD.xlsx`，不覆盖模板文件
```

---

### Task 4: 更新 CLAUDE.md

**Files:**
- Modify: `d:/OneDrive/Desktop/新建文件夹/CLAUDE.md`

- [ ] **Step 1: 更新 CLAUDE.md，加入 skill 和脚本说明**

读取当前的 CLAUDE.md，在其末尾追加以下内容：

```markdown
## 支付宝记账 Skill

当用户需要将支付宝 CSV 导入随手记模板时，使用 `alipay-booking` skill（通过 `/alipay-booking` 调用）。

### 手动操作

- **初始化模板**：`python init_template.py`（只需运行一次，生成 template.xlsx）
- **执行处理**：`python process_alipay.py .`
- **映射配置**：在 template.xlsx 的「分类映射」和「账户映射」sheet 中填写
```

---

### Task 5: 端到端验证

- [ ] **Step 1: 清空测试状态（如果已有输出文件）**

```bash
rm -f "d:/OneDrive/Desktop/新建文件夹/输出-"*.xlsx
```

- [ ] **Step 2: 运行完整流程**

```bash
cd "d:/OneDrive/Desktop/新建文件夹" && python3 process_alipay.py .
```

- [ ] **Step 3: 验证输出文件**

```bash
cd "d:/OneDrive/Desktop/新建文件夹" && python3 -c "
from openpyxl import load_workbook
import glob
files = glob.glob('输出-*.xlsx')
if files:
    wb = load_workbook(files[0])
    print(f'文件: {files[0]}')
    for name in wb.sheetnames:
        ws = wb[name]
        print(f'  {name}: {ws.max_row} 行 x {ws.max_column} 列')
        if ws.max_row > 1:
            # 打印第一行数据和最后一行数据
            row2 = [str(ws.cell(row=2, column=c).value) for c in range(1, ws.max_column + 1)]
            print(f'    第一行: {row2}')
else:
    print('未找到输出文件')
"
```

预期：3 个 sheet（支出、收入、转账），支出行数 ≈ 177（含退款的负数行），收入 ≈ 11

---

## 文件总览

| 文件 | 用途 |
|------|------|
| `template.xls` | 原始模板，只读 |
| `template.xlsx` | 工作模板，含映射配置 |
| `init_template.py` | 一次性初始化脚本 |
| `process_alipay.py` | 核心处理脚本 |
| `输出-YYYYMMDD.xlsx` | 生成的记账文件 |
| `skills/alipay-booking/SKILL.md` | Skill 定义 |
