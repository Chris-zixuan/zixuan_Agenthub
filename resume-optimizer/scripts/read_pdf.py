#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历PDF文档读取脚本（使用 pdfplumber 库）
功能：读取 .pdf 文件，提取文本内容
用法：python read_pdf.py <input_file.pdf> [output_file.txt]
      python read_pdf.py <input_file.pdf> --json [output_file.json]

依赖：pdfplumber 库
"""

import sys
import os
import re
import json


def parse_pdf(file_path):
    """
    读取PDF文档内容，返回纯文本和结构化数据
    支持文本型PDF格式（使用 pdfplumber 库）
    """
    if not os.path.exists(file_path):
        return {"success": False, "error": f"文件不存在: {file_path}", "content": ""}
    
    if not file_path.lower().endswith('.pdf'):
        return {"success": False, "error": "仅支持 .pdf 格式", "content": ""}
    
    try:
        import pdfplumber
        
        with pdfplumber.open(file_path) as pdf:
            pages_content = []
            
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_content.append(text)
            
            full_content = '\n\n'.join(pages_content)
            
            return {
                "success": True,
                "error": "",
                "content": full_content.strip(),
                "structure": {
                    "basic_info": [],
                    "education": [],
                    "work_experience": [],
                    "projects": [],
                    "skills": [],
                    "certificates": [],
                    "others": []
                },
                "stats": {
                    "pages": len(pdf.pages),
                    "characters": len(full_content)
                }
            }
    
    except ImportError:
        return {"success": False, "error": "未安装 pdfplumber 库，请运行: pip install pdfplumber", "content": ""}
    except Exception as e:
        return {"success": False, "error": f"解析PDF时出错: {str(e)}", "content": ""}


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
        print("用法：python read_pdf.py <input_file.pdf> [output_file.txt]")
        print("      python read_pdf.py <input_file.pdf> --json [output_file.json]")
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
    output_file = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--json':
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                output_file = sys.argv[i + 1]
            break
        elif i == 2 and not arg.startswith('--'):
            output_file = arg
    
    result = parse_pdf(resolved_input_file)
    
    if not result["success"]:
        print(f"错误：{result['error']}", file=sys.stderr)
        sys.exit(1)
    
    if output_json:
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
