#!/usr/bin/env python3
"""
Generate all CLI examples to demonstrate fmdtools v2.2.0 features.
"""

import sys
import subprocess
from pathlib import Path

def run_example_generation(example_dir, example_name):
    """Run the example generation script."""
    print(f"\n{'='*60}")
    print(f"Generating {example_name} Example")
    print(f"{'='*60}")
    
    try:
        # Change to example directory
        example_path = Path(__file__).parent / example_dir
        script_path = example_path / "generate_example.py"
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        # Run the generation script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(example_path),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {example_name} generated successfully!")
            print("Output:")
            print(result.stdout)
            return True
        else:
            print(f"❌ {example_name} generation failed!")
            print("Error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error generating {example_name}: {e}")
        return False

def main():
    """Generate all CLI examples."""
    print("fmdtools CLI Examples Generator")
    print("Generating all examples to demonstrate v2.2.0 features")
    print("=" * 60)
    
    examples = [
        ("01_simple_motor", "Simple Motor"),
        ("02_hydraulic_pump", "Hydraulic Pump"),
        ("03_aircraft_engine", "Aircraft Engine"),
        ("04_power_grid", "Power Grid"),
        ("05_autonomous_vehicle", "Autonomous Vehicle")
    ]
    
    results = []
    
    for example_dir, example_name in examples:
        success = run_example_generation(example_dir, example_name)
        results.append((example_name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("GENERATION SUMMARY")
    print(f"{'='*60}")
    
    successful = 0
    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{name:20} {status}")
        if success:
            successful += 1
    
    print(f"\nOverall: {successful}/{len(results)} examples generated successfully")
    
    if successful == len(results):
        print("\n🎉 All examples generated successfully!")
        print("The CLI is working correctly with fmdtools v2.2.0 features!")
        print("\nNext steps:")
        print("1. Check the generated models in each example directory")
        print("2. Test the generated code with fmdtools")
        print("3. Use the interactive CLI to create your own models")
    else:
        print(f"\n⚠️  {len(results) - successful} examples failed to generate.")
        print("Check the error messages above for details.")
    
    return successful == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
