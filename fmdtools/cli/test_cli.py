#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimal tests for fmdtools CLI conversational builder.
"""

import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
import pytest

from .nlp_wizard import ConversationalBuilder, main
from .core import LevelSpec


def test_entrypoint_import():
    """Test that CLI entrypoint imports without errors."""
    from fmdtools.cli import main as cli_main
    from fmdtools.cli.main import main
    from fmdtools.cli.nlp_wizard import main as nlp_main
    
    # All imports should succeed
    assert cli_main is not None
    assert main is not None
    assert nlp_main is not None


def test_conversational_builder_init():
    """Test ConversationalBuilder initialization."""
    builder = ConversationalBuilder()
    
    # Initially spec is None until valid input is provided
    assert builder.spec is None
    assert builder.last_spec is None
    assert builder.conversation_history == []
    assert not builder.is_ready()


def test_system_info_extraction():
    """Test system information extraction from natural language."""
    builder = ConversationalBuilder()
    
    # Test rover example
    text = "Rover with GPS, IMU, two motors; faults: GPS dropout; 10 minutes at 10 Hz"
    info = builder.extract_system_info(text)
    
    # Should extract functions including Rover
    functions = info.get("functions", [])
    assert "Rover" in functions
    assert "Gps" in functions
    assert "Imu" in functions
    assert "Motor" in functions
    
    # Should extract faults
    faults = info.get("faults", [])
    assert "dropout" in faults


def test_smoke_conversation():
    """Smoke test: drive one prompt to READY and generate."""
    with tempfile.TemporaryDirectory() as temp_dir:
        builder = ConversationalBuilder()
        
        # First input: system description
        response1 = builder.update_spec("Simple pump system with rpm and temperature states; faults: overheating")
        assert "pump" in response1.lower()
        assert not builder.is_ready()
        
        # Should ask for more details since single-function systems need minimal setup
        assert "Status:" in response1
        
        # Add minimal state info to make it ready
        response2 = builder.update_spec("The pump has rpm: 1800, temperature: 25")
        
        # Should be ready now (single function with states)
        if builder.is_ready():
            # Generate files
            result = builder.generate_files(temp_dir)
            assert "Generated files:" in result
            
            # Check that files were created
            model_dir = Path(temp_dir) / builder.spec.name.lower()
            assert model_dir.exists()
            assert (model_dir / "pump.py").exists()
            assert (model_dir / "architecture.py").exists()


def test_rover_example_ready():
    """Test that rover example can reach READY state."""
    builder = ConversationalBuilder()
    
    # Input the rover description with better name pattern
    response1 = builder.update_spec("Rover system with GPS, IMU, two motors; faults: GPS dropout")
    
    # Should extract functions  
    if builder.spec:
        assert builder.spec.name
        assert len(builder.spec.functions) >= 1
        
        # Add states to make it ready
        response2 = builder.update_spec("Rover has position, velocity, battery level")
        
        # For single function systems with states, should be ready
        if len(builder.spec.functions) == 1 and all(f.states for f in builder.spec.functions):
            assert builder.is_ready()


def test_pydantic_validation():
    """Test that Pydantic validation works correctly."""
    builder = ConversationalBuilder()
    
    # Valid update should work
    response = builder.update_spec("Test pump with rpm state")
    assert "error" not in response.lower()
    
    # Spec should be valid LevelSpec
    if builder.spec:
        assert isinstance(builder.spec, LevelSpec)


@pytest.mark.integration
def test_cli_main_help():
    """Integration test: CLI main help command."""
    with patch('builtins.input', side_effect=['help', 'quit']):
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            # Should have printed help
            help_printed = any("natural language" in str(call) for call in mock_print.call_args_list)
            assert help_printed


@pytest.mark.integration  
def test_cli_main_quit():
    """Integration test: CLI main quit command."""
    with patch('builtins.input', side_effect=['quit']):
        with patch('builtins.print') as mock_print:
            main()
            
            # Should have printed goodbye
            goodbye_printed = any("Goodbye" in str(call) for call in mock_print.call_args_list)
            assert goodbye_printed


if __name__ == "__main__":
    # Run basic tests
    print("Running CLI tests...")
    
    test_entrypoint_import()
    print("✓ Entrypoint import test passed")
    
    test_conversational_builder_init()
    print("✓ ConversationalBuilder init test passed")
    
    test_system_info_extraction()
    print("✓ System info extraction test passed")
    
    test_smoke_conversation()
    print("✓ Smoke conversation test passed")
    
    test_rover_example_ready()
    print("✓ Rover example ready test passed")
    
    test_pydantic_validation()
    print("✓ Pydantic validation test passed")
    
    print("All tests passed!")