#!/usr/bin/env python3
"""Generate PDF lead magnets from markdown articles using WeasyPrint."""

import os
import re
import sys
from weasyprint import HTML

ARTICLES_DIR = os.path.dirname(os.path.abspath(__file__))

CSS = """
body {
    font-family: 'Georgia', serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #222;
    max-width: 700px;
    margin: 40px auto;
}
h1 {
    font-size: 24pt;
    color: #1a1a2e;
    border-bottom: 3px solid #e94560;
    padding-bottom: 10px;
}
h2 {
    font-size: 16pt;
    color: #16213e;
    margin-top: 30px;
}
h3 {
    font-size: 13pt;
    color: #0f3460;
}
a { color: #e94560; }
blockquote {
    border-left: 4px solid #e94560;
    padding-left: 15px;
    margin-left: 0;
    color: #555;
    font-style: italic;
}
img { max-width: 100%; height: auto; }
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    font-size: 10pt;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
}
th {
    background-color: #f5f5f5;
    font-weight: bold;
    color: #1a1a2e;
}
ul, ol {
    padding-left: 25px;
}
li {
    margin-bottom: 4px;
}
strong { color: #1a1a2e; }
code {
    background: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 10pt;
}
"""


def md_to_html(text):
    """Convert markdown to HTML."""
    lines = text.split('\n')
    out = []
    in_list = False
    list_type = None
    in_blockquote = False
    in_table = False
    table_rows = []
    in_yaml_frontmatter = False
    yaml_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle YAML frontmatter (--- at start)
        if i == 0 and line.strip() == '---':
            in_yaml_frontmatter = True
            i += 1
            continue
        if in_yaml_frontmatter:
            if line.strip() == '---':
                in_yaml_frontmatter = False
                i += 1
                continue
            i += 1
            continue
        
        stripped = line.strip()
        
        # Blank line
        if stripped == '':
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            if in_table:
                out.append('</tbody></table>')
                in_table = False
            out.append('')
            i += 1
            continue
        
        # Horizontal rule
        if stripped in ('---', '***', '___', '* * *'):
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append('<hr>')
            i += 1
            continue
        
        # Headings
        h1_match = re.match(r'^# (.+)$', stripped)
        h2_match = re.match(r'^## (.+)$', stripped)
        h3_match = re.match(r'^### (.+)$', stripped)
        
        if h1_match:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append(f'<h1>{_inline(wrap_text(h1_match.group(1)))}</h1>')
            i += 1
            continue
        if h2_match:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append(f'<h2>{_inline(wrap_text(h2_match.group(1)))}</h2>')
            i += 1
            continue
        if h3_match:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
                list_type = None
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append(f'<h3>{_inline(wrap_text(h3_match.group(1)))}</h3>')
            i += 1
            continue
        
        # Blockquote (paragraph-mode, multi-line)
        if stripped.startswith('>'):
            if not in_blockquote:
                if in_list:
                    out.append(f'</{list_type}>')
                    in_list = False
                    list_type = None
                out.append('<blockquote>')
                in_blockquote = True
            content = re.sub(r'^>\s?', '', stripped)
            # Check if it's a bolded lead
            if content.startswith('**') and content.endswith('**'):
                content = f'<strong>{_inline(content[2:-2])}</strong>'
            else:
                content = _inline(wrap_text(content))
            out.append(f'<p style="margin:4px 0">{content}</p>')
            i += 1
            continue
        
        # Table detection - look ahead for header separator
        if '|' in stripped and not stripped.startswith('[') and not stripped.startswith('!'):
            # Check if next line is a table separator
            if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1].strip()):
                if in_list:
                    out.append(f'</{list_type}>')
                    in_list = False
                    list_type = None
                if in_blockquote:
                    out.append('</blockquote>')
                    in_blockquote = False
                # Parse header
                headers = [h.strip() for h in stripped.split('|') if h.strip()]
                out.append('<table><thead><tr>')
                for h in headers:
                    out.append(f'<th>{_inline(wrap_text(h))}</th>')
                out.append('</tr></thead><tbody>')
                i += 2  # Skip separator
                # Process data rows
                while i < len(lines) and '|' in lines[i]:
                    row = lines[i].strip()
                    if row == '':
                        break
                    cells = [c.strip() for c in row.split('|') if c.strip()]
                    if cells:
                        out.append('<tr>')
                        for c in cells:
                            out.append(f'<td>{_inline(wrap_text(c))}</td>')
                        out.append('</tr>')
                    i += 1
                out.append('</tbody></table>')
                continue
        
        # Unordered list
        ul_match = re.match(r'^(\s*)[\-*]\s+(.+)$', stripped)
        # Ordered list
        ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', stripped)
        
        if ul_match:
            if list_type != 'ul':
                if in_list:
                    out.append(f'</{list_type}>')
                out.append('<ul>')
                list_type = 'ul'
                in_list = True
            out.append(f'<li>{_inline(wrap_text(ul_match.group(2)))}</li>')
            i += 1
            continue
        
        if ol_match:
            if list_type != 'ol':
                if in_list:
                    out.append(f'</{list_type}>')
                out.append('<ol>')
                list_type = 'ol'
                in_list = True
            out.append(f'<li>{_inline(wrap_text(ol_match.group(2)))}</li>')
            i += 1
            continue
        
        # Regular paragraph
        if in_list:
            out.append(f'</{list_type}>')
            in_list = False
            list_type = None
        if in_blockquote:
            out.append('</blockquote>')
            in_blockquote = False
        
        # Image standalone line
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
        if img_match:
            alt = img_match.group(1)
            src = img_match.group(2)
            out.append(f'<p><img src="{src}" alt="{alt}"></p>')
            i += 1
            continue
        
        # Regular paragraph with inline formatting
        out.append(f'<p>{_inline(wrap_text(stripped))}</p>')
        i += 1
    
    # Close any open elements
    if in_list:
        out.append(f'</{list_type}>')
    if in_blockquote:
        out.append('</blockquote>')
    if in_table:
        out.append('</tbody></table>')
    
    return '\n'.join(out)


