#!/usr/bin/env python3
"""
Import CTI Automation Chain outputs to ELK Stack
"""

import argparse
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from elasticsearch import Elasticsearch
    ES_AVAILABLE = True
except ImportError:
    ES_AVAILABLE = False

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class ELKImporter:
    def __init__(self, host: str, api_key: str, verify_certs: bool = True):
        if not ES_AVAILABLE:
            raise ImportError("elasticsearch package required: pip install elasticsearch")
        
        self.es = Elasticsearch(
            hosts=[host],
            api_key=api_key,
            verify_certs=verify_certs,
            request_timeout=60
        )
    
    def import_sigma_rules(self, rules_dir: Path, index: str = "sigma-rules") -> int:
        """Import Sigma rules as documents"""
        count = 0
        for rule_file in Path(rules_dir).rglob("*.yaml"):
            if not rule_file.is_file():
                continue
            
            with open(rule_file) as f:
                try:
                    rule = yaml.safe_load(f)
                    if not rule:
                        continue
                    
                    doc = {
                        **rule,
                        "@timestamp": datetime.utcnow().isoformat(),
                        "source": "cti-automation-chain",
                        "file_name": rule_file.name
                    }
                    
                    self.es.index(index=index, document=doc)
                    count += 1
                    console.print(f"  ✓ Imported: {rule_file.name}")
                except Exception as e:
                    console.print(f"[red]Failed to import {rule_file.name}: {e}[/red]")
        
        return count
    
    def import_kql_queries(self, queries_dir: Path, index: str = "kql-queries") -> int:
        """Import KQL queries as documents"""
        count = 0
        for query_file in Path(queries_dir).rglob("*.kql"):
            if not query_file.is_file():
                continue
            
            content = query_file.read_text()
            doc = {
                "query": content,
                "file_name": query_file.name,
                "@timestamp": datetime.utcnow().isoformat(),
                "source": "cti-automation-chain",
                "type": "kql"
            }
            
            try:
                self.es.index(index=index, document=doc)
                count += 1
                console.print(f"  ✓ Imported KQL: {query_file.name}")
            except Exception as e:
                console.print(f"[red]Failed to import {query_file.name}: {e}[/red]")
        
        return count
    
    def import_spl_queries(self, queries_dir: Path, index: str = "spl-queries") -> int:
        """Import Splunk SPL queries as documents"""
        count = 0
        for query_file in Path(queries_dir).rglob("*.spl"):
            if not query_file.is_file():
                continue
            
            content = query_file.read_text()
            doc = {
                "query": content,
                "file_name": query_file.name,
                "@timestamp": datetime.utcnow().isoformat(),
                "source": "cti-automation-chain",
                "type": "spl"
            }
            
            try:
                self.es.index(index=index, document=doc)
                count += 1
                console.print(f"  ✓ Imported SPL: {query_file.name}")
            except Exception as e:
                console.print(f"[red]Failed to import {query_file.name}: {e}[/red]")
        
        return count
    
    def import_playbooks(self, playbooks_dir: Path, index: str = "cti-playbooks") -> int:
        """Import playbook outputs as documents"""
        count = 0
        for pb_file in Path(playbooks_dir).rglob("*.md"):
            if not pb_file.is_file():
                continue
            
            content = pb_file.read_text()
            doc = {
                "content": pb_file.read_text(),
                "file_name": pb_file.name,
                "@timestamp": datetime.utcnow().isoformat(),
                "source": "cti-automation-chain",
                "type": "playbook"
            }
            
            try:
                self.es.index(index=index, document=doc)
                count += 1
                console.print(f"  ✓ Imported playbook: {pb_file.name}")
            except Exception as e:
                console.print(f"[red]Failed to import {pb_file.name}: {e}[/red]")
        
        return count


def main():
    parser = argparse.ArgumentParser(description="Import CTI Automation Chain outputs to ELK")
    parser.add_argument("--host", required=True, help="ELK host URL (e.g., https://your-elk.com:9200)")
    parser.add_argument("--api-key", required=True, help="ELK API key")
    parser.add_argument("--path", default="./output", help="Path to output directory")
    parser.add_argument("--rules-index", default="sigma-rules", help="Index for Sigma rules")
    parser.add_argument("--kql-index", default="kql-queries", help="Index for KQL queries")
    parser.add_argument("--spl-index", default="spl-queries", help="Index for Splunk SPL queries")
    parser.add_argument("--playbook-index", default="cti-playbooks", help="Index for playbooks")
    parser.add_argument("--all", action="store_true", help="Import all artifact types")
    parser.add_argument("--no-verify-certs", action="store_true", help="Disable SSL cert verification")
    
    args = parser.parse_args()
    
    if not ES_AVAILABLE:
        console.print("[red]elasticsearch package not installed. Run: pip install elasticsearch[/red]")
        sys.exit(1)
    
    output_path = Path(args.path)
    if not Path(args.path).exists():
        console.print(f"[red]Path not found: {args.path}[/red]")
        sys.exit(1)
    
    # Initialize importer
    try:
        importer = ELKImporter(
            host=args.host,
            api_key=args.api_key,
            verify_certs=not args.no_verify_certs
        )
        console.print("[green]Connected to ELK[/green]")
    except Exception as e:
        console.print(f"[red]Failed to connect to ELK: {e}[/red]")
        sys.exit(1)
    
    total_imported = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        # Import Sigma rules
        sigma_dir = Path(args.path) / "sigma"
        if sigma_dir.exists():
            task = progress.add_task("Importing Sigma rules...", total=None)
            count = importer.import_sigma_rules(sigma_dir, args.rules_index)
            progress.update(task, description=f"[green]✓ Imported {count} Sigma rules[/green]")
            total_imported += count
        
        # Import KQL queries
        kql_dir = Path(args.path) / "kql"
        if kql_dir.exists():
            task = progress.add_task("Importing KQL queries...", total=None)
            count = importer.import_kql_queries(kql_dir, args.kql_index)
            progress.update(task, description=f"[green]✓ Imported {count} KQL queries[/green]")
            total_imported += count
        
        # Import SPL queries
        spl_dir = Path(args.path) / "spl"
        if spl_dir.exists():
            task = progress.add_task("Importing SPL queries...", total=None)
            count = importer.import_spl_queries(spl_dir, args.spl_index)
            progress.update(task, description=f"[green]✓ Imported {count} SPL queries[/green]")
            total_imported += count
        
        # Import playbooks
        playbook_dir = Path(args.path)
        if playbook_dir.exists():
            task = progress.add_task("Importing playbooks...", total=None)
            count = importer.import_playbooks(playbook_dir, args.playbook_index)
            progress.update(task, description=f"[green]✓ Imported {count} playbooks[/green]")
            total_imported += count
    
    console.print(f"\n[bold green]Import complete! Total imported: {total_imported}[/bold green]")


if __name__ == "__main__":
    main()