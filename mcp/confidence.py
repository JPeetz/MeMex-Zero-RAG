#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
Confidence Scoring for Memex

Tracks claim certainty and flags low-confidence information.
Each claim can have:
- Confidence level (high/medium/low/uncertain)
- Source count (how many sources support it)
- Contradiction flag (conflicting information exists)
- Last verified date

Usage:
    from confidence import ConfidenceTracker
    
    tracker = ConfidenceTracker(wiki_path="wiki")
    tracker.analyze()
    
    # Get low-confidence pages
    low = tracker.get_low_confidence(threshold=0.5)
    for page in low:
        print(f"{page['path']}: {page['score']:.2f} - {page['issues']}")

Claims are marked in wiki pages with confidence tags:
    [confidence: high|medium|low|uncertain]
    [sources: N]
    [verified: YYYY-MM-DD]
    [contradicts: page-name]
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class ClaimAnalysis:
    """Analysis of a single claim or page section."""
    text: str
    confidence: str  # high, medium, low, uncertain
    source_count: int
    verified_date: Optional[str]
    contradicts: List[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class PageConfidence:
    """Confidence analysis for a wiki page."""
    path: str
    title: str
    overall_score: float  # 0-1
    claims: List[ClaimAnalysis]
    issues: List[str]
    source_count: int
    has_contradictions: bool
    last_verified: Optional[str]
    stale: bool  # Not verified recently


class ConfidenceTracker:
    """
    Track and analyze confidence levels across wiki pages.
    """
    
    # Confidence level weights
    CONFIDENCE_WEIGHTS = {
        "high": 1.0,
        "medium": 0.7,
        "low": 0.4,
        "uncertain": 0.2
    }
    
    # Stale threshold (days since last verification)
    STALE_DAYS = 90
    
    def __init__(self, wiki_path: str = "wiki"):
        self.wiki_path = Path(wiki_path)
        self.pages: Dict[str, PageConfidence] = {}
    
    def analyze(self) -> Dict[str, PageConfidence]:
        """
        Analyze all wiki pages for confidence levels.
        
        Returns:
            Dict mapping path -> PageConfidence
        """
        self.pages = {}
        
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            rel_path = str(md_file.relative_to(self.wiki_path))
            content = md_file.read_text(encoding="utf-8")
            
            page = self._analyze_page(rel_path, content)
            self.pages[rel_path] = page
        
        # Cross-reference contradictions
        self._check_contradictions()
        
        return self.pages
    
    def _analyze_page(self, path: str, content: str) -> PageConfidence:
        """Analyze a single page."""
        title = path.replace(".md", "").split("/")[-1].replace("-", " ").title()
        claims = []
        issues = []
        
        # Extract frontmatter metadata
        source_count = 0
        last_verified = None
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                
                # Title
                title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                
                # Source count
                source_match = re.search(r'^source_count:\s*(\d+)', frontmatter, re.MULTILINE)
                if source_match:
                    source_count = int(source_match.group(1))
                
                # Verified date
                verified_match = re.search(r'^verified:\s*(\d{4}-\d{2}-\d{2})', frontmatter, re.MULTILINE)
                if verified_match:
                    last_verified = verified_match.group(1)
        
        # Count [Source: ...] citations in content
        source_citations = len(re.findall(r'\[Source:', content))
        source_count = max(source_count, source_citations)
        
        # Find confidence tags in content
        confidence_tags = re.findall(
            r'\[confidence:\s*(high|medium|low|uncertain)\]',
            content, re.IGNORECASE
        )
        
        # Find claims with explicit confidence
        for match in re.finditer(
            r'(?:^|\n)(.{10,200}?)\s*\[confidence:\s*(high|medium|low|uncertain)\]',
            content, re.IGNORECASE
        ):
            claims.append(ClaimAnalysis(
                text=match.group(1).strip(),
                confidence=match.group(2).lower(),
                source_count=source_count,
                verified_date=last_verified,
                line_number=content[:match.start()].count('\n') + 1
            ))
        
        # Find contradiction markers
        contradiction_markers = re.findall(
            r'\[contradicts:\s*([^\]]+)\]',
            content, re.IGNORECASE
        )
        has_contradictions = len(contradiction_markers) > 0 or "[CONFLICT]" in content
        
        # Calculate overall score
        if claims:
            claim_scores = [self.CONFIDENCE_WEIGHTS.get(c.confidence, 0.5) for c in claims]
            base_score = sum(claim_scores) / len(claim_scores)
        else:
            # No explicit confidence tags - infer from sources
            if source_count >= 3:
                base_score = 0.8
            elif source_count >= 1:
                base_score = 0.6
            else:
                base_score = 0.4
        
        # Adjust score
        score = base_score
        
        # Penalty for contradictions
        if has_contradictions:
            score *= 0.7
            issues.append("Has contradictions")
        
        # Penalty for no sources (on content pages)
        parts = path.split("/")
        is_content_page = len(parts) > 1 and parts[0] in ["sources", "entities", "concepts", "synthesis"]
        
        if is_content_page and source_count == 0:
            score *= 0.5
            issues.append("No source citations")
        
        # Check staleness
        stale = False
        if last_verified:
            try:
                verified_date = datetime.strptime(last_verified, "%Y-%m-%d")
                if datetime.now() - verified_date > timedelta(days=self.STALE_DAYS):
                    stale = True
                    score *= 0.9
                    issues.append(f"Not verified in {self.STALE_DAYS}+ days")
            except ValueError:
                pass
        
        # Bonus for high source count
        if source_count >= 5:
            score = min(1.0, score * 1.1)
        
        return PageConfidence(
            path=path,
            title=title,
            overall_score=round(score, 2),
            claims=claims,
            issues=issues,
            source_count=source_count,
            has_contradictions=has_contradictions,
            last_verified=last_verified,
            stale=stale
        )
    
    def _check_contradictions(self):
        """Cross-reference pages for contradictions."""
        # Build wikilink graph
        links: Dict[str, Set[str]] = {}
        
        for path, page in self.pages.items():
            md_file = self.wiki_path / path
            if md_file.exists():
                content = md_file.read_text(encoding="utf-8")
                page_links = re.findall(r'\[\[([^\]]+)\]\]', content)
                links[path] = set(page_links)
        
        # Check for mutual contradiction markers
        for path, page in self.pages.items():
            md_file = self.wiki_path / path
            if not md_file.exists():
                continue
            
            content = md_file.read_text(encoding="utf-8")
            
            # Find contradiction references
            contradicts = re.findall(r'\[contradicts:\s*([^\]]+)\]', content, re.IGNORECASE)
            
            for target in contradicts:
                target_path = f"{target}.md"
                # Check various locations
                for prefix in ["", "sources/", "entities/", "concepts/", "synthesis/"]:
                    full_path = f"{prefix}{target_path}"
                    if full_path in self.pages:
                        if not self.pages[full_path].has_contradictions:
                            self.pages[full_path].has_contradictions = True
                            self.pages[full_path].issues.append(f"Contradicted by {path}")
                            self.pages[full_path].overall_score *= 0.8
                        break
    
    def get_low_confidence(self, threshold: float = 0.5) -> List[PageConfidence]:
        """
        Get pages with confidence below threshold.
        
        Args:
            threshold: Score threshold (0-1)
            
        Returns:
            List of PageConfidence sorted by score ascending
        """
        low = [p for p in self.pages.values() if p.overall_score < threshold]
        return sorted(low, key=lambda x: x.overall_score)
    
    def get_needs_verification(self) -> List[PageConfidence]:
        """Get pages that need verification (stale or low confidence)."""
        needs = [p for p in self.pages.values() if p.stale or p.overall_score < 0.5]
        return sorted(needs, key=lambda x: x.overall_score)
    
    def get_contradictions(self) -> List[PageConfidence]:
        """Get all pages with contradictions."""
        return [p for p in self.pages.values() if p.has_contradictions]
    
    def generate_report(self) -> str:
        """Generate markdown confidence report."""
        if not self.pages:
            self.analyze()
        
        total = len(self.pages)
        high = len([p for p in self.pages.values() if p.overall_score >= 0.8])
        medium = len([p for p in self.pages.values() if 0.5 <= p.overall_score < 0.8])
        low = len([p for p in self.pages.values() if p.overall_score < 0.5])
        contradictions = len(self.get_contradictions())
        stale = len([p for p in self.pages.values() if p.stale])
        
        report = [
            "# Wiki Confidence Report",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total pages | {total} |",
            f"| High confidence (≥0.8) | {high} |",
            f"| Medium confidence (0.5-0.8) | {medium} |",
            f"| Low confidence (<0.5) | {low} |",
            f"| With contradictions | {contradictions} |",
            f"| Stale (>{self.STALE_DAYS} days) | {stale} |",
            "",
        ]
        
        # Low confidence pages
        low_pages = self.get_low_confidence(0.5)
        if low_pages:
            report.extend([
                "## Low Confidence Pages",
                "",
                "| Page | Score | Issues |",
                "|------|-------|--------|",
            ])
            for p in low_pages[:20]:
                issues = ", ".join(p.issues) or "—"
                report.append(f"| {p.path} | {p.overall_score:.2f} | {issues} |")
            report.append("")
        
        # Contradictions
        contradicted = self.get_contradictions()
        if contradicted:
            report.extend([
                "## Pages with Contradictions",
                "",
            ])
            for p in contradicted:
                report.append(f"- **{p.path}**: {', '.join(p.issues)}")
            report.append("")
        
        # Needs verification
        needs_verify = [p for p in self.pages.values() if p.stale]
        if needs_verify:
            report.extend([
                "## Needs Verification",
                "",
            ])
            for p in needs_verify[:10]:
                report.append(f"- {p.path} (last verified: {p.last_verified or 'never'})")
            report.append("")
        
        return "\n".join(report)
    
    def get_stats(self) -> dict:
        """Get confidence statistics."""
        if not self.pages:
            self.analyze()
        
        scores = [p.overall_score for p in self.pages.values()]
        
        return {
            "total_pages": len(self.pages),
            "avg_confidence": round(sum(scores) / len(scores), 2) if scores else 0,
            "high_confidence": len([s for s in scores if s >= 0.8]),
            "medium_confidence": len([s for s in scores if 0.5 <= s < 0.8]),
            "low_confidence": len([s for s in scores if s < 0.5]),
            "with_contradictions": len(self.get_contradictions()),
            "stale_pages": len([p for p in self.pages.values() if p.stale])
        }


def main():
    """CLI for confidence tracking."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memex confidence tracker")
    parser.add_argument("--wiki", "-w", type=str, default="wiki", help="Wiki path")
    parser.add_argument("--report", "-r", action="store_true", help="Generate full report")
    parser.add_argument("--low", "-l", type=float, default=0.5, help="Low confidence threshold")
    parser.add_argument("--output", "-o", type=str, help="Output file for report")
    args = parser.parse_args()
    
    tracker = ConfidenceTracker(wiki_path=args.wiki)
    tracker.analyze()
    
    if args.report:
        report = tracker.generate_report()
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"✅ Report saved to: {args.output}")
        else:
            print(report)
    else:
        stats = tracker.get_stats()
        print("📊 Confidence Statistics:")
        print(f"   Total pages: {stats['total_pages']}")
        print(f"   Average confidence: {stats['avg_confidence']}")
        print(f"   High (≥0.8): {stats['high_confidence']}")
        print(f"   Medium (0.5-0.8): {stats['medium_confidence']}")
        print(f"   Low (<0.5): {stats['low_confidence']}")
        print(f"   Contradictions: {stats['with_contradictions']}")
        print(f"   Stale: {stats['stale_pages']}")
        
        low = tracker.get_low_confidence(args.low)
        if low:
            print(f"\n⚠️  Low confidence pages:")
            for p in low[:10]:
                print(f"   {p.overall_score:.2f} {p.path}")


if __name__ == "__main__":
    main()
