#!/usr/bin/env python3
"""
CTI Automation Chain Runner
Executes Feedly CTI Prompt Library as chained automation pipeline (R1→R2→R3→R4)
"""

import os
import sys
import yaml
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

class CTIAutomationChain:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.project_root = Path(__file__).parent.parent
        self.config = self._load_config()
        self.chains_dir = self.project_root / "chains"
        self.prompts_dir = self.project_root / "prompts"
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Chain order
        self.chain_order = [
            "r1_intel",
            "r2_detection", 
            "r3_automate",
            "r4_respond"
        ]
        
    def _load_config(self) -> Dict:
        if self.config_path.exists():
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_chain_config(self, chain_name: str) -> Dict:
        chain_dir = self.chains_dir / chain_name
        config_file = chain_dir / "chain.yaml"
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_prompt(self, prompt_path: str) -> str:
        full_path = self.project_root / prompt_path
        if full_path.exists():
            with open(full_path) as f:
                return f.read()
        return ""
    
    def _render_prompt(self, prompt_text: str, variables: Dict) -> str:
        """Render prompt template with variables"""
        rendered = prompt_text
        for key, value in variables.items():
            placeholder = f"[{key}]"
            rendered = rendered.replace(placeholder, str(value))
        return rendered
    
    def _run_prompt_via_opencode(self, prompt_text: str) -> str:
        """Execute prompt via OpenCode CLI"""
        try:
            result = subprocess.run(
                ["opencode", prompt_text],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=self.project_root
            )
            if result.returncode != 0:
                console.print(f"[red]OpenCode error: {result.stderr}[/red]")
                return ""
            return result.stdout
        except subprocess.TimeoutExpired:
            console.print("[red]OpenCode timeout[/red]")
            return ""
        except FileNotFoundError:
            console.print("[red]OpenCode not found. Install with: npm install -g opencode-ai[/red]")
            return ""
    
    def _save_output(self, chain_name: str, stage: str, output: str, variables: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{stage}_{timestamp}.md"
        with open(output_file, "w") as f:
            f.write(f"# {stage.upper()} Output\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write(f"**Chain:** {variables.get('chain', 'full')}\n")
            f.write(f"**Sector:** {variables.get('sector', 'financial-services')}\n")
            f.write(f"**Region:** {variables.get('region', 'global')}\n")
            f.write(f"**Stakeholders:** {variables.get('stakeholders', 'SOC,Fraud,Compliance,Risk')}\n\n")
            f.write("---\n\n")
            f.write(output)
        return output_file
    
    def run_stage(self, chain_name: str, input_data: str, variables: Dict) -> Dict[str, str]:
        """Run a single chain stage"""
        chain_config = self._load_chain_config(chain_name)
        if not chain_config:
            console.print(f"[red]Chain config not found: {chain_name}[/red]")
            return {}
        
        console.print(f"\n[bold cyan]Running stage: {chain_name}[/bold cyan]")
        
        # Prepare variables for this stage
        stage_vars = {**variables, "input_data": input_data}
        
        outputs = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            for prompt_config in chain_config.get("chain", {}).get("prompts", []):
                task = progress.add_task(f"Running {prompt_config['name']}...", total=None)
                
                # Load prompt
                prompt_text = self._load_prompt(prompt_config["file"])
                if not prompt_text:
                    progress.update(task, description=f"[red]Prompt not found: {prompt_config['file']}[/red]")
                    continue
                
                # Render with variables
                rendered_prompt = self._render_prompt(prompt_text, stage_vars)
                
                # Execute via OpenCode
                output = self._run_prompt_via_opencode(rendered_prompt)
                
                if output:
                    outputs[prompt_config["output_key"]] = output
                    stage_vars[prompt_config["output_key"]] = output
                    progress.update(task, description=f"[green]✓ {prompt_config['name']}[/green]")
                else:
                    progress.update(task, description=f"[red]✗ {prompt_config['name']} failed[/red]")
        
        return outputs
    
    def run_chain(self, chain_type: str, input_data: str, variables: Dict) -> Dict:
        """Run full chain or specific stage"""
        if chain_type == "full":
            stages = self.chain_order
        else:
            stages = [chain_type] if chain_type in self.chain_order else []
        
        if not stages:
            console.print(f"[red]Invalid chain type: {chain_type}[/red]")
            return {}
        
        all_outputs = {}
        current_input = input_data
        
        for stage in stages:
            console.rule(f"[bold]Stage: {stage}[/bold]")
            outputs = self.run_stage(stage, current_input, variables)
            all_outputs[stage] = outputs
            
            # Combine outputs for next stage
            combined = "\n\n---\n\n".join(outputs.values())
            current_input = combined
        
        return all_outputs


def main():
    parser = argparse.ArgumentParser(description="CTI Automation Chain Runner")
    parser.add_argument("--chain", choices=["full", "r1", "r2", "r3", "r4"], default="full", help="Chain to run")
    parser.add_argument("--input", required=True, help="Input file path (intel report)")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--config", default="config/config.yaml", help="Config file path")
    parser.add_argument("--sector", default="financial-services", help="Sector name")
    parser.add_argument("--region", default="global", help="Country/region")
    parser.add_argument("--stakeholders", default="SOC,Fraud,Compliance,Risk", help="Stakeholder teams")
    parser.add_argument("--stage-only", help="Run only specific stage (r1, r2, r3, r4)")
    
    args = parser.parse_args()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        console.print(f"[red]Input file not found: {args.input}[/red]")
        sys.exit(1)
    
    with open(input_path) as f:
        input_data = f.read()
    
    variables = {
        "chain": args.chain,
        "sector": args.sector,
        "region": args.region,
        "stakeholders": args.stakeholders,
        "job_role": "CTI Analyst",
        "product_service": "CTI Automation Chain Output"
    }
    
    # Initialize chain runner
    chain = CTIAutomationChain(args.config)
    
    # Run chain
    if args.stage_only:
        outputs = chain.run_stage(args.stage_only, input_path.read_text(), variables)
    else:
        outputs = chain.run_chain(args.chain, input_data, variables)
    
    # Print summary
    console.print("\n[bold green]Chain execution complete![/bold green]")
    
    table = Table(title="Output Summary")
    table.add_column("Stage", style="cyan")
    table.add_column("Outputs", style="green")
    table.add_column("Keys", style="yellow")
    
    for stage, outputs in outputs.items():
        if isinstance(outputs, dict):
            table.add_row(stage, str(len(outputs)), ", ".join(outputs.keys()))
        else:
            table.add_row(stage, "1", "combined")
    
    console.print(table)
    console.print(f"\nOutputs saved to: [bold]{args.output}[/bold]")


if __name__ == "__main__":
    main()