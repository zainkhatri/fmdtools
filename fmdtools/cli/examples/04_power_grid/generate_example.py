#!/usr/bin/env python3
"""
Generate the Power Grid example using the fmdtools CLI.
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

def create_power_grid_example():
    """Create a power grid example using the CLI."""
    print("Generating Power Grid Example...")
    print("=" * 50)
    
    spec = LevelSpec(
        name="PowerGrid",
        description="Power grid system with multiple generation sources and distribution",
        functions=[
            FunctionSpec(
                name="SolarPowerPlant",
                description="Solar power generation with weather dependency",
                states={
                    "power_output": 100.0,
                    "efficiency": 0.22,
                    "irradiance": 800.0,
                    "temperature": 25.0,
                    "panel_condition": 1.0
                },
                faults=[
                    Fault(name="panel_failure"),
                    Fault(name="inverter_failure"),
                    Fault(name="weather_impact"),
                    Fault(name="grid_connection_failure")
                ]
            ),
            FunctionSpec(
                name="WindFarm",
                description="Wind power generation with wind speed dependency",
                states={
                    "power_output": 150.0,
                    "wind_speed": 12.0,
                    "efficiency": 0.45,
                    "turbine_condition": 1.0,
                    "maintenance_status": 1.0
                },
                faults=[
                    Fault(name="turbine_failure"),
                    Fault(name="gearbox_failure"),
                    Fault(name="wind_speed_variation"),
                    Fault(name="maintenance_required")
                ]
            ),
            FunctionSpec(
                name="CoalPowerPlant",
                description="Coal-fired power generation with fuel consumption",
                states={
                    "power_output": 500.0,
                    "fuel_consumption": 1000.0,
                    "efficiency": 0.38,
                    "emissions": 800.0,
                    "boiler_temperature": 600.0
                },
                faults=[
                    Fault(name="boiler_failure"),
                    Fault(name="turbine_failure"),
                    Fault(name="fuel_supply_failure"),
                    Fault(name="emissions_control_failure")
                ]
            ),
            FunctionSpec(
                name="PowerDistribution",
                description="Power distribution network with voltage and load management",
                states={
                    "voltage": 138.0,
                    "current": 1000.0,
                    "load_balance": 1.0,
                    "grid_frequency": 60.0,
                    "transmission_losses": 0.05
                },
                faults=[
                    Fault(name="transformer_failure"),
                    Fault(name="transmission_line_failure"),
                    Fault(name="voltage_regulation_failure"),
                    Fault(name="frequency_instability")
                ]
            ),
            FunctionSpec(
                name="LoadManagement",
                description="Load management and demand response system",
                states={
                    "total_demand": 750.0,
                    "peak_demand": 1000.0,
                    "demand_response": 0.0,
                    "grid_stability": 1.0,
                    "reserve_margin": 0.15
                },
                faults=[
                    Fault(name="demand_forecast_failure"),
                    Fault(name="load_shedding_failure"),
                    Fault(name="grid_stability_loss"),
                    Fault(name="communication_failure")
                ]
            )
        ],
        flows=[
            FlowSpec(
                name="ElectricalPower",
                description="Electrical power flow through the grid",
                vars={"voltage": 138.0, "current": 1000.0, "frequency": 60.0}
            ),
            FlowSpec(
                name="ControlSignal",
                description="Control signals for grid management",
                vars={"signal_strength": 1.0, "response_time": 0.1, "reliability": 0.99}
            ),
            FlowSpec(
                name="DataFlow",
                description="Data flow for monitoring and control",
                vars={"data_rate": 100.0, "latency": 0.05, "integrity": 1.0}
            )
        ],
        architecture=ArchitectureSpec(
            name="PowerGridArchitecture",
            functions=["SolarPowerPlant", "WindFarm", "CoalPowerPlant", "PowerDistribution", "LoadManagement"],
            connections=[
                ConnectionSpec(from_fn="SolarPowerPlant", to_fn="PowerDistribution", flow_name="ElectricalPower"),
                ConnectionSpec(from_fn="WindFarm", to_fn="PowerDistribution", flow_name="ElectricalPower"),
                ConnectionSpec(from_fn="CoalPowerPlant", to_fn="PowerDistribution", flow_name="ElectricalPower"),
                ConnectionSpec(from_fn="PowerDistribution", to_fn="LoadManagement", flow_name="ControlSignal"),
                ConnectionSpec(from_fn="LoadManagement", to_fn="PowerDistribution", flow_name="DataFlow")
            ]
        ),
        simulation=SimulationSpec(
            sample_run=True,
            fault_analysis=True,
            parameter_study=True,
            end_time=24.0,
            time_step=1.0,
            units='hr'
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
    spec, output_dir = create_power_grid_example()
    print(f"\nExample generated successfully!")
    print(f"Generated model location: {output_dir}")
    print(f"Model name: {spec.name}")
