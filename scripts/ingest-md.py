#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
#
# Ingest markdown files into Memex wiki
# Usage: python scripts/ingest-md.py <file.md> [--output wiki/sources/]
#
# Features:
# - Preserves existing frontmatter or generates new
# - Extracts title from H1 or filename
# - Detects wikilinks and converts if needed
# - Handles Obsidian-style links [[page]] and [[page|alias]]
# - Supports bulk ingestion from directories

"""
Markdown Ingestion for Memex

Ingests external markdown files into the wiki structure with proper
frontmatter, citations, and wikilink conversion.

Usage:
    python scripts/ingest-md.py document.md
    python scripts/ingest-md.py notes/ --recursive
    python scripts/ingest-md.py README.md --type sources --output wiki/sources/
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Optional: YAML parsing for frontmatter
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}, content
    
    # Find closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}, content
    
    frontmatter_text = content[4:end_match.start() + 3]
    body = content[end_match.end() + 3:]
    
    if HAS_YAML:
        try:
            frontmatter = yaml.safe_load(frontmatter_text) or {}
        except yaml.YAMLError:
            frontmatter = {}
    else:
        # Simple key: value parsing without yaml
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, _, value = line.partition(':')
                frontmatter[key.strip()] = value.strip().strip('"\'')
    
    return frontmatter, body


def extract_title(content: str, filename: str) -> str:
    """Extract title from H1 heading or filename."""
    # Try to find # Title
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    # Fall back to filename
    return filename.replace('-', ' ').replace('_', ' ').title()


def convert_links(content: str, link_style: str = "wikilink") -> str:
    """Convert between link styles."""
    if link_style == "wikilink":
        # Convert [text](file.md) to [[file|text]]
        def md_to_wiki(m):
            text, path = m.group(1), m.group(2)
            # Extract filename without extension
            name = Path(path).stem
            if text.lower() == name.lower().replace('-', ' '):
                return f"[[{name}]]"
            return f"[[{name}|{text}]]"
        
        content = re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', md_to_wiki, content)
    
    elif link_style == "markdown":
        # Convert [[page]] to [page](page.md)
        content = re.sub(r'\[\[([^\]|]+)\]\]', r'[\1](\1.md)', content)
        # Convert [[page|alias]] to [alias](page.md)
        content = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'[\2](\1.md)', content)
    
    return content


def detect_page_type(content: str, path: Path) -> str:
    """Detect appropriate wiki page type from content."""
    content_lower = content.lower()
    
    # Check parent directory name
    parent = path.parent.name.lower()
    if parent in ['sources', 'entities', 'concepts', 'synthesis']:
        return parent
    
    # Heuristics based on content
    if any(x in content_lower for x in ['abstract', 'doi:', 'arxiv:', 'published', 'journal']):
        return 'sources'
    if any(x in content_lower for x in ['born:', 'founded:', 'biography', 'career']):
        return 'entities'
    if any(x in content_lower for x in ['definition:', 'concept', 'theory', 'framework']):
        return 'concepts'
    if any(x in content_lower for x in ['synthesis', 'combining', 'integration', 'comparison']):
        return 'synthesis'
    
    return 'sources'  # Default


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def generate_frontmatter(
    title: str,
    page_type: str,
    source_path: Optional[str] = None,
    existing: Optional[dict] = None
) -> str:
    """Generate YAML frontmatter for wiki page."""
    fm = existing.copy() if existing else {}
    
    # Set/preserve fields
    if 'title' not in fm:
        fm['title'] = title
    if 'type' not in fm:
        fm['type'] = page_type
    if 'status' not in fm:
        fm['status'] = 'raw'
    if 'created' not in fm:
        fm['created'] = datetime.now().strftime('%Y-%m-%d')
    if 'tags' not in fm:
        fm['tags'] = []
    
    # Add source reference
    if source_path and 'source_file' not in fm:
        fm['source_file'] = source_path
    
    # Build YAML manually to control order
    lines = ['---']
    
    # Ordered fields first
    for key in ['title', 'type', 'status', 'created', 'updated', 'tags', 'source_file']:
        if key in fm:
            value = fm[key]
            if isinstance(value, list):
                lines.append(f'{key}: [{", ".join(str(v) for v in value)}]')
            elif isinstance(value, str) and (':' in value or '\n' in value):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
    
    # Remaining fields
    for key, value in fm.items():
        if key not in ['title', 'type', 'status', 'created', 'updated', 'tags', 'source_file']:
            if isinstance(value, list):
                lines.append(f'{key}: [{", ".join(str(v) for v in value)}]')
            elif isinstance(value, str) and (':' in value or '\n' in value):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
    
    lines.append('---')
    return '\n'.join(lines)


def ingest_markdown(
    input_path: Path,
    output_dir: Optional[Path] = None,
    page_type: Optional[str] = None,
    convert_links_style: Optional[str] = None,
    preserve_frontmatter: bool = True
) -> dict:
    """
    Ingest a markdown file into the wiki.
    
    Returns dict with:
        - output_path: where the file was written
        - title: extracted/generated title
        - type: page type
        - links: list of wikilinks found
    """
    content = input_path.read_text(encoding='utf-8')
    
    # Parse existing frontmatter
    existing_fm, body = parse_frontmatter(content)
    
    # Extract or generate title
    title = existing_fm.get('title') or extract_title(body, input_path.stem)
    
    # Determine page type
    if page_type:
        ptype = page_type
    elif 'type' in existing_fm:
        ptype = existing_fm['type']
    else:
        ptype = detect_page_type(body, input_path)
    
    # Convert links if requested
    if convert_links_style:
        body = convert_links(body, convert_links_style)
    
    # Find all wikilinks
    wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', body)
    
    # Generate output path
    if output_dir:
        out_dir = output_dir
    else:
        out_dir = Path('wiki') / ptype
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    slug = slugify(title)
    output_path = out_dir / f"{slug}.md"
    
    # Generate frontmatter
    fm_to_use = existing_fm if preserve_frontmatter else {}
    frontmatter = generate_frontmatter(
        title=title,
        page_type=ptype,
        source_path=str(input_path),
        existing=fm_to_use
    )
    
    # Ensure body starts with title if not present
    if not re.match(r'^#\s+', body.strip()):
        body = f"# {title}\n\n{body}"
    
    # Write output
    output_content = f"{frontmatter}\n\n{body.strip()}\n"
    output_path.write_text(output_content, encoding='utf-8')
    
    return {
        'input_path': str(input_path),
        'output_path': str(output_path),
        'title': title,
        'type': ptype,
        'links': list(set(wikilinks)),
        'has_frontmatter': bool(existing_fm)
    }


def ingest_directory(
    input_dir: Path,
    output_dir: Optional[Path] = None,
    recursive: bool = False,
    **kwargs
) -> list[dict]:
    """Ingest all markdown files from a directory."""
    results = []
    
    pattern = '**/*.md' if recursive else '*.md'
    
    for md_file in input_dir.glob(pattern):
        if md_file.name.startswith('.'):
            continue
        
        try:
            result = ingest_markdown(md_file, output_dir, **kwargs)
            results.append(result)
            print(f"✅ {md_file.name} → {result['output_path']}")
        except Exception as e:
            print(f"❌ {md_file.name}: {e}")
            results.append({
                'input_path': str(md_file),
                'error': str(e)
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Ingest markdown files into Memex wiki'
    )
    parser.add_argument('input', type=Path, help='Markdown file or directory')
    parser.add_argument('--output', '-o', type=Path, help='Output directory')
    parser.add_argument('--type', '-t', choices=['sources', 'entities', 'concepts', 'synthesis'],
                        help='Force page type')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Process directories recursively')
    parser.add_argument('--convert-links', choices=['wikilink', 'markdown'],
                        help='Convert link style')
    parser.add_argument('--no-preserve-fm', action='store_true',
                        help='Generate new frontmatter instead of preserving existing')
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"❌ Not found: {args.input}")
        sys.exit(1)
    
    kwargs = {
        'output_dir': args.output,
        'page_type': args.type,
        'convert_links_style': args.convert_links,
        'preserve_frontmatter': not args.no_preserve_fm
    }
    
    if args.input.is_dir():
        results = ingest_directory(args.input, recursive=args.recursive, **kwargs)
        print(f"\n📁 Ingested {len([r for r in results if 'error' not in r])} files")
    else:
        result = ingest_markdown(args.input, **kwargs)
        print(f"✅ {result['title']}")
        print(f"   Type: {result['type']}")
        print(f"   Output: {result['output_path']}")
        if result['links']:
            print(f"   Links: {', '.join(result['links'][:5])}" + 
                  (f" (+{len(result['links'])-5} more)" if len(result['links']) > 5 else ""))


if __name__ == '__main__':
    main()
