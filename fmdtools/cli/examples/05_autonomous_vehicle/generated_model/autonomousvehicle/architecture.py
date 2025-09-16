#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Architecture definition for AutonomousVehicle model.
"""

from fmdtools.define.architecture.function import FunctionArchitecture

# Import functions
from .perceptionsystem import Perceptionsystem
from .decisionmaking import Decisionmaking
from .propulsionsystem import Propulsionsystem
from .safetysystem import Safetysystem
from .communicationsystem import Communicationsystem

# Import flows
from .flows import Sensordata, Controlcommands, Powerflow, Safetysignals

class Autonomousvehiclearchitecture(FunctionArchitecture):
    """AutonomousVehicleArchitecture architecture implementation."""
    
    default_sp = dict(end_time=100.0, time_step=1.0, units='sec')
    default_track = {'fxns': 'all', 'flows': 'all'}
    
    def init_architecture(self, **kwargs):
        """Initialize the architecture with flows and functions."""
        # Add flows
        self.add_flow("sensordata", Sensordata)
        self.add_flow("controlcommands", Controlcommands)
        self.add_flow("powerflow", Powerflow)
        self.add_flow("safetysignals", Safetysignals)

        # Add functions
        # Connect function to all flows (simplified approach)
        self.add_fxn("perceptionsystem", Perceptionsystem, "sensordata", "controlcommands", "powerflow", "safetysignals")
        # Connect function to all flows (simplified approach)
        self.add_fxn("decisionmaking", Decisionmaking, "sensordata", "controlcommands", "powerflow", "safetysignals")
        # Connect function to all flows (simplified approach)
        self.add_fxn("propulsionsystem", Propulsionsystem, "sensordata", "controlcommands", "powerflow", "safetysignals")
        # Connect function to all flows (simplified approach)
        self.add_fxn("safetysystem", Safetysystem, "sensordata", "controlcommands", "powerflow", "safetysignals")
        # Connect function to all flows (simplified approach)
        self.add_fxn("communicationsystem", Communicationsystem, "sensordata", "controlcommands", "powerflow", "safetysignals")

    def __call__(self, time=None, **kwargs):
        """Simulate the architecture until given time."""
        if time is not None:
            kwargs['end_time'] = time
        return super().__call__(**kwargs)