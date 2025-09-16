#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Architecture definition for SimpleMotor model.
"""

from fmdtools.define.architecture.function import FunctionArchitecture

# Import functions
from .motor import Motor

# Import flows


class Motorarchitecture(FunctionArchitecture):
    """MotorArchitecture architecture implementation."""
    
    default_sp = dict(end_time=100.0, time_step=1.0, units='sec')
    default_track = {'fxns': 'all', 'flows': 'all'}
    
    def init_architecture(self, **kwargs):
        """Initialize the architecture with flows and functions."""
        # Add flows

        # Add functions
        # Connect function to all flows (simplified approach)
        self.add_fxn("motor", Motor)

    def __call__(self, time=None, **kwargs):
        """Simulate the architecture until given time."""
        if time is not None:
            kwargs['end_time'] = time
        return super().__call__(**kwargs)