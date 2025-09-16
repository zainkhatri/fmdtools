#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compact fmdtools CLI - Interactive model builder.
"""

from .nlp_wizard import main as build_model
from .core import LevelSpec, render_level

__all__ = [
    'build_model',  # Main interactive builder
    'LevelSpec',    # For programmatic use
    'render_level'  # For generating files
]

# Simple entry point
def create_model():
    """Create a fmdtools model interactively."""
    build_model()