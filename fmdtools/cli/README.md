# fmdtools CLI

Intelligent conversational command-line tool for generating fmdtools fault modeling projects.

## Overview

The fmdtools CLI is an intelligent conversational model builder that creates complete fault modeling projects from natural language descriptions. It uses advanced NLP to understand your system descriptions, asks smart follow-up questions, and generates production-ready Python code following fmdtools architecture patterns.

## Installation

The CLI is included with fmdtools. Install fmdtools to access the CLI:

```bash
pip install fmdtools
```

## Usage

### Conversational Mode

Start the conversational model builder:

```bash
fmdtools create
```

Describe your system in natural language and the intelligent builder will create an fmdtools model. The system:
- Uses advanced NLP to understand complex system descriptions
- Intelligently extracts components, states, and fault modes
- Asks smart, contextual follow-up questions (maximum 3 per turn)
- Provides clear status updates and acknowledges what it understood
- Supports optional XML import from Draw.io or Gaphor for pre-filling

The builder reaches READY status when all required information is provided.

### Programmatic Usage

Use the CLI components directly in Python:

```python
from fmdtools.cli import LevelSpec, render_level

# Define your model specification
spec = LevelSpec(...)

# Generate model files
files = render_level(spec, output_directory="./my_model")
```

## Generated Structure

The CLI creates a complete fmdtools project with the following structure:

```
model_name/
├── __init__.py              # Package initialization
├── function_name.py         # Function implementations
├── flows.py                 # Flow definitions
├── architecture.py          # System architecture
└── level_model_name.py      # Main model class
```

## Code Quality

Generated code includes:

- **Function Classes**: Complete with state containers, mode containers, and fault definitions
- **Flow Classes**: With proper state variables and inheritance
- **Architecture Class**: Using correct fmdtools patterns (`add_fxn`, `init_architecture`)
- **Main Model**: With classification methods and simulation support
- **Documentation**: Comprehensive docstrings and comments
- **Examples**: TODO comments with implementation guidance

## File Descriptions

### Core Files

