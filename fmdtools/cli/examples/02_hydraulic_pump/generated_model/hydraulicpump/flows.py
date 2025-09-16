#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flow definitions for HydraulicPump model.
"""

from fmdtools.define.flow.base import Flow
from fmdtools.define.container.state import State

class HydraulicflowState(State):
    """State for Hydraulicflow flow."""
    flow_rate: float = 20.0
    pressure: float = 100.0
    temperature: float = 45.0


class Hydraulicflow(Flow):
    """Hydraulicflow flow - Main hydraulic fluid flow from pump to valve."""
    
    container_s = HydraulicflowState


class ReturnflowState(State):
    """State for Returnflow flow."""
    flow_rate: float = 18.0
    pressure: float = 5.0
    temperature: float = 50.0


class Returnflow(Flow):
    """Returnflow flow - Return flow from valve to reservoir."""
    
    container_s = ReturnflowState


