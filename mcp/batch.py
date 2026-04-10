#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
Batch API for Memex

Reduces costs by 50% using Anthropic/OpenAI batch APIs for bulk operations.
Ideal for:
- Initial wiki ingestion (many sources)
- Periodic wiki synthesis
- Bulk entity extraction
- Mass summarization

Usage:
    from batch import BatchProcessor
    
    processor = BatchProcessor(provider="anthropic")
    
    # Queue tasks
    for source in sources:
        processor.add_task(
            id=source.name,
            prompt=f"Summarize: {source.content}",
            system="You are a wiki curator..."
        )
    
    # Submit batch
    batch_id = processor.submit()
    
    # Poll for results (or wait)
    results = processor.wait_for_results(batch_id)

Requires:
    pip install anthropic  # For Anthropic batch API
    pip install openai     # For OpenAI batch API
"""

import json
import os
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class BatchTask:
    """Single task in a batch."""
    id: str
    prompt: str
    system: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 4096
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchResult:
    """Result from a batch task."""
    id: str
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BatchProcessor:
    """
    Batch processing using Anthropic or OpenAI batch APIs.
    
    Anthropic: Message Batches API (50% cost reduction)
    OpenAI: Batch API (50% cost reduction)
    """
    
    DEFAULT_MODELS = {
        "anthropic": "claude-sonnet-4-20250514",
        "openai": "gpt-4o"
    }
    
    def __init__(
        self,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        output_dir: str = ".memex/batches"
    ):
        self.provider = provider.lower()
        self.model = model or self.DEFAULT_MODELS.get(self.provider)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tasks: List[BatchTask] = []
        
        # Initialize client
        if self.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self.client = anthropic.Anthropic(api_key=api_key)
        elif self.provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("openai package not installed. Run: pip install openai")
            self.client = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'anthropic' or 'openai'")
    
    def add_task(
        self,
        id: str,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a task to the batch queue."""
        self.tasks.append(BatchTask(
            id=id,
            prompt=prompt,
            system=system,
            model=model or self.model,
            max_tokens=max_tokens,
            metadata=metadata or {}
        ))
    
    def clear_tasks(self):
        """Clear the task queue."""
        self.tasks = []
    
    def submit(self) -> str:
        """
        Submit queued tasks as a batch.
        
        Returns:
            Batch ID for tracking
        """
        if not self.tasks:
            raise ValueError("No tasks queued")
        
        if self.provider == "anthropic":
            return self._submit_anthropic()
        else:
            return self._submit_openai()
    
    def _submit_anthropic(self) -> str:
        """Submit batch to Anthropic."""
        requests = []
        
        for task in self.tasks:
            request = {
                "custom_id": task.id,
                "params": {
                    "model": task.model,
                    "max_tokens": task.max_tokens,
                    "messages": [
                        {"role": "user", "content": task.prompt}
                    ]
                }
            }
            
            if task.system:
                request["params"]["system"] = task.system
            
            requests.append(request)
        
        # Create batch
        batch = self.client.messages.batches.create(requests=requests)
        
        # Save batch info
        batch_info = {
            "id": batch.id,
            "provider": "anthropic",
            "created_at": datetime.now().isoformat(),
            "task_count": len(self.tasks),
            "status": batch.processing_status
        }
        
        info_path = self.output_dir / f"{batch.id}.json"
        info_path.write_text(json.dumps(batch_info, indent=2))
        
        print(f"✅ Submitted batch: {batch.id}")
        print(f"   Tasks: {len(self.tasks)}")
        print(f"   Status: {batch.processing_status}")
        
        self.clear_tasks()
        return batch.id
    
    def _submit_openai(self) -> str:
        """Submit batch to OpenAI."""
        # Create JSONL file
        jsonl_content = []
        
        for task in self.tasks:
            messages = []
            if task.system:
                messages.append({"role": "system", "content": task.system})
            messages.append({"role": "user", "content": task.prompt})
            
            request = {
                "custom_id": task.id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": task.model,
                    "messages": messages,
                    "max_tokens": task.max_tokens
                }
            }
            jsonl_content.append(json.dumps(request))
        
        # Write to temp file and upload
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('\n'.join(jsonl_content))
            temp_path = f.name
        
        try:
            # Upload file
            with open(temp_path, 'rb') as f:
                file_obj = self.client.files.create(file=f, purpose="batch")
            
            # Create batch
            batch = self.client.batches.create(
                input_file_id=file_obj.id,
                endpoint="/v1/chat/completions",
                completion_window="24h"
            )
            
            # Save batch info
            batch_info = {
                "id": batch.id,
                "provider": "openai",
                "created_at": datetime.now().isoformat(),
                "task_count": len(self.tasks),
                "status": batch.status,
                "input_file_id": file_obj.id
            }
            
            info_path = self.output_dir / f"{batch.id}.json"
            info_path.write_text(json.dumps(batch_info, indent=2))
            
            print(f"✅ Submitted batch: {batch.id}")
            print(f"   Tasks: {len(self.tasks)}")
            print(f"   Status: {batch.status}")
            
            self.clear_tasks()
            return batch.id
            
        finally:
            os.unlink(temp_path)
    
    def get_status(self, batch_id: str) -> dict:
        """Get batch status."""
        if self.provider == "anthropic":
            batch = self.client.messages.batches.retrieve(batch_id)
            return {
                "id": batch.id,
                "status": batch.processing_status,
                "created_at": str(batch.created_at),
                "completed": batch.processing_status == "ended",
                "counts": {
                    "total": batch.request_counts.processing + batch.request_counts.succeeded + batch.request_counts.errored,
                    "succeeded": batch.request_counts.succeeded,
                    "errored": batch.request_counts.errored,
                    "processing": batch.request_counts.processing
                }
            }
        else:
            batch = self.client.batches.retrieve(batch_id)
            return {
                "id": batch.id,
                "status": batch.status,
                "created_at": str(batch.created_at),
                "completed": batch.status in ["completed", "failed", "expired", "cancelled"],
                "counts": {
                    "total": batch.request_counts.total,
                    "completed": batch.request_counts.completed,
                    "failed": batch.request_counts.failed
                }
            }
    
    def get_results(self, batch_id: str) -> List[BatchResult]:
        """
        Get results from a completed batch.
        
        Returns:
            List of BatchResult for each task
        """
        if self.provider == "anthropic":
            return self._get_results_anthropic(batch_id)
        else:
            return self._get_results_openai(batch_id)
    
    def _get_results_anthropic(self, batch_id: str) -> List[BatchResult]:
        """Get results from Anthropic batch."""
        results = []
        
        for result in self.client.messages.batches.results(batch_id):
            if result.result.type == "succeeded":
                message = result.result.message
                content = ""
                for block in message.content:
                    if hasattr(block, 'text'):
                        content += block.text
                
                results.append(BatchResult(
                    id=result.custom_id,
                    success=True,
                    content=content,
                    usage={
                        "input_tokens": message.usage.input_tokens,
                        "output_tokens": message.usage.output_tokens
                    }
                ))
            else:
                results.append(BatchResult(
                    id=result.custom_id,
                    success=False,
                    error=str(result.result.error) if hasattr(result.result, 'error') else "Unknown error"
                ))
        
        return results
    
    def _get_results_openai(self, batch_id: str) -> List[BatchResult]:
        """Get results from OpenAI batch."""
        batch = self.client.batches.retrieve(batch_id)
        
        if not batch.output_file_id:
            return []
        
        # Download results file
        file_content = self.client.files.content(batch.output_file_id)
        
        results = []
        for line in file_content.text.strip().split('\n'):
            if not line:
                continue
            
            data = json.loads(line)
            custom_id = data["custom_id"]
            
            if data.get("error"):
                results.append(BatchResult(
                    id=custom_id,
                    success=False,
                    error=str(data["error"])
                ))
            else:
                response = data["response"]["body"]
                content = response["choices"][0]["message"]["content"]
                usage = response.get("usage", {})
                
                results.append(BatchResult(
                    id=custom_id,
                    success=True,
                    content=content,
                    usage={
                        "input_tokens": usage.get("prompt_tokens", 0),
                        "output_tokens": usage.get("completion_tokens", 0)
                    }
                ))
        
        return results
    
    def wait_for_results(
        self,
        batch_id: str,
        poll_interval: int = 30,
        timeout: int = 86400,  # 24 hours
        callback: Optional[Callable[[dict], None]] = None
    ) -> List[BatchResult]:
        """
        Wait for batch to complete and return results.
        
        Args:
            batch_id: Batch ID to wait for
            poll_interval: Seconds between status checks
            timeout: Maximum seconds to wait
            callback: Optional function called on each status check
            
        Returns:
            List of BatchResult
        """
        start_time = time.time()
        
        while True:
            status = self.get_status(batch_id)
            
            if callback:
                callback(status)
            
            if status["completed"]:
                if status["status"] in ["ended", "completed"]:
                    print(f"✅ Batch completed: {batch_id}")
                    return self.get_results(batch_id)
                else:
                    raise RuntimeError(f"Batch failed with status: {status['status']}")
            
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Batch {batch_id} did not complete within {timeout}s")
            
            print(f"⏳ Batch {batch_id}: {status['status']} ({status.get('counts', {})})")
            time.sleep(poll_interval)
    
    def list_batches(self, limit: int = 10) -> List[dict]:
        """List recent batches."""
        if self.provider == "anthropic":
            batches = self.client.messages.batches.list(limit=limit)
            return [
                {
                    "id": b.id,
                    "status": b.processing_status,
                    "created_at": str(b.created_at),
                    "counts": {
                        "succeeded": b.request_counts.succeeded,
                        "errored": b.request_counts.errored
                    }
                }
                for b in batches.data
            ]
        else:
            batches = self.client.batches.list(limit=limit)
            return [
                {
                    "id": b.id,
                    "status": b.status,
                    "created_at": str(b.created_at),
                    "counts": {
                        "completed": b.request_counts.completed,
                        "failed": b.request_counts.failed
                    }
                }
                for b in batches.data
            ]


