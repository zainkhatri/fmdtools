#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flow definitions for PowerGrid model.
"""

from fmdtools.define.flow.base import Flow
from fmdtools.define.container.state import State

class ElectricalpowerState(State):
    """State for Electricalpower flow."""
    voltage: float = 138.0
    current: float = 1000.0
    frequency: float = 60.0


class Electricalpower(Flow):
    """Electricalpower flow - Electrical power flow through the grid."""
    
    container_s = ElectricalpowerState


class ControlsignalState(State):
    """State for Controlsignal flow."""
    signal_strength: float = 1.0
    response_time: float = 0.1
    reliability: float = 0.99


class Controlsignal(Flow):
    """Controlsignal flow - Control signals for grid management."""
    
    container_s = ControlsignalState


class DataflowState(State):
    """State for Dataflow flow."""
    data_rate: float = 100.0
    latency: float = 0.05
    integrity: float = 1.0


class Dataflow(Flow):
    """Dataflow flow - Data flow for monitoring and control."""
    
    container_s = DataflowState


