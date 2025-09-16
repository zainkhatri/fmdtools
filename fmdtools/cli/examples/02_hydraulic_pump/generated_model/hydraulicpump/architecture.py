#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Architecture definition for HydraulicPump model.
"""

from fmdtools.define.architecture.function import FunctionArchitecture

# Import functions
from .hydraulicpump import Hydraulicpump
from .pressurereliefvalve import Pressurereliefvalve
from .reservoir import Reservoir

# Import flows
from .flows import Hydraulicflow, Returnflow

class Hydraulicpumparchitecture(FunctionArchitecture):
    """HydraulicPumpArchitecture architecture implementation."""
    
    default_sp = dict(end_time=100.0, time_step=1.0, units='sec')
    default_track = {'fxns': 'all', 'flows': 'all'}
    
    def init_architecture(self, **kwargs):
        """Initialize the architecture with flows and functions."""
        # Add flows
        self.add_flow("hydraulicflow", Hydraulicflow)
        self.add_flow("returnflow", Returnflow)

        # Add functions
        # Connect function to all flows (simplified approach)
        self.add_fxn("hydraulicpump", Hydraulicpump, "hydraulicflow", "returnflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("pressurereliefvalve", Pressurereliefvalve, "hydraulicflow", "returnflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("reservoir", Reservoir, "hydraulicflow", "returnflow")

    def __call__(self, time=None, **kwargs):
        """Simulate the architecture until given time."""
        if time is not None:
            kwargs['end_time'] = time
        return super().__call__(**kwargs)