def wrap_text(text):
    """Escape HTML entities in raw text."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def _inline(text):
    """Process inline markdown: bold, italic, links, images, code."""
    # Images inline
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" style="max-width:100%;height:auto">', text)
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Em dash
    text = text.replace('---', '&mdash;')
    text = text.replace('--', '&ndash;')
    return text


def generate_pdf(md_file, pdf_file):
    """Generate PDF from markdown file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_body = md_to_html(md_content)
    
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""
    
    HTML(string=html_doc).write_pdf(pdf_file)
    size_kb = os.path.getsize(pdf_file) / 1024
    print(f"✅ {os.path.basename(pdf_file):55s} ({size_kb:.0f} KB)")


def main():
    articles = [
        "multi-agent-architecture-2026-05-23.md",
        "agentic-ai-governance-2026-05-25.md",
        "ai-agent-evaluation-2026-05-26.md",
        "enterprise-ai-agent-deployment-2026-05-27.md",
        "multi-agent-ai-frameworks-2026-05-28.md",
        "prompt-injection-defense-ai-agents-2026.md",
    ]
    
    print(f"\n📄 Generating PDFs from {len(articles)} articles in:\n   {ARTICLES_DIR}\n")
    
    for article in articles:
        md_path = os.path.join(ARTICLES_DIR, article)
        pdf_path = os.path.join(ARTICLES_DIR, article.replace('.md', '.pdf'))
        
        if not os.path.exists(md_path):
            print(f"❌ MISSING: {article}")
            continue
        
        try:
            generate_pdf(md_path, pdf_path)
        except Exception as e:
            print(f"❌ FAILED {article}: {e}")
    
    print(f"\n✨ Done! All PDFs saved to:\n   {ARTICLES_DIR}/\n")


if __name__ == '__main__':
    main()