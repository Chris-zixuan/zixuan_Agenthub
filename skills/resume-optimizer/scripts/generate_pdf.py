#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历PDF生成脚本
功能：将MD简历转换为PDF（Windows平台使用Word COM对象）
用法：python generate_pdf.py <input.md> <output.pdf>

依赖：
- Windows：使用 Word COM 对象（需要安装 Microsoft Word）
- 其他平台：生成 HTML 文件供手动打印为 PDF
"""

import sys
import os
import platform


def md_to_html(md_content):
    """将Markdown内容转换为HTML"""
    import re
    
    html_parts = []
    
    html_parts.append('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>简历</title>
    <style>
        @page { size: A4; margin: 20mm 18mm; }
        body {
            font-family: "Microsoft YaHei", "PingFang SC", "SimSun", sans-serif;
            font-size: 10.5pt;
            line-height: 1.8;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 20px;
        }
        h1 {
            font-size: 18pt;
            font-weight: bold;
            color: #000;
            margin: 0 0 10px 0;
            text-align: left;
        }
        h2 {
            font-size: 12pt;
            font-weight: bold;
            color: #333;
            margin: 18px 0 10px 0;
            padding-bottom: 4px;
            border-bottom: 1px solid #ccc;
        }
        h3 {
            font-size: 11pt;
            font-weight: bold;
            color: #333;
            margin: 14px 0 6px 0;
        }
        p {
            margin: 6px 0;
            text-align: justify;
        }
        ul {
            margin: 6px 0;
            padding-left: 24px;
        }
        li {
            margin-bottom: 6px;
            line-height: 1.7;
        }
        .contact-info {
            font-size: 10pt;
            color: #555;
            margin: 4px 0;
        }
        .section-divider {
            border-top: 2px solid #ccc;
            margin: 14px 0;
        }
        .profile {
            background-color: #f9f9f9;
            padding: 10px;
            border-left: 3px solid #666;
            margin: 10px 0;
        }
    </style>
</head>
<body>
''')
    
    lines = md_content.split('\n')
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            continue
        
        # 处理标题
        if stripped.startswith('# ') and not stripped.startswith('##'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            title_text = stripped[2:]
            html_parts.append(f'<h1>{title_text}</h1>\n')
        elif stripped.startswith('## ') and not stripped.startswith('###'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            title_text = stripped[3:]
            html_parts.append(f'<h2>{title_text}</h2>\n')
        elif stripped.startswith('### '):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            title_text = stripped[4:]
            html_parts.append(f'<h3>{title_text}</h3>\n')
        elif stripped.startswith('---'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append('<div class="section-divider"></div>\n')
        elif stripped.startswith('- ') or stripped.startswith('* '):
            content = stripped[2:]
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            if not in_list:
                html_parts.append('<ul>\n')
                in_list = True
            html_parts.append(f'<li>{content}</li>\n')
        else:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            html_parts.append(f'<p>{content}</p>\n')
    
    if in_list:
        html_parts.append('</ul>')
    
    html_parts.append('</body>\n</html>')
    
    return ''.join(html_parts)


def generate_pdf_with_word(docx_file, pdf_file):
    """使用Word COM对象将docx转换为PDF（仅Windows）"""
    try:
        import win32com.client
        import pythoncom
        
        # 初始化COM
        pythoncom.CoInitialize()
        
        word = None
        try:
            word = win32com.client.Dispatch('Word.Application')
            word.Visible = False
            
            # 打开Word文档
            doc = word.Documents.Open(os.path.abspath(docx_file))
            
            # 保存为PDF
            doc.SaveAs(os.path.abspath(pdf_file), FileFormat=17)
            doc.Close()
            
            return True
        finally:
            if word:
                word.Quit()
            pythoncom.CoUninitialize()
    except Exception as e:
        print(f"Word COM转换失败: {e}", file=sys.stderr)
        return False


def generate_pdf(md_file, pdf_file):
    """生成PDF文件"""
    if not os.path.exists(md_file):
        print(f"错误：输入文件不存在 - {md_file}", file=sys.stderr)
        return False
    
    # 读取MD内容
    md_content = None
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']
    
    for encoding in encodings:
        try:
            with open(md_file, 'r', encoding=encoding) as f:
                md_content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if md_content is None:
        print(f"错误：无法读取文件编码 - {md_file}", file=sys.stderr)
        return False
    
    if not md_content.strip():
        print(f"错误：文件内容为空 - {md_file}", file=sys.stderr)
        return False
    
    # 确保输出目录存在
    output_dir = os.path.dirname(pdf_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # 确定docx临时文件路径
    docx_file = pdf_file.replace('.pdf', '.docx')
    
    # 生成docx文件
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from generate_docx import md_to_docx
    
    if not md_to_docx(md_content, docx_file):
        print("错误：无法生成Word文档", file=sys.stderr)
        return False
    
    # 验证docx文件
    if not os.path.exists(docx_file) or os.path.getsize(docx_file) == 0:
        print("错误：Word文档生成失败（文件为空）", file=sys.stderr)
        return False
    
    # 转换为PDF
    if platform.system() == 'Windows':
        print("正在使用Word转换为PDF...")
        if generate_pdf_with_word(docx_file, pdf_file):
            # 验证PDF文件
            if os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 0:
                print(f"PDF已生成：{pdf_file}")
                # 保留docx文件（用户可能需要）
                return True
            else:
                print("警告：PDF文件生成失败或为空", file=sys.stderr)
                # 保留docx文件作为备选
                print(f"提示：Word文档已生成：{docx_file}", file=sys.stderr)
                return False
        else:
            print("警告：无法使用Word生成PDF", file=sys.stderr)
            print(f"提示：Word文档已生成：{docx_file}", file=sys.stderr)
            return False
    else:
        # 非Windows系统：生成HTML文件作为降级方案
        html_file = pdf_file.replace('.pdf', '.html')
        html_content = md_to_html(md_content)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"非Windows系统，已生成HTML文件：{html_file}")
        print("提示：请用浏览器打开HTML文件，然后通过打印功能导出为PDF")
        return True


def main():
    if len(sys.argv) < 3:
        print("用法：python generate_pdf.py <input.md> <output.pdf>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    success = generate_pdf(input_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