class MemexBatchIngest:
    """
    Batch ingestion helper for Memex wikis.
    
    Uses batch API to process multiple source documents efficiently.
    """
    
    INGEST_SYSTEM = """You are a wiki curator. For the given source document:
1. Extract the key facts and claims
2. Identify entities (people, organizations, projects)
3. Identify concepts (ideas, methods, frameworks)
4. Note any dates, citations, or references
5. Summarize in 2-3 paragraphs

Format your response as YAML with sections:
- summary: 2-3 paragraph summary
- entities: list of {name, type, description}
- concepts: list of {name, description}
- claims: list of {text, confidence: high/medium/low}
- citations: list of source references found
"""
    
    def __init__(self, wiki_path: str = "wiki", provider: str = "anthropic"):
        self.wiki_path = Path(wiki_path)
        self.raw_path = Path("raw")
        self.processor = BatchProcessor(provider=provider)
    
    def queue_sources(self, sources: Optional[List[str]] = None):
        """
        Queue source files for batch ingestion.
        
        Args:
            sources: List of source filenames in raw/. If None, queues all.
        """
        if sources is None:
            sources = [f.name for f in self.raw_path.glob("*.md")]
        
        for source in sources:
            source_path = self.raw_path / source
            if not source_path.exists():
                print(f"⚠️  Skipping missing: {source}")
                continue
            
            content = source_path.read_text(encoding="utf-8")
            
            self.processor.add_task(
                id=source,
                prompt=f"Source document:\n\n{content}",
                system=self.INGEST_SYSTEM,
                metadata={"source_path": str(source_path)}
            )
        
        print(f"📥 Queued {len(self.processor.tasks)} sources for ingestion")
    
    def submit_and_wait(self) -> List[BatchResult]:
        """Submit batch and wait for results."""
        batch_id = self.processor.submit()
        return self.processor.wait_for_results(batch_id)
    
    def process_results(self, results: List[BatchResult]) -> dict:
        """
        Process batch results and generate wiki pages.
        
        Returns:
            Stats dict with counts of created pages
        """
        import yaml
        
        stats = {"sources": 0, "entities": 0, "concepts": 0, "errors": 0}
        
        for result in results:
            if not result.success:
                print(f"❌ Failed: {result.id} - {result.error}")
                stats["errors"] += 1
                continue
            
            try:
                # Parse YAML response
                data = yaml.safe_load(result.content)
                
                # Create source page
                source_name = Path(result.id).stem
                source_page = self.wiki_path / "sources" / f"{source_name}.md"
                source_page.parent.mkdir(parents=True, exist_ok=True)
                
                source_content = [
                    "---",
                    f"title: {source_name.replace('-', ' ').title()}",
                    "type: source",
                    f"ingested: {datetime.now().strftime('%Y-%m-%d')}",
                    "status: processed",
                    "---",
                    "",
                    f"# {source_name.replace('-', ' ').title()}",
                    "",
                    data.get("summary", ""),
                    "",
                    f"[Source: raw/{result.id}]"
                ]
                
                source_page.write_text("\n".join(source_content), encoding="utf-8")
                stats["sources"] += 1
                
                # TODO: Create entity and concept pages
                # This would be expanded based on the extracted data
                
            except Exception as e:
                print(f"❌ Error processing {result.id}: {e}")
                stats["errors"] += 1
        
        return stats


