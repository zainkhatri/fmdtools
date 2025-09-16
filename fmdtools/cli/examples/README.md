# fmdtools CLI Examples

This directory contains comprehensive examples demonstrating the fmdtools CLI's capabilities with v2.2.0 features.

## Overview

The examples showcase different complexity levels and use cases:

1. **[Simple Motor System](01_simple_motor/)** - Basic single-function system
2. **[Hydraulic Pump System](02_hydraulic_pump/)** - Multi-function system with flows
3. **[Aircraft Engine System](03_aircraft_engine/)** - Complex multi-function system
4. **[Power Grid System](04_power_grid/)** - Large-scale distributed system
5. **[Autonomous Vehicle System](05_autonomous_vehicle/)** - State-of-the-art AI system

## Quick Start

### Generate All Examples

```bash
cd /path/to/fmdtools/fmdtools/cli/examples
python generate_all_examples.py
```

### Generate Individual Examples

```bash
cd /path/to/fmdtools/fmdtools/cli/examples/01_simple_motor
python generate_example.py
```

### Use the Interactive CLI

```bash
cd /path/to/fmdtools
python -m fmdtools.cli.main
```

Then follow the conversational prompts in each example's README.

## Key v2.2.0 Features Demonstrated

- ✅ **Auto-generated slots** - No manual `__slots__` definitions needed
- ✅ **New behavior method signatures** - Removed `time` argument from behavior methods
- ✅ **Classify method** - Added `classify()` method for result classification
- ✅ **New call syntax** - Added `__call__(time=None, **kwargs)` method for `model(time=5.0)` syntax
- ✅ **Enhanced simulation parameters** - Added `time_step` and `units` with proper defaults
- ✅ **Comprehensive fault analysis** - Multiple fault types and scenarios
- ✅ **Parameter studies** - Optimization and sensitivity analysis
- ✅ **Complex architectures** - Multi-function systems with flows and connections

## Example Complexity Levels

| Example | Functions | Flows | Connections | Simulation Time | Time Step | Features |
|---------|-----------|-------|-------------|-----------------|-----------|----------|
| Simple Motor | 1 | 0 | 0 | 50 sec | 1.0 sec | Basic fault analysis |
| Hydraulic Pump | 3 | 2 | 2 | 100 sec | 0.5 sec | Multi-function, flows |
| Aircraft Engine | 4 | 4 | 3 | 200 sec | 2.0 sec | Complex system, parameter study |
| Power Grid | 5 | 3 | 5 | 24 hr | 1.0 hr | Large-scale, long-duration |
| Autonomous Vehicle | 5 | 4 | 5 | 60 min | 0.1 min | AI system, high-frequency |

## Usage Patterns

### Basic Usage
```python
from generated_model import GeneratedModel

# Create and run simulation
model = GeneratedModel(track='all')
result = model(time=10.0)  # New v2.2.0 call syntax
```

### Traditional Simulation
```python
from fmdtools.sim.propagate import nominal
result, mdlhist = nominal(model, end_time=100.0)
```

### Fault Analysis
```python
from fmdtools.sim.propagate import single_faults
results, mdlhists = single_faults(model)
```

### Parameter Study
```python
from fmdtools.sim.sample import ParameterSample
ps = ParameterSample()
ps.add_variable_replicates([], replicates=10)
from fmdtools.sim.propagate import parameter_sample
results, mdlhists = parameter_sample(model, ps)
```

## Generated Code Structure

Each example generates:
- `function.py` - Function definitions with v2.2.0 features
- `flows.py` - Flow definitions (if applicable)
- `architecture.py` - System architecture with connections
- `level_modelname.py` - Main model class
- `__init__.py` - Package initialization

## Testing the Examples

Each example includes:
- README with detailed instructions
- `generate_example.py` script for automated generation
- Expected output descriptions
- Usage examples with v2.2.0 features

## Contributing

To add new examples:
1. Create a new directory with descriptive name
2. Add README.md with CLI prompts and usage
3. Add generate_example.py script
4. Update this main README
5. Test the example generation

## Support

For questions about the examples or CLI usage:
- Check the individual example READMEs
- Review the generated code
- Test with the interactive CLI
- Refer to the main fmdtools documentation
