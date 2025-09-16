# Example 4: Power Grid System

This example demonstrates a large-scale system with multiple power generation sources, distribution networks, and load management using the fmdtools CLI.

## CLI Command

```bash
cd /path/to/fmdtools
python -m fmdtools.cli.main
```

Then use the conversational interface:

```
I need a power grid system with:
- A solar power plant with states for power output, efficiency, and weather dependency
- A wind farm with power generation, wind speed dependency, and maintenance states
- A coal power plant with fuel consumption, emissions, and efficiency
- A power distribution network with voltage, current, and load balancing
- A load management system for demand response and grid stability
- Flows for electrical power, control signals, and data
- Connections between all power sources and distribution
- Fault analysis for equipment failures, weather impacts, and grid instability
- Simulation for 24 hours with 1 hour time steps
- Both fault analysis and parameter study enabled
```

## Generated Files

The CLI will generate:
- `solarpowerplant.py` - Solar generation function
- `windfarm.py` - Wind generation function
- `coalpowerplant.py` - Coal generation function
- `powerdistribution.py` - Distribution network function
- `loadmanagement.py` - Load management function
- `flows.py` - Power and control flow definitions
- `architecture.py` - Complete grid architecture
- `level_powergrid.py` - Main model class

## Key v2.2.0 Features Demonstrated

- ✅ Large-scale multi-function system
- ✅ Renewable and conventional power sources
- ✅ Complex flow networks
- ✅ Long-duration simulation (24 hours)
- ✅ Comprehensive fault analysis
- ✅ Parameter study for optimization
- ✅ New call syntax for different time periods

## Usage

```python
from powergrid import PowerGrid

# Create and run simulation
model = PowerGrid(track='all')

# Different time periods using new call syntax
morning_result = model(time=6.0)  # Morning peak
afternoon_result = model(time=12.0)  # Afternoon
evening_result = model(time=18.0)  # Evening peak
night_result = model(time=24.0)  # Night period

# Traditional simulation
from fmdtools.sim.propagate import nominal
result, mdlhist = nominal(model, end_time=24.0)

# Parameter study for optimization
from fmdtools.sim.sample import ParameterSample
ps = ParameterSample()
ps.add_variable_replicates([], replicates=10)
from fmdtools.sim.propagate import parameter_sample
results, mdlhists = parameter_sample(model, ps)

# Comprehensive fault analysis
from fmdtools.sim.propagate import single_faults
results, mdlhists = single_faults(model)
```

## Expected Output

The power grid will simulate with:
- Multiple power generation sources
- Renewable energy integration
- Grid stability and load balancing
- Fault detection and recovery
- Long-term performance analysis
- Optimization through parameter studies
