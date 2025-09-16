#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Coolingsystem function for AircraftEngine model.

Engine cooling and thermal management"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class CoolingsystemState(State):
    """State for Coolingsystem function."""
    coolant_temperature: float = 90.0
    flow_rate: float = 100.0
    pressure: float = 5.0
    heat_exchanger_efficiency: float = 0.85

class CoolingsystemMode(Mode):
    """Mode for Coolingsystem function."""
    failrate = 1e-5
    fault_coolant_pump_failure = (1e-6,)
    fault_radiator_clog = (1e-6,)
    fault_thermostat_failure = (1e-6,)
    fault_coolant_leak = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Coolingsystem(Function):
    """Coolingsystem function implementation."""
    container_s = CoolingsystemState
    container_m = CoolingsystemMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('coolant_pump_failure'):
                self._handle_coolant_pump_failure_fault()
            if self.m.has_fault('radiator_clog'):
                self._handle_radiator_clog_fault()
            if self.m.has_fault('thermostat_failure'):
                self._handle_thermostat_failure_fault()
            if self.m.has_fault('coolant_leak'):
                self._handle_coolant_leak_fault()
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

    def _handle_coolant_pump_failure_fault(self):
        """Handle coolant_pump_failure fault."""
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

    def _handle_radiator_clog_fault(self):
        """Handle radiator_clog fault."""
        # Clogged/Blocked fault handling
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.1
        if hasattr(self.s, 'pressure'):
            self.s.pressure *= 1.5  # Back pressure increases
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.2
        if hasattr(self.s, 'status'):
            self.s.status = 0.2

    def _handle_thermostat_failure_fault(self):
        """Handle thermostat_failure fault."""
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

    def _handle_coolant_leak_fault(self):
        """Handle coolant_leak fault."""
        # Leak fault handling
        if hasattr(self.s, 'pressure'):
            self.s.pressure *= 0.6
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 1.5  # Higher flow rate due to leak
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.7
        if hasattr(self.s, 'status'):
            self.s.status = 0.4

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