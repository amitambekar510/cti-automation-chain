#!/usr/bin/env python3
"""
Generate Kibana Lens dashboards from CTI Automation Chain outputs
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console

console = Console()

class DashboardGenerator:
    def __init__(self):
        self.output_dir = Path("dashboards")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_sigma_dashboard(self, rules_dir: Path) -> Path:
        """Generate Kibana Lens dashboard for Sigma rules"""
        dashboard = {
            "attributes": {
                "title": "CTI Automation Chain - Sigma Rules Dashboard",
                "description": "Auto-generated dashboard for Sigma rules from CTI Automation Chain",
                "panelsJSON": json.dumps([
                    {
                        "type": "lens",
                        "version": "8.0.0",
                        "title": "Sigma Rules by ATT&CK Tactic",
                        "gridData": {"x": 0, "y": 0, "w": 24, "h": 15},
                        "lens": {
                            "layers": [{
                                "layerType": "table",
                                "data": {
                                    "columns": [
                                        {"name": "rule.title", "alias": "Rule Title"},
                                        {"name": "tags", "alias": "ATT&CK Tags"},
                                        {"name": "logsource.product", "alias": "Product"},
                                        {"name": "level", "alias": "Severity"}
                                    ]
                                }
                            }]
                        }
                    },
                    {
                        "type": "lens",
                        "version": "8.0.0",
                        "title": "Rules by Severity Level",
                        "gridData": {"x": 0, "y": 15, "w": 12, "h": 15},
                        "lens": {
                            "layers": [{
                                "layerType": "pie",
                                "data": {
                                    "series": [{
                                        "terms": {"field": "level", "size": 10}
                                    }]
                                }
                            }]
                        }
                    },
                    {
                        "type": "lens",
                        "version": "8.0.0",
                        "title": "Rules by Product",
                        "gridData": {"x": 12, "y": 15, "w": 12, "h": 15},
                        "lens": {
                            "layers": [{
                                "layerType": "pie",
                                "data": {
                                    "series": [{
                                        "terms": {"field": "logsource.product", "size": 10}
                                    }]
                                }
                            }]
                        }
                    }
                ],
                "timeRestore": True,
                "version": 1,
                "timeRange": {
                    "from": "now-7d",
                    "to": "now"
                }
            }
        
        output_file = self.output_dir / "sigma-dashboard.ndjson"
        with open(output_file, "w") as f:
            f.write(json.dumps(dashboard) + "\n")
        
        return output_file
    
    def generate_kql_dashboard(self, queries_dir: Path) -> Path:
        """Generate Kibana Lens dashboard for KQL queries"""
        dashboard = {
            "attributes": {
                "title": "CTI Automation Chain - KQL Queries Dashboard",
                "description": "Auto-generated dashboard for KQL queries from CTI Automation Chain",
                "panelsJSON": json.dumps([
                    {
                        "type": "lens",
                        "version": "8.0.0",
                        "title": "KQL Queries by ATT&CK Technique",
                        "gridData": {"x": 0, "y": 0, "w": 24, "h": 15},
                        "lens": {
                            "layers": [{
                                "layerType": "table",
                                "data": {
                                    "columns": [
                                        {"name": "file_name", "alias": "Query File"},
                                        {"name": "query", "alias": "KQL Query"}
                                    ]
                                }
                            }]
                        }
                    }
                ],
                "timeRestore": True,
                "version": 1,
                "timeRange": {
                    "from": "now-7d",
                    "to": "now"
                }
            }
        
        output_file = self.output_dir / "kql-dashboard.ndjson"
        with open(output_file, "w") as f:
            f.write(json.dumps(dashboard) + "\n")
        
        return output_file
    
    def generate_playbook_dashboard(self, playbooks_dir: Path) -> Path:
        """Generate Kibana Lens dashboard for playbooks"""
        dashboard = {
            "attributes": {
                "title": "CTI Automation Chain - Playbooks Dashboard",
                "description": "Auto-generated dashboard for playbooks from CTI Automation Chain",
                "panelsJSON": json.dumps([
                    {
                        "type": "lens",
                        "version": "8.0.0",
                        "title": "Playbooks by Stage",
                        "gridData": {"x": 0, "y": 0, "w": 24, "h": 15},
                        "lens": {
                            "layers": [{
                                "layerType": "pie",
                                "data": {
                                    "series": [{
                                        "terms": {"field": "stage", "size": 10}
                                    }]
                                }
                            }]
                        }
                    },
                    {
                        "type": "lens",
                        "version": "8.0.0",
                        "title": "Playbooks List",
                        "gridData": {"x": 0, "y": 15, "w": 24, "h": 20},
                        "lens": {
                            "layers": [{
                                "layerType": "table",
                                "data": {
                                    "columns": [
                                        {"name": "file_name", "alias": "Playbook"},
                                        {"name": "stage", "alias": "Stage"},
                                        {"name": "created_at", "alias": "Created"}
                                    ]
                                }
                            }]
                        }
                    }
                ],
                "timeRestore": True,
                "version": 1,
                "timeRange": {
                    "from": "now-30d",
                    "to": "now"
                }
            }
        
        output_file = self.output_dir / "playbooks-dashboard.ndjson"
        with open(output_file, "w") as f:
            f.write(json.dumps(dashboard) + "\n")
        
        return output_file
    
    def generate_all(self, output_path: Path):
        """Generate all dashboards"""
        results = []
        
        # Check for different output directories
        if (output_path / "sigma").exists():
            result = self.generate_sigma_dashboard(output_path / "sigma")
            results.append(("Sigma Rules Dashboard", result))
        
        if (output_path / "kql").exists():
            result = self.generate_kql_dashboard(output_path / "kql")
            results.append(("KQL Queries Dashboard", result))
        
        if (output_path / "playbooks").exists() or any(f.suffix == '.md' for f in output_path.rglob("*")):
            result = self.generate_playbook_dashboard(output_path)
            results.append(("Playbooks Dashboard", result))
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Generate Kibana dashboards from CTI Automation Chain outputs")
    parser.add_argument("--path", default="./output", help="Path to output directory")
    parser.add_argument("--all", action="store_true", help="Generate all dashboards")
    parser.add_argument("--sigma", action="store_true", help="Generate Sigma dashboard only")
    parser.add_argument("--kql", action="store_true", help="Generate KQL dashboard only")
    parser.add_argument("--playbooks", action="store_true", help="Generate playbooks dashboard only")
    
    args = parser.parse_args()
    
    generator = DashboardGenerator()
    output_path = Path(args.path)
    
    if not output_path.exists():
        console.print(f"[red]Path not found: {args.path}[/red]")
        sys.exit(1)
    
    results = []
    
    if args.all or args.sigma:
        if (output_path / "sigma").exists() or any(f.suffix in ['.yaml', '.yml'] for f in output_path.rglob("*")):
            result = generator.generate_sigma_dashboard(output_path / "sigma" if (output_path / "sigma").exists() else output_path)
            results.append(("Sigma Rules Dashboard", result))
            console.print(f"[green]✓[/green] Generated: {result}")
    
    if args.all or args.kql:
        if (output_path / "kql").exists() or any(f.suffix == '.kql' for f in output_path.rglob("*")):
            result = generator.generate_kql_dashboard(output_path / "kql" if (output_path / "kql").exists() else output_path)
            results.append(("KQL Queries Dashboard", result))
            console.print(f"[green]✓[/green] Generated: {result}")
    
    if args.all or args.playbooks:
        result = generator.generate_playbook_dashboard(output_path)
        results.append(("Playbooks Dashboard", result))
        console.print(f"[green]✓[/green] Generated: {result}")
    
    if not results:
        console.print("[yellow]No output files found to generate dashboards[/yellow]")
    
    console.print(f"\nDashboards saved to: [bold]{generator.output_dir}[/bold]")
    console.print("\nImport in Kibana: Stack Management → Saved Objects → Import")


if __name__ == "__main__":
    main()