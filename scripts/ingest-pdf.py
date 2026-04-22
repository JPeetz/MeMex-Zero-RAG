#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
PDF Ingestion for Memex

Extracts text from PDF files and prepares them for wiki ingestion.
Supports academic papers, reports, and general documents.

Usage:
    python scripts/ingest-pdf.py path/to/document.pdf
    python scripts/ingest-pdf.py path/to/document.pdf --output raw/

Requires:
    pip install pymupdf  # or: pip install PyMuPDF
    
For OCR support (scanned PDFs):
    pip install pytesseract pillow
    # Also need tesseract binary: brew install tesseract (macOS) / apt install tesseract-ocr (Linux)
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import pytesseract
    from PIL import Image
    import io
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


def validate_pdf(pdf_path: Path) -> bool:
    """Validate file is actually a PDF by checking magic bytes."""
    try:
        with open(pdf_path, 'rb') as f:
            header = f.read(8)
            # PDF files start with %PDF-
            return header[:5] == b'%PDF-'
    except (IOError, OSError):
        return False


def extract_with_pymupdf(pdf_path: Path) -> dict:
    """Extract text and metadata using PyMuPDF."""
    if not validate_pdf(pdf_path):
        raise ValueError(f"Invalid PDF file: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    
    # Extract metadata
    meta = doc.metadata
    
    # Extract text from all pages
    text_parts = []
    for page_num, page in enumerate(doc, 1):
        text = page.get_text("text")
        if text.strip():
            text_parts.append(f"<!-- Page {page_num} -->\n{text}")
        elif HAS_OCR:
            # Try OCR for image-based pages
            pix = page.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes()))
            ocr_text = pytesseract.image_to_string(img)
            if ocr_text.strip():
                text_parts.append(f"<!-- Page {page_num} (OCR) -->\n{ocr_text}")
    
    doc.close()
    
    return {
        "title": meta.get("title", ""),
        "author": meta.get("author", ""),
        "subject": meta.get("subject", ""),
        "keywords": meta.get("keywords", ""),
        "created": meta.get("creationDate", ""),
        "pages": len(text_parts),
        "text": "\n\n".join(text_parts)
    }


def extract_academic_metadata(text: str) -> dict:
    """Extract academic paper metadata from text content."""
    metadata = {}
    
    # Try to find abstract
    abstract_match = re.search(
        r'(?:^|\n)(?:Abstract|ABSTRACT)[:\s]*\n?(.*?)(?=\n(?:Introduction|INTRODUCTION|1\.|Keywords|KEYWORDS))',
        text,
        re.DOTALL | re.IGNORECASE
    )
    if abstract_match:
        metadata["abstract"] = abstract_match.group(1).strip()[:1000]
    
    # Try to find DOI
    doi_match = re.search(r'10\.\d{4,}/[^\s]+', text)
    if doi_match:
        metadata["doi"] = doi_match.group(0).rstrip('.,;')
    
    # Try to find arXiv ID
    arxiv_match = re.search(r'arXiv:(\d{4}\.\d{4,})', text)
    if arxiv_match:
        metadata["arxiv"] = arxiv_match.group(1)
    
    return metadata


def clean_text(text: str) -> str:
    """Clean extracted text for markdown compatibility."""
    # Fix common PDF extraction issues
    text = re.sub(r'(?<=[a-z])-\n(?=[a-z])', '', text)  # Fix hyphenation
    text = re.sub(r'\n{3,}', '\n\n', text)  # Normalize multiple newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Normalize whitespace
    text = re.sub(r'\f', '\n\n---\n\n', text)  # Page breaks to horizontal rules
    
    return text.strip()


def generate_markdown(pdf_path: Path, extracted: dict, academic_meta: dict) -> str:
    """Generate markdown file from extracted content."""
    
    # Determine title
    title = extracted["title"] or pdf_path.stem.replace("-", " ").replace("_", " ").title()
    
    # Build frontmatter
    frontmatter = [
        "---",
        f'title: "{title}"',
        f"type: source",
        f"source_type: pdf",
        f"source_file: {pdf_path.name}",
        f"ingested: {datetime.now().strftime('%Y-%m-%d')}",
    ]
    
    if extracted["author"]:
        frontmatter.append(f'author: "{extracted["author"]}"')
    
    if academic_meta.get("doi"):
        frontmatter.append(f'doi: "{academic_meta["doi"]}"')
    
    if academic_meta.get("arxiv"):
        frontmatter.append(f'arxiv: "{academic_meta["arxiv"]}"')
    
    if extracted["pages"]:
        frontmatter.append(f"pages: {extracted['pages']}")
    
    frontmatter.append("status: raw")
    frontmatter.append("---")
    
    # Build content
    content_parts = ["\n".join(frontmatter), ""]
    
    content_parts.append(f"# {title}")
    content_parts.append("")
    
    if extracted["author"]:
        content_parts.append(f"**Author:** {extracted['author']}")
        content_parts.append("")
    
    if academic_meta.get("abstract"):
        content_parts.append("## Abstract")
        content_parts.append("")
        content_parts.append(academic_meta["abstract"])
        content_parts.append("")
    
    content_parts.append("## Content")
    content_parts.append("")
    content_parts.append(clean_text(extracted["text"]))
    content_parts.append("")
    
    content_parts.append("---")
    content_parts.append("")
    content_parts.append(f"*Extracted from `{pdf_path.name}` on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    return "\n".join(content_parts)


def main():
    parser = argparse.ArgumentParser(description="Extract PDF content for Memex ingestion")
    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument("--output", "-o", type=Path, default=Path("raw"), help="Output directory (default: raw/)")
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR for scanned pages")
    args = parser.parse_args()
    
    if not HAS_PYMUPDF:
        print("❌ PyMuPDF not installed. Run: pip install pymupdf")
        sys.exit(1)
    
    if not args.pdf.exists():
        print(f"❌ File not found: {args.pdf}")
        sys.exit(1)
    
    print(f"📄 Processing: {args.pdf.name}")
    
    # Extract content
    extracted = extract_with_pymupdf(args.pdf)
    print(f"   Extracted {extracted['pages']} pages")
    
    # Extract academic metadata
    academic_meta = extract_academic_metadata(extracted["text"])
    if academic_meta.get("doi"):
        print(f"   Found DOI: {academic_meta['doi']}")
    
    # Generate markdown
    markdown = generate_markdown(args.pdf, extracted, academic_meta)
    
    # Write output
    args.output.mkdir(parents=True, exist_ok=True)
    output_file = args.output / f"{args.pdf.stem}.md"
    output_file.write_text(markdown, encoding="utf-8")
    
    print(f"✅ Saved to: {output_file}")
    print(f"")
    print(f"Next steps:")
    print(f"  1. Review {output_file}")
    print(f"  2. Ask your LLM: 'Ingest raw/{args.pdf.stem}.md following SCHEMA.md'")


if __name__ == "__main__":
    main()
