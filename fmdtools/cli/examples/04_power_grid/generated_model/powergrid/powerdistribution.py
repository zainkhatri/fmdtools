#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Powerdistribution function for PowerGrid model.

Power distribution network with voltage and load management"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class PowerdistributionState(State):
    """State for Powerdistribution function."""
    voltage: float = 138.0
    current: float = 1000.0
    load_balance: float = 1.0
    grid_frequency: float = 60.0
    transmission_losses: float = 0.05

class PowerdistributionMode(Mode):
    """Mode for Powerdistribution function."""
    failrate = 1e-5
    fault_transformer_failure = (1e-6,)
    fault_transmission_line_failure = (1e-6,)
    fault_voltage_regulation_failure = (1e-6,)
    fault_frequency_instability = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Powerdistribution(Function):
    """Powerdistribution function implementation."""
    container_s = PowerdistributionState
    container_m = PowerdistributionMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('transformer_failure'):
                self._handle_transformer_failure_fault()
            if self.m.has_fault('transmission_line_failure'):
                self._handle_transmission_line_failure_fault()
            if self.m.has_fault('voltage_regulation_failure'):
                self._handle_voltage_regulation_failure_fault()
            if self.m.has_fault('frequency_instability'):
                self._handle_frequency_instability_fault()
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

    def _handle_transformer_failure_fault(self):
        """Handle transformer_failure fault."""
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

    def _handle_transmission_line_failure_fault(self):
        """Handle transmission_line_failure fault."""
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

    def _handle_voltage_regulation_failure_fault(self):
        """Handle voltage_regulation_failure fault."""
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

    def _handle_frequency_instability_fault(self):
        """Handle frequency_instability fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "frequency_instability":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

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