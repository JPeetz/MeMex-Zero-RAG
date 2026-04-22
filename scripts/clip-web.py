#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
Web Clipper for Memex

Fetches web pages, extracts readable content, and saves as markdown.
Handles articles, blog posts, documentation, and research papers.

Usage:
    python scripts/clip-web.py https://example.com/article
    python scripts/clip-web.py https://example.com/article --output raw/my-article.md
    python scripts/clip-web.py https://example.com/article --full  # Include all metadata

Requires:
    pip install httpx readability-lxml lxml beautifulsoup4

Optional:
    pip install trafilatura  # Better extraction for news articles
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    from readability import Document
    HAS_READABILITY = True
except ImportError:
    HAS_READABILITY = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False


def fetch_page(url: str, timeout: int = 30) -> str:
    """Fetch page content with proper headers."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_with_trafilatura(html: str, url: str) -> dict:
    """Extract content using trafilatura (best for news/blogs)."""
    result = trafilatura.bare_extraction(html, url=url, include_comments=False)
    
    if not result:
        return None
    
    return {
        "title": result.get("title", ""),
        "author": result.get("author", ""),
        "date": result.get("date", ""),
        "text": result.get("text", ""),
        "description": result.get("description", ""),
    }


def extract_with_readability(html: str, url: str) -> dict:
    """Extract content using readability (good general purpose)."""
    doc = Document(html)
    
    # Get clean HTML
    content_html = doc.summary()
    
    # Convert to plain text (simplified)
    soup = BeautifulSoup(content_html, "lxml")
    
    # Convert common elements to markdown
    for tag in soup.find_all("h1"):
        tag.replace_with(f"\n# {tag.get_text()}\n")
    for tag in soup.find_all("h2"):
        tag.replace_with(f"\n## {tag.get_text()}\n")
    for tag in soup.find_all("h3"):
        tag.replace_with(f"\n### {tag.get_text()}\n")
    for tag in soup.find_all("strong"):
        tag.replace_with(f"**{tag.get_text()}**")
    for tag in soup.find_all("em"):
        tag.replace_with(f"*{tag.get_text()}*")
    for tag in soup.find_all("code"):
        tag.replace_with(f"`{tag.get_text()}`")
    for tag in soup.find_all("a"):
        href = tag.get("href", "")
        text = tag.get_text()
        if href and text:
            tag.replace_with(f"[{text}]({href})")
    for tag in soup.find_all("li"):
        tag.replace_with(f"- {tag.get_text()}\n")
    for tag in soup.find_all("pre"):
        tag.replace_with(f"\n```\n{tag.get_text()}\n```\n")
    
    text = soup.get_text(separator="\n")
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return {
        "title": doc.title(),
        "author": "",
        "date": "",
        "text": text.strip(),
        "description": "",
    }


def extract_metadata(html: str) -> dict:
    """Extract additional metadata from page."""
    soup = BeautifulSoup(html, "lxml")
    meta = {}
    
    # Open Graph
    og_title = soup.find("meta", property="og:title")
    if og_title:
        meta["og_title"] = og_title.get("content", "")
    
    og_desc = soup.find("meta", property="og:description")
    if og_desc:
        meta["og_description"] = og_desc.get("content", "")
    
    og_image = soup.find("meta", property="og:image")
    if og_image:
        meta["og_image"] = og_image.get("content", "")
    
    # Article metadata
    author = soup.find("meta", attrs={"name": "author"})
    if author:
        meta["author"] = author.get("content", "")
    
    published = soup.find("meta", property="article:published_time")
    if published:
        meta["published"] = published.get("content", "")
    
    # Description
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        meta["description"] = desc.get("content", "")
    
    return meta


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:60]


def generate_markdown(url: str, extracted: dict, meta: dict, full: bool = False) -> str:
    """Generate markdown from extracted content."""
    
    now = datetime.now()
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    
    title = extracted.get("title") or meta.get("og_title") or f"Clip from {domain}"
    author = extracted.get("author") or meta.get("author") or ""
    date = extracted.get("date") or meta.get("published") or ""
    description = extracted.get("description") or meta.get("og_description") or ""
    
    frontmatter = [
        "---",
        f'title: "{title}"',
        f"type: source",
        f"source_type: web",
        f"url: {url}",
        f"domain: {domain}",
        f"clipped: {now.strftime('%Y-%m-%d')}",
    ]
    
    if author:
        frontmatter.append(f'author: "{author}"')
    
    if date:
        frontmatter.append(f"published: {date[:10] if len(date) > 10 else date}")
    
    frontmatter.append("status: raw")
    frontmatter.append("---")
    
    content = [
        "\n".join(frontmatter),
        "",
        f"# {title}",
        "",
    ]
    
    if author:
        content.append(f"**Author:** {author}")
        content.append("")
    
    content.append(f"**Source:** [{domain}]({url})")
    content.append("")
    
    if description and full:
        content.extend([
            "## Summary",
            "",
            description,
            "",
        ])
    
    content.extend([
        "## Content",
        "",
        extracted.get("text", "").strip(),
        "",
        "---",
        "",
        f"*Clipped from [{url}]({url}) on {now.strftime('%Y-%m-%d %H:%M')}*",
    ])
    
    return "\n".join(content)


def main():
    parser = argparse.ArgumentParser(description="Clip web pages for Memex")
    parser.add_argument("url", type=str, help="URL to clip")
    parser.add_argument("--output", "-o", type=Path, help="Output markdown file")
    parser.add_argument("--full", "-f", action="store_true", help="Include all metadata")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Request timeout in seconds")
    args = parser.parse_args()
    
    # Check dependencies
    if not HAS_HTTPX:
        print("❌ httpx not installed. Run: pip install httpx")
        sys.exit(1)
    
    if not HAS_READABILITY and not HAS_TRAFILATURA:
        print("❌ No extraction library installed. Run one of:")
        print("   pip install readability-lxml lxml beautifulsoup4")
        print("   pip install trafilatura")
        sys.exit(1)
    
    print(f"🌐 Fetching: {args.url}")
    
    try:
        html = fetch_page(args.url, timeout=args.timeout)
    except Exception as e:
        print(f"❌ Failed to fetch: {e}")
        sys.exit(1)
    
    print(f"📄 Fetched {len(html)} bytes")
    
    # Extract content
    extracted = None
    if HAS_TRAFILATURA:
        print("   Using trafilatura...")
        extracted = extract_with_trafilatura(html, args.url)
    
    if not extracted and HAS_READABILITY:
        print("   Using readability...")
        extracted = extract_with_readability(html, args.url)
    
    if not extracted or not extracted.get("text"):
        print("❌ Failed to extract content")
        sys.exit(1)
    
    # Extract additional metadata
    meta = {}
    if HAS_BS4:
        meta = extract_metadata(html)
    
    print(f"✅ Extracted: {extracted.get('title', 'Untitled')}")
    print(f"   {len(extracted.get('text', ''))} characters")
    
    # Generate markdown
    markdown = generate_markdown(args.url, extracted, meta, args.full)
    
    # Determine output path
    if args.output:
        output_file = args.output
    else:
        output_dir = Path("raw")
        output_dir.mkdir(parents=True, exist_ok=True)
        slug = slugify(extracted.get("title", "") or urlparse(args.url).path)
        output_file = output_dir / f"{slug}.md"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(markdown, encoding="utf-8")
    
    print(f"📝 Saved to: {output_file}")
    print("")
    print("Next steps:")
    print(f"  1. Review {output_file}")
    print(f"  2. Ask your LLM: 'Ingest {output_file} following SCHEMA.md'")


if __name__ == "__main__":
    main()
