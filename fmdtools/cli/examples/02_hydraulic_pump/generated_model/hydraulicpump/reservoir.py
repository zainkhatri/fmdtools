#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reservoir function for HydraulicPump model.

Hydraulic fluid reservoir with level and contamination monitoring"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class ReservoirState(State):
    """State for Reservoir function."""
    fluid_level: float = 80.0
    temperature: float = 30.0
    pressure: float = 1.0
    contamination: float = 0.01

class ReservoirMode(Mode):
    """Mode for Reservoir function."""
    failrate = 1e-5
    fault_leak = (1e-6,)
    fault_contamination = (1e-6,)
    fault_overheating = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Reservoir(Function):
    """Reservoir function implementation."""
    container_s = ReservoirState
    container_m = ReservoirMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('leak'):
                self._handle_leak_fault()
            if self.m.has_fault('contamination'):
                self._handle_contamination_fault()
            if self.m.has_fault('overheating'):
                self._handle_overheating_fault()
        else:
            # Nominal behavior when no faults present
            self._nominal_behavior()

    def _nominal_behavior(self):
        """Nominal behavior implementation."""
        # Generic component nominal behavior
        if hasattr(self.s, 'temperature'):
            # Temperature regulation toward ambient
            ambient_temp = 25.0
            self.s.temperature += (ambient_temp - self.s.temperature) * 0.02
            
        if hasattr(self.s, 'pressure'):
            # Maintain pressure within operating range
            target_pressure = 100.0
            self.s.pressure += (target_pressure - self.s.pressure) * 0.05
            
        if hasattr(self.s, 'flow_rate') and hasattr(self.s, 'pressure'):
            # Flow rate proportional to pressure
            self.s.flow_rate = (self.s.pressure / 100.0) * 10.0
            
        if hasattr(self.s, 'power_consumption'):
            # Baseline power consumption
            self.s.power_consumption = 1000.0
        
        # Always update efficiency and status for all components
        if hasattr(self.s, 'efficiency'):
            # Slight efficiency degradation over time (wear)
            self.s.efficiency = max(0.5, self.s.efficiency - 0.0001)
            
        if hasattr(self.s, 'status'):
            # Status remains operational if no faults
            self.s.status = 1.0

    def _handle_leak_fault(self):
        """Handle leak fault."""
        # Leak fault handling
        if hasattr(self.s, 'pressure'):
            self.s.pressure *= 0.6
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 1.5  # Higher flow rate due to leak
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.7
        if hasattr(self.s, 'status'):
            self.s.status = 0.4

    def _handle_contamination_fault(self):
        """Handle contamination fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "contamination":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

    def _handle_overheating_fault(self):
        """Handle overheating fault."""
        # Overheating fault handling
        if hasattr(self.s, 'temperature'):
            self.s.temperature = min(self.s.temperature * 1.2, 150.0)
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.3
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.5
        if hasattr(self.s, 'status'):
            self.s.status = 0.3

    def dynamic_behavior(self):
        """Dynamic behavior implementation."""
        dt = 1.0  # Time step
        
        # Generic component dynamics
        if hasattr(self.s, 'temperature'):
            # Temperature dynamics toward ambient
            cooling_rate = (self.s.temperature - 25.0) * 0.01
            self.s.temperature += -cooling_rate * dt
            
        if hasattr(self.s, 'pressure'):
            # Pressure fluctuations
            pressure_noise = (np.random.random() - 0.5) * 1.0
            self.s.pressure += pressure_noise * dt

    def classify(self, nominal_history=None, scenario=None):
        """Classify simulation results."""
        # Default implementation - can be overridden for specific behavior
        if self.m.has_fault():
            return "faulty"
        return "nominal"