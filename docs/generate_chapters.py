#!/usr/bin/env python3
import os
import re

chapters_dir = os.path.expanduser("~/Novel/chapters")
output_dir = os.path.expanduser("~/Novel/docs")

chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.endswith('.md')])

def md_to_html(content):
    # Remove the h1 title (first line starting with #)
    lines = content.split('\n')
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
    content = '\n'.join(lines).strip()
    
    # Convert paragraphs
    paragraphs = content.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Simple inline formatting
            p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'\*(.+?)\*', r'<em>\1</em>', p)
            # Replace newlines within paragraph with <br>
            p = p.replace('\n', '<br>')
            html_paragraphs.append(f'<p>{p}</p>')
    
    return '\n'.join(html_paragraphs)

for i, filename in enumerate(chapter_files):
    # Parse filename: 01-爱丁堡的风.md
    match = re.match(r'(\d+)-(.+)\.md', filename)
    if not match:
        continue
    
    num = match.group(1)
    title = match.group(2)
    
    # Read content
    with open(os.path.join(chapters_dir, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    html_content = md_to_html(content)
    
    # Navigation
    prev_link = f'<a href="chapter-{int(num)-1:02d}.html">← 上一章</a>' if i > 0 else '<span class="disabled">← 上一章</span>'
    next_link = f'<a href="chapter-{int(num)+1:02d}.html">下一章 →</a>' if i < len(chapter_files) - 1 else '<span class="disabled">下一章 →</span>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{num}章：{title} | 先凑合</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="chapter-page">
    <nav class="nav">
        <div class="nav-inner">
            <a href="index.html" class="nav-title">先凑合</a>
            <div class="nav-links">
                <a href="index.html#chapters">目录</a>
            </div>
        </div>
    </nav>

    <header class="chapter-header">
        <span class="chapter-number">第 {num} 章</span>
        <h1>{title}</h1>
    </header>

    <article class="chapter-content">
        {html_content}
    </article>

    <nav class="chapter-nav">
        {prev_link}
        <a href="index.html#chapters">目录</a>
        {next_link}
    </nav>

    <footer class="footer">
        <p>© 2026 先凑合</p>
    </footer>
</body>
</html>'''
    
    output_file = os.path.join(output_dir, f'chapter-{num}.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated: chapter-{num}.html')

print('Done!')
