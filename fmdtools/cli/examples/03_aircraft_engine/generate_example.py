#!/usr/bin/env python3
"""
Generate the Aircraft Engine example using the fmdtools CLI.
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

def create_aircraft_engine_example():
    """Create an aircraft engine example using the CLI."""
    print("Generating Aircraft Engine Example...")
    print("=" * 50)
    
    spec = LevelSpec(
        name="AircraftEngine",
        description="Aircraft turbofan engine system with comprehensive fault analysis",
        functions=[
            FunctionSpec(
                name="TurbofanEngine",
                description="Main turbofan engine with thrust generation and fuel consumption",
                states={
                    "thrust": 50000.0,
                    "fuel_consumption": 2000.0,
                    "temperature": 800.0,
                    "pressure": 15.0,
                    "efficiency": 0.35,
                    "rpm": 12000.0,
                    "bypass_ratio": 8.0
                },
                faults=[
                    Fault(name="compressor_stall"),
                    Fault(name="turbine_failure"),
                    Fault(name="combustion_chamber_failure"),
                    Fault(name="fan_blade_damage")
                ]
            ),
            FunctionSpec(
                name="FuelSystem",
                description="Fuel delivery and management system",
                states={
                    "fuel_pressure": 300.0,
                    "flow_rate": 2000.0,
                    "temperature": 20.0,
                    "fuel_level": 100.0,
                    "pump_efficiency": 0.95
                },
                faults=[
                    Fault(name="fuel_pump_failure"),
                    Fault(name="fuel_filter_clog"),
                    Fault(name="fuel_leak"),
                    Fault(name="injector_failure")
                ]
            ),
            FunctionSpec(
                name="CoolingSystem",
                description="Engine cooling and thermal management",
                states={
                    "coolant_temperature": 90.0,
                    "flow_rate": 100.0,
                    "pressure": 5.0,
                    "heat_exchanger_efficiency": 0.85
                },
                faults=[
                    Fault(name="coolant_pump_failure"),
                    Fault(name="radiator_clog"),
                    Fault(name="thermostat_failure"),
                    Fault(name="coolant_leak")
                ]
            ),
            FunctionSpec(
                name="ExhaustSystem",
                description="Exhaust gas management and thrust vectoring",
                states={
                    "exhaust_temperature": 600.0,
                    "exhaust_pressure": 2.0,
                    "thrust_vector_angle": 0.0,
                    "noise_level": 85.0
                },
                faults=[
                    Fault(name="exhaust_nozzle_failure"),
                    Fault(name="thrust_reverser_failure"),
                    Fault(name="noise_suppression_failure")
                ]
            )
        ],
        flows=[
            FlowSpec(
                name="FuelFlow",
                description="Fuel delivery from fuel system to engine",
                vars={"flow_rate": 2000.0, "pressure": 300.0, "temperature": 20.0}
            ),
            FlowSpec(
                name="AirFlow",
                description="Air intake and compression flow",
                vars={"flow_rate": 500.0, "pressure": 15.0, "temperature": 25.0}
            ),
            FlowSpec(
                name="CoolantFlow",
                description="Coolant circulation for thermal management",
                vars={"flow_rate": 100.0, "temperature": 90.0, "pressure": 5.0}
            ),
            FlowSpec(
                name="ExhaustFlow",
                description="Exhaust gases and thrust output",
                vars={"flow_rate": 700.0, "temperature": 600.0, "pressure": 2.0}
            )
        ],
        architecture=ArchitectureSpec(
            name="AircraftEngineArchitecture",
            functions=["TurbofanEngine", "FuelSystem", "CoolingSystem", "ExhaustSystem"],
            connections=[
                ConnectionSpec(from_fn="FuelSystem", to_fn="TurbofanEngine", flow_name="FuelFlow"),
                ConnectionSpec(from_fn="TurbofanEngine", to_fn="ExhaustSystem", flow_name="ExhaustFlow"),
                ConnectionSpec(from_fn="CoolingSystem", to_fn="TurbofanEngine", flow_name="CoolantFlow")
            ]
        ),
        simulation=SimulationSpec(
            sample_run=True,
            fault_analysis=True,
            parameter_study=True,
            end_time=200.0,
            time_step=2.0,
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
    spec, output_dir = create_aircraft_engine_example()
    print(f"\nExample generated successfully!")
    print(f"Generated model location: {output_dir}")
    print(f"Model name: {spec.name}")
