#!/usr/bin/env python3
"""
Generate the Autonomous Vehicle example using the fmdtools CLI.
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

def create_autonomous_vehicle_example():
    """Create an autonomous vehicle example using the CLI."""
    print("Generating Autonomous Vehicle Example...")
    print("=" * 50)
    
    spec = LevelSpec(
        name="AutonomousVehicle",
        description="Autonomous vehicle system with AI, sensors, and safety systems",
        functions=[
            FunctionSpec(
                name="PerceptionSystem",
                description="Multi-sensor perception system with camera, lidar, and radar",
                states={
                    "camera_quality": 1.0,
                    "lidar_range": 200.0,
                    "radar_detection": 1.0,
                    "sensor_fusion_accuracy": 0.95,
                    "object_detection_rate": 0.98
                },
                faults=[
                    Fault(name="camera_failure"),
                    Fault(name="lidar_failure"),
                    Fault(name="radar_failure"),
                    Fault(name="sensor_calibration_drift"),
                    Fault(name="weather_impact")
                ]
            ),
            FunctionSpec(
                name="DecisionMaking",
                description="AI decision-making system with path planning and obstacle avoidance",
                states={
                    "path_planning_accuracy": 0.99,
                    "obstacle_avoidance": 1.0,
                    "decision_confidence": 0.95,
                    "processing_latency": 0.05,
                    "ai_model_accuracy": 0.98
                },
                faults=[
                    Fault(name="ai_model_failure"),
                    Fault(name="path_planning_error"),
                    Fault(name="obstacle_detection_failure"),
                    Fault(name="decision_timeout"),
                    Fault(name="software_crash")
                ]
            ),
            FunctionSpec(
                name="PropulsionSystem",
                description="Electric propulsion system with battery management",
                states={
                    "motor_power": 150.0,
                    "battery_level": 80.0,
                    "efficiency": 0.92,
                    "temperature": 25.0,
                    "regenerative_braking": 0.85
                },
                faults=[
                    Fault(name="motor_failure"),
                    Fault(name="battery_degradation"),
                    Fault(name="inverter_failure"),
                    Fault(name="thermal_overload"),
                    Fault(name="power_management_failure")
                ]
            ),
            FunctionSpec(
                name="SafetySystem",
                description="Safety and fail-safe mechanisms",
                states={
                    "emergency_braking": 1.0,
                    "stability_control": 1.0,
                    "collision_avoidance": 1.0,
                    "fail_safe_status": 1.0,
                    "safety_margin": 0.9
                },
                faults=[
                    Fault(name="brake_system_failure"),
                    Fault(name="stability_control_failure"),
                    Fault(name="collision_avoidance_failure"),
                    Fault(name="fail_safe_override"),
                    Fault(name="safety_system_timeout")
                ]
            ),
            FunctionSpec(
                name="CommunicationSystem",
                description="V2X communication system for vehicle-to-everything connectivity",
                states={
                    "v2x_range": 1000.0,
                    "communication_latency": 0.01,
                    "signal_strength": 1.0,
                    "data_integrity": 0.99,
                    "network_coverage": 1.0
                },
                faults=[
                    Fault(name="communication_failure"),
                    Fault(name="network_timeout"),
                    Fault(name="signal_interference"),
                    Fault(name="data_corruption"),
                    Fault(name="antenna_failure")
                ]
            )
        ],
        flows=[
            FlowSpec(
                name="SensorData",
                description="Sensor data flow from perception to decision making",
                vars={"data_rate": 1000.0, "latency": 0.01, "accuracy": 0.95}
            ),
            FlowSpec(
                name="ControlCommands",
                description="Control commands from decision making to propulsion",
                vars={"command_rate": 100.0, "latency": 0.05, "reliability": 0.99}
            ),
            FlowSpec(
                name="PowerFlow",
                description="Electrical power flow through the vehicle",
                vars={"voltage": 400.0, "current": 200.0, "efficiency": 0.92}
            ),
            FlowSpec(
                name="SafetySignals",
                description="Safety signals and emergency commands",
                vars={"signal_strength": 1.0, "response_time": 0.001, "priority": 1.0}
            )
        ],
        architecture=ArchitectureSpec(
            name="AutonomousVehicleArchitecture",
            functions=["PerceptionSystem", "DecisionMaking", "PropulsionSystem", "SafetySystem", "CommunicationSystem"],
            connections=[
                ConnectionSpec(from_fn="PerceptionSystem", to_fn="DecisionMaking", flow_name="SensorData"),
                ConnectionSpec(from_fn="DecisionMaking", to_fn="PropulsionSystem", flow_name="ControlCommands"),
                ConnectionSpec(from_fn="PropulsionSystem", to_fn="PropulsionSystem", flow_name="PowerFlow"),
                ConnectionSpec(from_fn="SafetySystem", to_fn="PropulsionSystem", flow_name="SafetySignals"),
                ConnectionSpec(from_fn="CommunicationSystem", to_fn="DecisionMaking", flow_name="SensorData")
            ]
        ),
        simulation=SimulationSpec(
            sample_run=True,
            fault_analysis=True,
            parameter_study=True,
            end_time=60.0,
            time_step=0.1,
            units='min'
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
    spec, output_dir = create_autonomous_vehicle_example()
    print(f"\nExample generated successfully!")
    print(f"Generated model location: {output_dir}")
    print(f"Model name: {spec.name}")