def main():
    """CLI for batch processing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memex batch processor")
    parser.add_argument("--provider", "-p", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("--list", "-l", action="store_true", help="List recent batches")
    parser.add_argument("--status", "-s", type=str, help="Get batch status")
    parser.add_argument("--results", "-r", type=str, help="Get batch results")
    parser.add_argument("--ingest", "-i", action="store_true", help="Batch ingest raw/ sources")
    args = parser.parse_args()
    
    if args.list:
        processor = BatchProcessor(provider=args.provider)
        batches = processor.list_batches()
        print(f"📋 Recent batches ({args.provider}):")
        for b in batches:
            print(f"   {b['id']}: {b['status']} ({b['counts']})")
    
    elif args.status:
        processor = BatchProcessor(provider=args.provider)
        status = processor.get_status(args.status)
        print(json.dumps(status, indent=2))
    
    elif args.results:
        processor = BatchProcessor(provider=args.provider)
        results = processor.get_results(args.results)
        for r in results:
            print(f"\n{'✅' if r.success else '❌'} {r.id}")
            if r.success:
                print(f"   {r.content[:200]}...")
            else:
                print(f"   Error: {r.error}")
    
    elif args.ingest:
        ingester = MemexBatchIngest(provider=args.provider)
        ingester.queue_sources()
        
        if input("Submit batch? [y/N] ").lower() == 'y':
            results = ingester.submit_and_wait()
            stats = ingester.process_results(results)
            print(f"✅ Processed: {stats}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
