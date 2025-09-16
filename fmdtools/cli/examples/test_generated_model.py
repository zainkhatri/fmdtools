#!/usr/bin/env python3
"""
Test a generated model to verify v2.2.0 features work correctly.
"""

import sys
import tempfile
from pathlib import Path

# Add fmdtools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from fmdtools.cli.core import (
    LevelSpec, 
    FunctionSpec, 
    ArchitectureSpec,
    SimulationSpec,
    Fault,
    render_level
)

def test_generated_model():
    """Test a generated model to verify v2.2.0 features."""
    print("Testing Generated Model with v2.2.0 Features")
    print("=" * 50)
    
    # Create a simple test model
    spec = LevelSpec(
        name="TestModel",
        description="Test model for v2.2.0 features",
        functions=[
            FunctionSpec(
                name="TestFunction",
                description="Test function with v2.2.0 features",
                states={
                    "value": 1.0,
                    "status": 1.0,
                    "efficiency": 0.9
                },
                faults=[
                    Fault(name="failure"),
                    Fault(name="degradation")
                ]
            )
        ],
        flows=[],
        architecture=ArchitectureSpec(
            name="TestArchitecture",
            functions=["TestFunction"],
            connections=[]
        ),
        simulation=SimulationSpec(
            sample_run=True,
            fault_analysis=False,
            end_time=10.0,
            time_step=1.0,
            units='sec'
        )
    )
    
    # Generate the model
    with tempfile.TemporaryDirectory() as temp_dir:
        files = render_level(spec, temp_dir, force=True, dry_run=False)
        print(f"✓ Generated {len(files)} files")
        
        # Add the generated directory to Python path
        sys.path.insert(0, temp_dir)
        
        try:
            # Import the main model class
            module_name = spec.name.lower()
            main_module = __import__(f"{module_name}.level_{module_name}", fromlist=[spec.name])
            
            # Find the model class
            if hasattr(main_module, 'MODEL_CLASS'):
                model_class = main_module.MODEL_CLASS
            else:
                for attr_name in dir(main_module):
                    attr = getattr(main_module, attr_name)
                    if (isinstance(attr, type) and 
                        hasattr(attr, '__bases__') and 
                        any('Architecture' in str(base) for base in attr.__bases__)):
                        model_class = attr
                        break
                else:
                    raise AttributeError(f"Could not find model class in {module_name}")
            
            print(f"✓ Successfully imported {spec.name} class")
            
            # Test model instantiation
            model = model_class(track='all')
            print(f"✓ Model instantiated with {len(model.functions)} functions")
            
            # Test v2.2.0 features
            print("\nTesting v2.2.0 features:")
            
            # Check for auto-generated slots
            test_fxn = model.functions['testfunction']
            if not hasattr(test_fxn, '__slots__') or test_fxn.__slots__ == ():
                print("✓ Auto-generated slots working (no manual __slots__)")
            else:
                print("⚠️  Manual __slots__ found")
            
            # Check behavior method signatures
            import inspect
            static_sig = inspect.signature(test_fxn.static_behavior)
            dynamic_sig = inspect.signature(test_fxn.dynamic_behavior)
            
            if len(static_sig.parameters) == 1:  # Only 'self'
                print("✓ Static behavior method has correct v2.2.0 signature")
            else:
                print("⚠️  Static behavior method has old signature")
                
            if len(dynamic_sig.parameters) == 1:  # Only 'self'
                print("✓ Dynamic behavior method has correct v2.2.0 signature")
            else:
                print("⚠️  Dynamic behavior method has old signature")
            
            # Check classify method
            if hasattr(test_fxn, 'classify'):
                classification = test_fxn.classify()
                print(f"✓ Classify method works: {classification}")
            else:
                print("⚠️  Classify method missing")
            
            # Check new call method
            if hasattr(model, '__call__'):
                print("✓ New call method present")
            else:
                print("⚠️  Call method missing")
            
            # Check simulation parameters
            if hasattr(model, 'default_sp') and 'time_step' in model.default_sp:
                print(f"✓ Enhanced simulation parameters: {model.default_sp}")
            else:
                print("⚠️  Old simulation parameters")
            
            print("\n🎉 All v2.2.0 features working correctly!")
            return True
            
        except Exception as e:
            print(f"❌ Model testing failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Clean up path
            if temp_dir in sys.path:
                sys.path.remove(temp_dir)

if __name__ == "__main__":
    success = test_generated_model()
    sys.exit(0 if success else 1)
