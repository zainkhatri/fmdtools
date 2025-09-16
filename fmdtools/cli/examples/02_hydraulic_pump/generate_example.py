#!/usr/bin/env python3
"""
Generate the Hydraulic Pump example using the fmdtools CLI.
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
    FlowSpec,
    ConnectionSpec,
    Fault,
    render_level
)

def create_hydraulic_pump_example():
    """Create a hydraulic pump example using the CLI."""
    print("Generating Hydraulic Pump Example...")
    print("=" * 50)
    
    spec = LevelSpec(
        name="HydraulicPump",
        description="Hydraulic pump system with pressure control and reservoir",
        functions=[
            FunctionSpec(
                name="HydraulicPump",
                description="Main hydraulic pump with pressure and flow control",
                states={
                    "rpm": 1500.0,
                    "pressure": 100.0,
                    "flow_rate": 20.0,
                    "temperature": 45.0,
                    "efficiency": 0.88,
                    "vibration": 0.1
                },
                faults=[
                    Fault(name="cavitation"),
                    Fault(name="seal_leak"),
                    Fault(name="bearing_wear"),
                    Fault(name="motor_failure")
                ]
            ),
            FunctionSpec(
                name="PressureReliefValve",
                description="Pressure relief valve for system protection",
                states={
                    "position": 50.0,
                    "pressure_drop": 10.0,
                    "flow_coefficient": 1.0,
                    "response_time": 0.1
                },
                faults=[
                    Fault(name="stuck_open"),
                    Fault(name="stuck_closed"),
                    Fault(name="spring_failure")
                ]
            ),
            FunctionSpec(
                name="Reservoir",
                description="Hydraulic fluid reservoir with level and contamination monitoring",
                states={
                    "fluid_level": 80.0,
                    "temperature": 30.0,
                    "pressure": 1.0,
                    "contamination": 0.01
                },
                faults=[
                    Fault(name="leak"),
                    Fault(name="contamination"),
                    Fault(name="overheating")
                ]
            )
        ],
        flows=[
            FlowSpec(
                name="HydraulicFlow",
                description="Main hydraulic fluid flow from pump to valve",
                vars={"flow_rate": 20.0, "pressure": 100.0, "temperature": 45.0}
            ),
            FlowSpec(
                name="ReturnFlow",
                description="Return flow from valve to reservoir",
                vars={"flow_rate": 18.0, "pressure": 5.0, "temperature": 50.0}
            )
        ],
        architecture=ArchitectureSpec(
            name="HydraulicPumpArchitecture",
            functions=["HydraulicPump", "PressureReliefValve", "Reservoir"],
            connections=[
                ConnectionSpec(from_fn="HydraulicPump", to_fn="PressureReliefValve", flow_name="HydraulicFlow"),
                ConnectionSpec(from_fn="PressureReliefValve", to_fn="Reservoir", flow_name="ReturnFlow")
            ]
        ),
        simulation=SimulationSpec(
            sample_run=True,
            fault_analysis=True,
            parameter_study=False,
            end_time=100.0,
            time_step=0.5,
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
    spec, output_dir = create_hydraulic_pump_example()
    print(f"\nExample generated successfully!")
    print(f"Generated model location: {output_dir}")
    print(f"Model name: {spec.name}")
