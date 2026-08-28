#!/usr/bin/env python3
"""
Validate CTI Automation Chain outputs
"""

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table

console = Console()

class OutputValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate_file(self, file_path: Path) -> Dict:
        """Validate a single output file"""
        results = {
            "file": str(file_path),
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        content = file_path.read_text()
        
        # Check for empty output
        if not content.strip():
            results["errors"].append("Empty output file")
            results["valid"] = False
            return results
        
        # Check for common issues
        if "Not available in provided reports" in content:
            results["warnings"].append("Contains 'Not available in provided reports' - may indicate missing data")
        
        if "I cannot" in content or "I'm unable" in content:
            results["warnings"].append("Contains refusal language - model may have refused")
        
        # Check for hallucination indicators
        hallucination_patterns = [
            r"As an AI language model",
            r"I don't have access to",
            r"I cannot browse",
            r"knowledge cutoff"
        ]
        for pattern in hallucination_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                results["warnings"].append(f"Possible hallucination indicator: '{pattern}'")
        
        # Check for required sections based on file type
        filename = file_path.name.lower()
        if "sigma" in filename:
            results["info"].append("Sigma rule detected - should be validated with sigmahq")
        elif "kql" in filename.lower() or "spl" in filename.lower():
            results["info"].append("KQL/SPL query detected - should be tested in target SIEM")
        elif "sitrep" in filename.lower():
            results["info"].append("SITREP detected - verify Confirmed/Assessed/Unknown labels")
        elif "sigma" in filename.lower():
            results["info"].append("Sigma rule - validate with pySigma before deployment")
        
        # Check for required fields in YAML (Sigma rules)
        if file_path.suffix in ['.yaml', '.yml']:
            if "id:" not in content:
                results["warnings"].append("Sigma rule missing 'id' field")
            if "status:" not in content:
                results["warnings"].append("Sigma rule missing 'status' field")
            if "logsource:" not in content:
                results["warnings"].append("Sigma rule missing 'logsource' field")
            if "detection:" not in content:
                results["warnings"].append("Sigma rule missing 'detection' field")
        
        # Check for KQL time-bounded joins
        if "kql" in filename.lower() or content.startswith(".kql"):
            if "ago(" not in content and "between" not in content.lower():
                results["warnings"].append("KQL query may be missing time-bounded filters")
        
        # Check for SPL time-bounded searches
        if "spl" in filename.lower() or content.startswith(".spl"):
            if "earliest=" not in content and "latest=" not in content:
                results["warnings"].append("SPL query may be missing time bounds")
        
        return results
    
    def validate_directory(self, dir_path: Path) -> List[Dict]:
        """Validate all markdown/yaml files in directory"""
        results = []
        for ext in ['.md', '.yaml', '.yml', '.kql', '.spl', '.json']:
            for file_path in dir_path.rglob(f"*{ext}"):
                if file_path.is_file():
                    results.append(self.validate_file(file_path))
        return results
    
    def print_report(self, results: List[Dict]):
        """Print validation report"""
        table = Table(title="Validation Report")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Errors", style="red")
        table.add_column("Warnings", style="yellow")
        table.add_column("Info", style="blue")
        
        total_errors = 0
        total_warnings = 0
        
        for result in results:
            status = "✅ Valid" if result["valid"] else "❌ Invalid"
            error_count = len(result["errors"])
            warning_count = len(result["warnings"])
            info_count = len(result["info"])
            
            total_errors += error_count
            total_warnings += warning_count
            
            table.add_row(
                Path(result["file"]).name,
                status,
                str(error_count) if error_count else "✓",
                str(warning_count) if warning_count else "✓",
                str(info_count) if info_count else "—"
            )
        
        console.print(table)
        console.print(f"\nTotal: {len(results)} files | Errors: {total_errors} | Warnings: {total_warnings}")
        
        # Print details
        for result in results:
            if result["errors"]:
                console.print(f"\n[red]Errors in {Path(result['file']).name}:[/red]")
                for err in result["errors"]:
                    console.print(f"  - {err}")
            if result["warnings"]:
                console.print(f"\n[yellow]Warnings in {Path(result['file']).name}:[/yellow]")
                for warn in result["warnings"]:
                    console.print(f"  - {warn}")


def main():
    parser = argparse.ArgumentParser(description="Validate CTI Automation Chain outputs")
    parser.add_argument("--path", default="./output", help="Path to output directory")
    parser.add_argument("--file", help="Validate single file")
    
    args = parser.parse_args()
    
    validator = OutputValidator()
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            console.print(f"[red]File not found: {args.file}[/red]")
            sys.exit(1)
        results = [validator.validate_file(file_path)]
    else:
        path = Path(args.path)
        if not path.exists():
            console.print(f"[red]Path not found: {args.path}[/red]")
            sys.exit(1)
        results = validator.validate_directory(path)
    
    validator.print_report(results)
    
    # Exit code based on errors
    has_errors = any(r["errors"] for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()