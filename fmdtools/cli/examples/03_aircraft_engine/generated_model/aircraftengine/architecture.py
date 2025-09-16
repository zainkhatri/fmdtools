#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Architecture definition for AircraftEngine model.
"""

from fmdtools.define.architecture.function import FunctionArchitecture

# Import functions
from .turbofanengine import Turbofanengine
from .fuelsystem import Fuelsystem
from .coolingsystem import Coolingsystem
from .exhaustsystem import Exhaustsystem

# Import flows
from .flows import Fuelflow, Airflow, Coolantflow, Exhaustflow

class Aircraftenginearchitecture(FunctionArchitecture):
    """AircraftEngineArchitecture architecture implementation."""
    
    default_sp = dict(end_time=100.0, time_step=1.0, units='sec')
    default_track = {'fxns': 'all', 'flows': 'all'}
    
    def init_architecture(self, **kwargs):
        """Initialize the architecture with flows and functions."""
        # Add flows
        self.add_flow("fuelflow", Fuelflow)
        self.add_flow("airflow", Airflow)
        self.add_flow("coolantflow", Coolantflow)
        self.add_flow("exhaustflow", Exhaustflow)

        # Add functions
        # Connect function to all flows (simplified approach)
        self.add_fxn("turbofanengine", Turbofanengine, "fuelflow", "airflow", "coolantflow", "exhaustflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("fuelsystem", Fuelsystem, "fuelflow", "airflow", "coolantflow", "exhaustflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("coolingsystem", Coolingsystem, "fuelflow", "airflow", "coolantflow", "exhaustflow")
        # Connect function to all flows (simplified approach)
        self.add_fxn("exhaustsystem", Exhaustsystem, "fuelflow", "airflow", "coolantflow", "exhaustflow")

    def __call__(self, time=None, **kwargs):
        """Simulate the architecture until given time."""
        if time is not None:
            kwargs['end_time'] = time
        return super().__call__(**kwargs)