#!/usr/bin/env python3
"""
Generate the Simple Motor example using the fmdtools CLI.
"""

import sys
import os
from pathlib import Path

# Add fmdtools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from fmdtools.cli.core import (
    LevelSpec, 
    FunctionSpec, 
    ArchitectureSpec,
    SimulationSpec,
    Fault,
    render_level
)

def create_simple_motor_example():
    """Create a simple motor example using the CLI."""
    print("Generating Simple Motor Example...")
    print("=" * 50)
    
    spec = LevelSpec(
        name="SimpleMotor",
        description="Simple electric motor system for basic fault analysis",
        functions=[
            FunctionSpec(
                name="Motor",
                description="Electric motor with basic states and faults",
                states={
                    "rpm": 1800.0,
                    "temperature": 25.0,
                    "efficiency": 0.95,
                    "power_consumption": 1000.0,
                    "vibration": 0.1
                },
                faults=[
                    Fault(name="bearing_wear"),
                    Fault(name="overheating"),
                    Fault(name="electrical_failure")
                ]
            )
        ],
        flows=[],
        architecture=ArchitectureSpec(
            name="MotorArchitecture",
            functions=["Motor"],
            connections=[]
        ),
        simulation=SimulationSpec(
            sample_run=True,
            fault_analysis=True,
            parameter_study=False,
            end_time=50.0,
            time_step=1.0,
            units='sec'
        )
    )
    
    # Generate the model
    output_dir = Path(__file__).parent / "generated_model"
    files = render_level(spec, str(output_dir), force=True, dry_run=False)
    
    print(f"✓ Generated {len(files)} files in {output_dir}")
    print("Generated files:")
    for f in files:
        print(f"  - {f.name}")
    
    return spec, output_dir

if __name__ == "__main__":
    spec, output_dir = create_simple_motor_example()
    print(f"\nExample generated successfully!")
    print(f"Generated model location: {output_dir}")
    print(f"Model name: {spec.name}")
