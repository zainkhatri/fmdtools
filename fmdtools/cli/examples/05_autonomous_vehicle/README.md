# Example 5: Autonomous Vehicle System

This example demonstrates a cutting-edge autonomous vehicle system with AI, sensors, and safety systems using the fmdtools CLI.

## CLI Command

```bash
cd /path/to/fmdtools
python -m fmdtools.cli.main
```

Then use the conversational interface:

```
I need an autonomous vehicle system with:
- A perception system with camera, lidar, and radar sensors
- A decision-making AI system with path planning and obstacle avoidance
- A propulsion system with electric motors and battery management
- A safety system with emergency braking and fail-safe mechanisms
- A communication system for V2X connectivity
- Flows for sensor data, control commands, and power
- Connections between all systems
- Fault analysis for sensor failures, AI errors, and system malfunctions
- Simulation for 60 minutes with 0.1 second time steps
- All analysis types enabled (sample run, fault analysis, parameter study)
```

## Generated Files

The CLI will generate:
- `perceptionsystem.py` - Sensor and perception function
- `decisionmaking.py` - AI decision-making function
- `propulsionsystem.py` - Electric propulsion function
- `safetysystem.py` - Safety and fail-safe function
- `communicationsystem.py` - V2X communication function
- `flows.py` - Data and control flow definitions
- `architecture.py` - Complete vehicle architecture
- `level_autonomousvehicle.py` - Main model class

## Key v2.2.0 Features Demonstrated

- ✅ State-of-the-art autonomous systems
- ✅ High-frequency simulation (0.1s time steps)
- ✅ Complex sensor and AI integration
- ✅ Safety-critical fault analysis
- ✅ All analysis types enabled
- ✅ New call syntax for different driving scenarios

## Usage

```python
from autonomousvehicle import AutonomousVehicle

# Create and run simulation
model = AutonomousVehicle(track='all')

# Different driving scenarios using new call syntax
urban_result = model(time=10.0)  # Urban driving
highway_result = model(time=30.0)  # Highway driving
parking_result = model(time=60.0)  # Parking scenario

# Traditional simulation
from fmdtools.sim.propagate import nominal
result, mdlhist = nominal(model, end_time=60.0)

# Comprehensive analysis
from fmdtools.sim.sample import ParameterSample
ps = ParameterSample()
ps.add_variable_replicates([], replicates=20)
from fmdtools.sim.propagate import parameter_sample
results, mdlhists = parameter_sample(model, ps)

# Safety-critical fault analysis
from fmdtools.sim.propagate import single_faults
results, mdlhists = single_faults(model)
```

## Expected Output

The autonomous vehicle will simulate with:
- Multi-sensor perception and data fusion
- AI-driven decision making and path planning
- Electric propulsion and battery management
- Safety systems and fail-safe mechanisms
- V2X communication and coordination
- Comprehensive fault detection and analysis
- High-frequency real-time simulation
