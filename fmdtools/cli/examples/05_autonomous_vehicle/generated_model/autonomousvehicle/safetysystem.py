#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Safetysystem function for AutonomousVehicle model.

Safety and fail-safe mechanisms"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class SafetysystemState(State):
    """State for Safetysystem function."""
    emergency_braking: float = 1.0
    stability_control: float = 1.0
    collision_avoidance: float = 1.0
    fail_safe_status: float = 1.0
    safety_margin: float = 0.9

class SafetysystemMode(Mode):
    """Mode for Safetysystem function."""
    failrate = 1e-5
    fault_brake_system_failure = (1e-6,)
    fault_stability_control_failure = (1e-6,)
    fault_collision_avoidance_failure = (1e-6,)
    fault_fail_safe_override = (1e-6,)
    fault_safety_system_timeout = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Safetysystem(Function):
    """Safetysystem function implementation."""
    container_s = SafetysystemState
    container_m = SafetysystemMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('brake_system_failure'):
                self._handle_brake_system_failure_fault()
            if self.m.has_fault('stability_control_failure'):
                self._handle_stability_control_failure_fault()
            if self.m.has_fault('collision_avoidance_failure'):
                self._handle_collision_avoidance_failure_fault()
            if self.m.has_fault('fail_safe_override'):
                self._handle_fail_safe_override_fault()
            if self.m.has_fault('safety_system_timeout'):
                self._handle_safety_system_timeout_fault()
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

    def _handle_brake_system_failure_fault(self):
        """Handle brake_system_failure fault."""
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

    def _handle_stability_control_failure_fault(self):
        """Handle stability_control_failure fault."""
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

    def _handle_collision_avoidance_failure_fault(self):
        """Handle collision_avoidance_failure fault."""
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

    def _handle_fail_safe_override_fault(self):
        """Handle fail_safe_override fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "fail_safe_override":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

    def _handle_safety_system_timeout_fault(self):
        """Handle safety_system_timeout fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "safety_system_timeout":
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