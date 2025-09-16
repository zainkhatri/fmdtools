#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Architecture definition for PowerGrid model.
"""

from fmdtools.define.architecture.function import FunctionArchitecture

# Import functions
from .solarpowerplant import Solarpowerplant
from .windfarm import Windfarm
from .coalpowerplant import Coalpowerplant
from .powerdistribution import Powerdistribution
from .loadmanagement import Loadmanagement

# Import flows
from .flows import Electricalpower, Controlsignal, Dataflow

class Powergridarchitecture(FunctionArchitecture):
    """PowerGridArchitecture architecture implementation."""
    
    default_sp = dict(end_time=100.0, time_step=1.0, units='sec')
    default_track = {'fxns': 'all', 'flows': 'all'}
    
    def init_architecture(self, **kwargs):
        """Initialize the architecture with flows and functions."""
        # Add flows
        self.add_flow("electricalpower", Electricalpower)
        self.add_flow("controlsignal", Controlsignal)
        self.add_flow("dataflow", Dataflow)

        # Add functions
        # Connect function to all flows (simplified approach)
        self.add_fxn("solarpowerplant", Solarpowerplant, "electricalpower", "controlsignal", "dataflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("windfarm", Windfarm, "electricalpower", "controlsignal", "dataflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("coalpowerplant", Coalpowerplant, "electricalpower", "controlsignal", "dataflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("powerdistribution", Powerdistribution, "electricalpower", "controlsignal", "dataflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("loadmanagement", Loadmanagement, "electricalpower", "controlsignal", "dataflow")

    def __call__(self, time=None, **kwargs):
        """Simulate the architecture until given time."""
        if time is not None:
            kwargs['end_time'] = time
        return super().__call__(**kwargs)