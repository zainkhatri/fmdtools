# Example 2: Hydraulic Pump System

This example demonstrates a more complex system with multiple functions, flows, and connections using the fmdtools CLI.

## CLI Command

```bash
cd /path/to/fmdtools
python -m fmdtools.cli.main
```

Then use the conversational interface:

```
I need a hydraulic pump system with:
- A hydraulic pump function with states for rpm, pressure, flow rate, temperature, efficiency, and vibration
- A pressure relief valve function with position, pressure drop, and response time
- A reservoir function for fluid level, temperature, and contamination
- Flows for hydraulic fluid and return flow
- Connections between pump, valve, and reservoir
- Fault analysis for cavitation, seal leaks, and valve failures
- Simulation for 100 seconds with 0.5 second time steps
```

## Generated Files

The CLI will generate:
- `hydraulicpump.py` - Pump function with v2.2.0 features
- `pressurereliefvalve.py` - Valve function
- `reservoir.py` - Reservoir function
- `flows.py` - Flow definitions
- `architecture.py` - System architecture with connections
- `level_hydraulicpump.py` - Main model class

## Key v2.2.0 Features Demonstrated

- ✅ Multi-function architecture with proper connections
- ✅ Flow definitions and connections
- ✅ Enhanced simulation parameters (`time_step=0.5`)
- ✅ Comprehensive fault analysis
- ✅ New call syntax for different simulation times

## Usage

```python
from hydraulicpump import HydraulicPump

# Create and run simulation
model = HydraulicPump(track='all')

# New v2.2.0 call syntax
result = model(time=50.0)  # Run for 50 seconds
result = model(time=100.0)  # Run for 100 seconds

# Traditional simulation
from fmdtools.sim.propagate import nominal
result, mdlhist = nominal(model, end_time=100.0)

# Fault analysis
from fmdtools.sim.propagate import one_fault
fault_scenarios = model.get_fault_scenarios()
for scenario in fault_scenarios[:3]:  # Test first 3 faults
    result, mdlhist = one_fault(model, scenario, end_time=100.0)
```

## Expected Output

The hydraulic system will simulate with:
- Pump operation at 1500 RPM
- Pressure regulation through relief valve
- Fluid circulation and temperature management
- Fault detection for cavitation, leaks, and valve failures
- Comprehensive system monitoring
