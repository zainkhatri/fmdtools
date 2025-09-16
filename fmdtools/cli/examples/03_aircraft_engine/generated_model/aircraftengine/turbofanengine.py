#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Turbofanengine function for AircraftEngine model.

Main turbofan engine with thrust generation and fuel consumption"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class TurbofanengineState(State):
    """State for Turbofanengine function."""
    thrust: float = 50000.0
    fuel_consumption: float = 2000.0
    temperature: float = 800.0
    pressure: float = 15.0
    efficiency: float = 0.35
    rpm: float = 12000.0
    bypass_ratio: float = 8.0

class TurbofanengineMode(Mode):
    """Mode for Turbofanengine function."""
    failrate = 1e-5
    fault_compressor_stall = (1e-6,)
    fault_turbine_failure = (1e-6,)
    fault_combustion_chamber_failure = (1e-6,)
    fault_fan_blade_damage = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Turbofanengine(Function):
    """Turbofanengine function implementation."""
    container_s = TurbofanengineState
    container_m = TurbofanengineMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('compressor_stall'):
                self._handle_compressor_stall_fault()
            if self.m.has_fault('turbine_failure'):
                self._handle_turbine_failure_fault()
            if self.m.has_fault('combustion_chamber_failure'):
                self._handle_combustion_chamber_failure_fault()
            if self.m.has_fault('fan_blade_damage'):
                self._handle_fan_blade_damage_fault()
        else:
            # Nominal behavior when no faults present
            self._nominal_behavior()

    def _nominal_behavior(self):
        """Nominal behavior implementation."""
        # Engine/Motor nominal behavior
        if hasattr(self.s, 'rpm') and hasattr(self.s, 'temperature'):
            # Temperature increases with RPM
            target_temp = 90.0 + (self.s.rpm - 800) * 0.01
            self.s.temperature += (target_temp - self.s.temperature) * 0.1
            
        if hasattr(self.s, 'power_output') and hasattr(self.s, 'rpm') and hasattr(self.s, 'efficiency'):
            # Power output based on RPM and efficiency
            base_power = (self.s.rpm / 1800.0) * 200.0
            self.s.power_output = base_power * self.s.efficiency
            
        if hasattr(self.s, 'fuel_level') and hasattr(self.s, 'rpm'):
            # Fuel consumption
            fuel_rate = (self.s.rpm / 1800.0) * 0.1
            self.s.fuel_level = max(0, self.s.fuel_level - fuel_rate * 0.01)
            
        if hasattr(self.s, 'oil_pressure') and hasattr(self.s, 'rpm'):
            # Oil pressure varies with RPM
            self.s.oil_pressure = 30.0 + (self.s.rpm / 1800.0) * 20.0

        
        # Always update efficiency and status for all components
        if hasattr(self.s, 'efficiency'):
            # Slight efficiency degradation over time (wear)
            self.s.efficiency = max(0.5, self.s.efficiency - 0.0001)
            
        if hasattr(self.s, 'status'):
            # Status remains operational if no faults
            self.s.status = 1.0

    def _handle_compressor_stall_fault(self):
        """Handle compressor_stall fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "compressor_stall":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

    def _handle_turbine_failure_fault(self):
        """Handle turbine_failure fault."""
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

    def _handle_combustion_chamber_failure_fault(self):
        """Handle combustion_chamber_failure fault."""
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

    def _handle_fan_blade_damage_fault(self):
        """Handle fan_blade_damage fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "fan_blade_damage":
            self.s.temperature *= 1.1
        if hasattr(self.s, 'status'):
            self.s.status = 0.5

    def dynamic_behavior(self):
        """Dynamic behavior implementation."""
        dt = 1.0  # Time step
        
        # Engine/Motor dynamics
        if hasattr(self.s, 'rpm') and not self.m.has_fault():
            # RPM dynamics
            rpm_rate = (1800.0 - self.s.rpm) * 0.1
            self.s.rpm = max(0, self.s.rpm + rpm_rate * dt)
            
        if hasattr(self.s, 'temperature'):
            # Temperature dynamics with cooling
            cooling_rate = (self.s.temperature - 25.0) * 0.02
            self.s.temperature = max(25.0, self.s.temperature - cooling_rate * dt)


    def classify(self, nominal_history=None, scenario=None):
        """Classify simulation results."""
        # Default implementation - can be overridden for specific behavior
        if self.m.has_fault():
            return "faulty"
        return "nominal"