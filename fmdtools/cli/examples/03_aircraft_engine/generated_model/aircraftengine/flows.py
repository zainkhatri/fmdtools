#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flow definitions for AircraftEngine model.
"""

from fmdtools.define.flow.base import Flow
from fmdtools.define.container.state import State

class FuelflowState(State):
    """State for Fuelflow flow."""
    flow_rate: float = 2000.0
    pressure: float = 300.0
    temperature: float = 20.0


class Fuelflow(Flow):
    """Fuelflow flow - Fuel delivery from fuel system to engine."""
    
    container_s = FuelflowState


class AirflowState(State):
    """State for Airflow flow."""
    flow_rate: float = 500.0
    pressure: float = 15.0
    temperature: float = 25.0


class Airflow(Flow):
    """Airflow flow - Air intake and compression flow."""
    
    container_s = AirflowState


class CoolantflowState(State):
    """State for Coolantflow flow."""
    flow_rate: float = 100.0
    temperature: float = 90.0
    pressure: float = 5.0


class Coolantflow(Flow):
    """Coolantflow flow - Coolant circulation for thermal management."""
    
    container_s = CoolantflowState


class ExhaustflowState(State):
    """State for Exhaustflow flow."""
    flow_rate: float = 700.0
    temperature: float = 600.0
    pressure: float = 2.0


class Exhaustflow(Flow):
    """Exhaustflow flow - Exhaust gases and thrust output."""
    
    container_s = ExhaustflowState


