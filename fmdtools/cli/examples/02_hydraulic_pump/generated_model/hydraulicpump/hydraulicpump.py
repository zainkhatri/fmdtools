#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hydraulicpump function for HydraulicPump model.

Main hydraulic pump with pressure and flow control"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class HydraulicpumpState(State):
    """State for Hydraulicpump function."""
    rpm: float = 1500.0
    pressure: float = 100.0
    flow_rate: float = 20.0
    temperature: float = 45.0
    efficiency: float = 0.88
    vibration: float = 0.1

class HydraulicpumpMode(Mode):
    """Mode for Hydraulicpump function."""
    failrate = 1e-5
    fault_cavitation = (1e-6,)
    fault_seal_leak = (1e-6,)
    fault_bearing_wear = (1e-6,)
    fault_motor_failure = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Hydraulicpump(Function):
    """Hydraulicpump function implementation."""
    container_s = HydraulicpumpState
    container_m = HydraulicpumpMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('cavitation'):
                self._handle_cavitation_fault()
            if self.m.has_fault('seal_leak'):
                self._handle_seal_leak_fault()
            if self.m.has_fault('bearing_wear'):
                self._handle_bearing_wear_fault()
            if self.m.has_fault('motor_failure'):
                self._handle_motor_failure_fault()
        else:
            # Nominal behavior when no faults present
            self._nominal_behavior()

    def _nominal_behavior(self):
        """Nominal behavior implementation."""
        # Pump/Hydraulic nominal behavior
        if hasattr(self.s, 'pressure') and hasattr(self.s, 'flow_rate'):
            # Pressure-flow relationship
            self.s.pressure = 50.0 + self.s.flow_rate * 5.0
            
        if hasattr(self.s, 'temperature') and hasattr(self.s, 'flow_rate'):
            # Temperature increases with flow rate (friction)
            self.s.temperature = 25.0 + self.s.flow_rate * 1.5
            
        if hasattr(self.s, 'vibration') and hasattr(self.s, 'pressure'):
            # Vibration increases with pressure
            self.s.vibration = 0.05 + (self.s.pressure / 100.0) * 0.05
            
        if hasattr(self.s, 'efficiency'):
            # Efficiency degrades slightly with high pressure
            pressure_factor = getattr(self.s, 'pressure', 100.0) / 100.0
            self.s.efficiency = max(0.5, 0.9 - (pressure_factor - 1.0) * 0.1)

        
        # Always update efficiency and status for all components
        if hasattr(self.s, 'efficiency'):
            # Slight efficiency degradation over time (wear)
            self.s.efficiency = max(0.5, self.s.efficiency - 0.0001)
            
        if hasattr(self.s, 'status'):
            # Status remains operational if no faults
            self.s.status = 1.0

    def _handle_cavitation_fault(self):
        """Handle cavitation fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "cavitation":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

    def _handle_seal_leak_fault(self):
        """Handle seal_leak fault."""
        # Leak fault handling
        if hasattr(self.s, 'pressure'):
            self.s.pressure *= 0.6
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 1.5  # Higher flow rate due to leak
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.7
        if hasattr(self.s, 'status'):
            self.s.status = 0.4

    def _handle_bearing_wear_fault(self):
        """Handle bearing_wear fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "bearing_wear":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

    def _handle_motor_failure_fault(self):
        """Handle motor_failure fault."""
        # Mechanical failure handling
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.1
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency = 0.0
        if hasattr(self.s, 'rpm'):
            self.s.rpm = max(self.s.rpm * 0.5, 0)
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.2
        if hasattr(self.s, 'status'):
            self.s.status = 0.0

    def dynamic_behavior(self):
        """Dynamic behavior implementation."""
        dt = 1.0  # Time step
        
        # Pump dynamics
        if hasattr(self.s, 'pressure'):
            # Pressure buildup dynamics
            target_pressure = getattr(self.s, 'flow_rate', 10.0) * 10.0
            pressure_rate = (target_pressure - self.s.pressure) * 0.2
            self.s.pressure += pressure_rate * dt
            
        if hasattr(self.s, 'vibration'):
            # Vibration dynamics
            self.s.vibration += (np.random.random() - 0.5) * 0.01


    def classify(self, nominal_history=None, scenario=None):
        """Classify simulation results."""
        # Default implementation - can be overridden for specific behavior
        if self.m.has_fault():
            return "faulty"
        return "nominal"