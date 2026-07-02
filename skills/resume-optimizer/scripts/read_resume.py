#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历文档读取脚本（统一入口）
功能：自动识别并读取 .docx 和 .pdf 格式的简历文件
用法：python read_resume.py <input_file> [output_file.txt]
      python read_resume.py <input_file> --json [output_file.json]
      python read_resume.py <input_file> --structure [output_file.json]

支持格式：
- .docx（使用 python-docx 库）
- .pdf（使用 pdfplumber 库，仅支持文本型PDF）
"""

import sys
import os
import json


def read_docx(file_path):
    """调用 read_docx.py 的解析功能"""
    from read_docx import parse_docx
    return parse_docx(file_path)


def read_pdf(file_path):
    """调用 read_pdf.py 的解析功能"""
    from read_pdf import parse_pdf
    return parse_pdf(file_path)


def detect_and_parse(file_path):
    """根据文件扩展名自动选择解析器"""
    if not os.path.exists(file_path):
        return {"success": False, "error": f"文件不存在: {file_path}", "content": ""}
    
    lower_path = file_path.lower()
    
    if lower_path.endswith('.docx'):
        return read_docx(file_path)
    elif lower_path.endswith('.pdf'):
        return read_pdf(file_path)
    else:
        return {"success": False, "error": f"不支持的文件格式: {file_path}\n支持的格式: .docx, .pdf", "content": ""}


def find_input_file(file_name):
    """在多个位置查找输入文件：技能根目录的 input/、当前运行目录的 input/、当前目录"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root_dir = os.path.dirname(script_dir)
    
    if os.path.exists(file_name):
        return file_name
    
    input_path = os.path.join(skill_root_dir, "input", file_name)
    if os.path.exists(input_path):
        return input_path
    
    input_path = os.path.join("input", file_name)
    if os.path.exists(input_path):
        return input_path
    
    return None


def main():
    if len(sys.argv) < 2:
        print("用法：python read_resume.py <input_file> [output_file.txt]")
        print("      python read_resume.py <input_file> --json [output_file.json]")
        print("      python read_resume.py <input_file> --structure [output_file.json]")
        print("\n支持的文件格式：")
        print("  - .docx：Microsoft Word 文档")
        print("  - .pdf：PDF文档（仅支持文本型PDF，不支持扫描件）")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    resolved_input_file = find_input_file(input_file)
    if resolved_input_file is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_root_dir = os.path.dirname(script_dir)
        input_dir = os.path.join(skill_root_dir, "input")
        print(f"错误：找不到文件 '{input_file}'", file=sys.stderr)
        print(f"提示：请将文件放置在以下位置之一：", file=sys.stderr)
        print(f"  - 技能目录的 input/ 子目录：{input_dir}", file=sys.stderr)
        print(f"  - 当前运行目录的 input/ 子目录：{os.path.join(os.getcwd(), 'input')}", file=sys.stderr)
        print(f"  - 当前运行目录", file=sys.stderr)
        sys.exit(1)
    
    output_json = '--json' in sys.argv
    output_structure = '--structure' in sys.argv
    output_file = None
    
    for i, arg in enumerate(sys.argv):
        if arg in ('--json', '--structure'):
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                output_file = sys.argv[i + 1]
            break
        elif i == 2 and not arg.startswith('--'):
            output_file = arg
    
    result = detect_and_parse(resolved_input_file)
    
    if not result["success"]:
        print(f"错误：{result['error']}", file=sys.stderr)
        sys.exit(1)
    
    if output_json or output_structure:
        output_data = {
            "file": input_file,
            "content": result["content"],
            "structure": result["structure"],
            "stats": result["stats"]
        }
        json_str = json.dumps(output_data, ensure_ascii=False, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"JSON数据已保存到: {output_file}")
        else:
            print(json_str)
    else:
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result["content"])
            print(f"文本内容已保存到: {output_file}")
        else:
            print(result["content"])


if __name__ == "__main__":
    main()
