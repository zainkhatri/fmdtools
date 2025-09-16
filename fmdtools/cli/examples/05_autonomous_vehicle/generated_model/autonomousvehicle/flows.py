#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flow definitions for AutonomousVehicle model.
"""

from fmdtools.define.flow.base import Flow
from fmdtools.define.container.state import State

class SensordataState(State):
    """State for Sensordata flow."""
    data_rate: float = 1000.0
    latency: float = 0.01
    accuracy: float = 0.95


class Sensordata(Flow):
    """Sensordata flow - Sensor data flow from perception to decision making."""
    
    container_s = SensordataState


class ControlcommandsState(State):
    """State for Controlcommands flow."""
    command_rate: float = 100.0
    latency: float = 0.05
    reliability: float = 0.99


class Controlcommands(Flow):
    """Controlcommands flow - Control commands from decision making to propulsion."""
    
    container_s = ControlcommandsState


class PowerflowState(State):
    """State for Powerflow flow."""
    voltage: float = 400.0
    current: float = 200.0
    efficiency: float = 0.92


class Powerflow(Flow):
    """Powerflow flow - Electrical power flow through the vehicle."""
    
    container_s = PowerflowState


class SafetysignalsState(State):
    """State for Safetysignals flow."""
    signal_strength: float = 1.0
    response_time: float = 0.001
    priority: float = 1.0


class Safetysignals(Flow):
    """Safetysignals flow - Safety signals and emergency commands."""
    
    container_s = SafetysignalsState