- **core.py**: Contains all core functionality including schemas, utilities, input processing, and code generation
- **wizard.py**: Interactive CLI wizard for guided model creation  
- **main.py**: CLI entry point and command-line interface
- **templates/**: Jinja2 templates for code generation

### Templates

The CLI uses Jinja2 templates to generate code:

- **function.py.j2**: Function class template with states, modes, and fault handling
- **flows.py.j2**: Flow class template with state containers
- **architecture.py.j2**: Architecture template with proper fmdtools structure
- **level.py.j2**: Main model template with simulation methods
- **init.py.j2**: Package initialization template

## Features

- **Input Validation**: Sanitizes user input and prevents code injection
- **Smart Processing**: Detects multiple items, suggests improvements
- **Error Handling**: Graceful error recovery and clear error messages
- **Security**: Proper escaping and validation of all user inputs
- **Standards Compliance**: Generates code that matches official fmdtools examples

## Example Workflow

1. Run `fmdtools create` command
2. Describe your system in natural language:
   ```
   > I want to model a pump system. The pump has rpm and temperature 
   > states and can fail due to overheating. Water flow has pressure.
   ```
3. Builder extracts information and asks targeted follow-ups if needed
4. When ready, type `generate` to create model files
5. Test generated model with included simulation functions

## Conversational Example

```
> I want you to build a model for the G37 AC system 2008 v6 engine

Got it - system: G37, components: AcSystem, Engine
What states does the AC system have? (e.g., temperature, pressure, flow_rate)
What can go wrong with AcSystem?
What can go wrong with the engine? (e.g., overheating, mechanical failure)

Status: Gathering system information

> temperature, the engine can combust

Got it - components: Engine, states: temperature, faults: combustion
What states does the AC system have? (e.g., temperature, pressure, flow_rate)
What can go wrong with AcSystem?

Status: READY - 1 components defined
Added: +name: G37, +component: Engine, +states: Engine, +faults: Engine

> generate

Generating your model...
Generated files:
g37/
├── engine.py
├── architecture.py
├── level_g37.py
├── __init__.py
Location: /path/to/g37

Model generated successfully!
```

## Demo Example

Here's a complete example of generating a simple electric motor model:

```python
from fmdtools.cli.core import LevelSpec, FunctionSpec, FlowSpec, ArchitectureSpec, SimulationSpec, ConnectionSpec, Fault, render_level

# Define simple motor model
spec = LevelSpec(
    name='SimpleMotor',
    description='Electric motor converts electrical power to mechanical rotation',
    functions=[
        FunctionSpec(
            name='Motor', 
            description='Electric motor converts electrical power to rotational motion',
            states={'rpm': 1800, 'temperature': 25, 'efficiency': 0.95},
            faults=[Fault(name='bearing_wear'), Fault(name='overheating')]
        )
    ],
    flows=[
        FlowSpec(name='ElectricalPower', description='Input electrical power', vars={'voltage': 12, 'current': 5}),
        FlowSpec(name='MechanicalPower', description='Output rotational power', vars={'torque': 10, 'rpm': 1800})
    ],
    architecture=ArchitectureSpec(
        name='MotorSystem',
        functions=['Motor'],
        connections=[
            ConnectionSpec(from_fn='Motor', to_fn='Motor', flow_name='ElectricalPower')
        ]
    ),
    simulation=SimulationSpec(sample_run=True, fault_analysis=True)
)

# Generate model files
files = render_level(spec, './simple_motor', force=True)
```

**Generated Output** (5 files, 222 lines of code):
- `motor.py` - Motor function with states (rpm, temperature, efficiency) and fault modes (bearing_wear, overheating)
- `flows.py` - ElectricalPower and MechanicalPower flow definitions with proper state variables
- `architecture.py` - MotorSystem architecture using correct fmdtools patterns (add_fxn, init_architecture)
- `level_simplemotor.py` - Main model class with find_classification method and simulation functions
- `__init__.py` - Package initialization with proper exports

**Key Features Demonstrated**:
- Complete fmdtools-compliant structure
- Proper fault modeling with Mode containers
- Domain-specific state variables
- Professional code generation with documentation
- Simulation-ready model structure

**Sample Generated File** (`motor.py`):
```python
class MotorState(State):
    """State for Motor function."""
    rpm: float = 1800
    temperature: float = 25
    efficiency: float = 0.95

class MotorMode(Mode):
    """Mode for Motor function."""
    failrate = 1e-5
    fault_bearing_wear = (1e-6,)
    fault_overheating = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Motor(Function):
    """Motor function implementation."""
    
    __slots__ = ()
    container_s = MotorState
    container_m = MotorMode

    def static_behavior(self, time):
        """Static behavior implementation."""
        # Check for fault conditions
        if self.m.has_fault('bearing_wear'):
            # TODO: Implement fault behavior for bearing_wear
            pass
        if self.m.has_fault('overheating'):
            # TODO: Implement fault behavior for overheating
            pass
        
        # Nominal behavior when no faults present
        if not self.m.has_fault():
            # TODO: Implement nominal static behavior
            pass
```

## Advanced Usage

### Custom Templates

Templates can be customized by modifying files in the `templates/` directory. All templates use Jinja2 syntax with custom filters for sanitization.

### Batch Generation

Generate multiple models programmatically:

```python
from fmdtools.cli.core import render_level, LevelSpec

specs = [spec1, spec2, spec3]
for spec in specs:
    render_level(spec, f"./models/{spec.name}")
```

## Development

The CLI is designed for maintainability with consolidated functionality:

- All schemas and utilities in `core.py`
- Interactive logic in `wizard.py`
- Template-based code generation
- Comprehensive input validation

## Support

For issues or questions:
- Check the main fmdtools documentation
- Review generated code comments and examples
- Examine templates for customization options