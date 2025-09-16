# Example 1: Simple Motor System

This example demonstrates how to use the fmdtools CLI to generate a basic electric motor model with fault analysis capabilities.

## CLI Command

```bash
cd /path/to/fmdtools
python -m fmdtools.cli.main
```

Then use the conversational interface:

```
I want to create a simple electric motor system with:
- A motor function that has states for rpm, temperature, efficiency, and power consumption
- Faults for bearing wear, overheating, and electrical failure
- A basic simulation that runs for 50 seconds
- Fault analysis enabled
```

## Generated Files

The CLI will generate:
- `motor.py` - Motor function with v2.2.0 behavior methods
- `architecture.py` - System architecture with new call syntax
- `level_simplemotor.py` - Main model class
- `__init__.py` - Package initialization

## Key v2.2.0 Features Demonstrated

- ✅ Auto-generated slots (no manual `__slots__` definitions)
- ✅ New behavior method signatures without `time` argument
- ✅ `classify()` method for result classification
- ✅ New call syntax: `model(time=25.0)`
- ✅ Enhanced simulation parameters with `time_step` and `units`

## Usage

```python
from simplemotor import SimpleMotor

# Create and run simulation
model = SimpleMotor(track='all')
result = model(time=25.0)  # New v2.2.0 call syntax

# Traditional simulation
from fmdtools.sim.propagate import nominal
result, mdlhist = nominal(model, end_time=50.0)

# Fault analysis
from fmdtools.sim.propagate import one_fault
fault_scenarios = model.get_fault_scenarios()
if fault_scenarios:
    result, mdlhist = one_fault(model, fault_scenarios[0], end_time=50.0)
```

## Expected Output

The motor will simulate with:
- Initial RPM: 1800
- Temperature monitoring
- Efficiency tracking
- Power consumption analysis
- Fault detection and classification
