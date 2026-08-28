#!/usr/bin/env python3
"""
Run a single stage of the CTI Automation Chain
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.run_chain import CTIAutomationChain


def main():
    parser = argparse.ArgumentParser(description="Run a single CTI Automation Chain stage")
    parser.add_argument("stage", choices=["r1", "r2", "r3", "r4"], help="Stage to run")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--config", default="config/config.yaml", help="Config file path")
    parser.add_argument("--sector", default="financial-services", help="Sector name")
    parser.add_argument("--region", default="global", help="Country/region")
    parser.add_argument("--stakeholders", default="SOC,Fraud,Compliance,Risk", help="Stakeholder teams")
    
    args = parser.parse_args()
    
    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {args.input}")
        sys.exit(1)
    
    input_data = input_path.read_text()
    
    variables = {
        "chain": "stage",
        "sector": args.sector,
        "region": args.region,
        "stakeholders": args.stakeholders,
        "job_role": "CTI Analyst",
        "product_service": f"CTI Stage {args.stage.upper()} Output"
    }
    
    # Initialize chain runner
    chain = CTIAutomationChain(args.config)
    
    # Map short stage names to chain names
    stage_map = {
        "r1": "r1_intel",
        "r2": "r2_detection", 
        "r3": "r3_automate",
        "r4": "r4_respond"
    }
    
    chain_name = stage_map.get(args.stage)
    if not chain_name:
        print(f"Invalid stage: {args.stage}")
        sys.exit(1)
    
    # Read input
    input_data = Path(args.input).read_text()
    
    # Run stage
    chain_runner = CTIAutomationChain(args.config)
    outputs = chain_runner.run_stage(chain_name, input_path.read_text(), {
        "chain": "stage",
        "sector": args.sector,
        "region": args.region,
        "stakeholders": args.stakeholders,
        "job_role": "CTI Analyst",
        "product_service": f"CTI Stage {args.stage.upper()} Output"
    })
    
    print(f"Stage {args.stage} complete. Outputs: {len(outputs)}")
    for key, output in outputs.items():
        print(f"  - {key}: {len(output)} chars")


if __name__ == "__main__":
    main()