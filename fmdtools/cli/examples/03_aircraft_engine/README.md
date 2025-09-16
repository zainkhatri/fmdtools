# Example 3: Aircraft Engine System

This example demonstrates a complex multi-function system with multiple flows and sophisticated fault analysis using the fmdtools CLI.

## CLI Command

```bash
cd /path/to/fmdtools
python -m fmdtools.cli.main
```

Then use the conversational interface:

```
I need an aircraft engine system with:
- A turbofan engine with states for thrust, fuel consumption, temperature, pressure, and efficiency
- A fuel system with pressure, flow rate, and temperature monitoring
- A cooling system with coolant flow and temperature control
- An exhaust system for thrust and temperature management
- Flows for fuel, air, coolant, and exhaust
- Connections between all systems
- Comprehensive fault analysis for engine failures, fuel system issues, and cooling problems
- Simulation for 200 seconds with 2 second time steps
- Parameter study enabled for optimization
```

## Generated Files

The CLI will generate:
- `turbofanengine.py` - Main engine function
- `fuelsystem.py` - Fuel delivery system
- `coolingsystem.py` - Engine cooling system
- `exhaustsystem.py` - Exhaust management
- `flows.py` - All flow definitions
- `architecture.py` - Complete system architecture
- `level_aircraftengine.py` - Main model class

## Key v2.2.0 Features Demonstrated

- ✅ Complex multi-function architecture
- ✅ Multiple flow types and connections
- ✅ Parameter study capabilities
- ✅ Advanced fault analysis
- ✅ Custom simulation parameters
- ✅ New call syntax for different flight phases

## Usage

```python
from aircraftengine import AircraftEngine

# Create and run simulation
model = AircraftEngine(track='all')

# Different flight phases using new call syntax
takeoff_result = model(time=30.0)  # Takeoff phase
cruise_result = model(time=120.0)  # Cruise phase
landing_result = model(time=200.0)  # Landing phase

# Traditional simulation
from fmdtools.sim.propagate import nominal
result, mdlhist = nominal(model, end_time=200.0)

# Parameter study
from fmdtools.sim.sample import ParameterSample
ps = ParameterSample()
ps.add_variable_replicates([], replicates=5)
from fmdtools.sim.propagate import parameter_sample
results, mdlhists = parameter_sample(model, ps)

# Comprehensive fault analysis
from fmdtools.sim.propagate import single_faults
results, mdlhists = single_faults(model)
```

## Expected Output

The aircraft engine will simulate with:
- Thrust generation and fuel consumption
- Multi-system coordination
- Temperature and pressure management
- Exhaust gas handling
- Comprehensive fault detection and analysis
- Performance optimization through parameter studies
