#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pressurereliefvalve function for HydraulicPump model.

Pressure relief valve for system protection"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class PressurereliefvalveState(State):
    """State for Pressurereliefvalve function."""
    position: float = 50.0
    pressure_drop: float = 10.0
    flow_coefficient: float = 1.0
    response_time: float = 0.1

class PressurereliefvalveMode(Mode):
    """Mode for Pressurereliefvalve function."""
    failrate = 1e-5
    fault_stuck_open = (1e-6,)
    fault_stuck_closed = (1e-6,)
    fault_spring_failure = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Pressurereliefvalve(Function):
    """Pressurereliefvalve function implementation."""
    container_s = PressurereliefvalveState
    container_m = PressurereliefvalveMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('stuck_open'):
                self._handle_stuck_open_fault()
            if self.m.has_fault('stuck_closed'):
                self._handle_stuck_closed_fault()
            if self.m.has_fault('spring_failure'):
                self._handle_spring_failure_fault()
        else:
            # Nominal behavior when no faults present
            self._nominal_behavior()

    def _nominal_behavior(self):
        """Nominal behavior implementation."""
        # Valve/Control nominal behavior
        if hasattr(self.s, 'position') and hasattr(self.s, 'flow_coefficient'):
            # Flow coefficient based on valve position
            self.s.flow_coefficient = (self.s.position / 100.0) * 1.5
            
        if hasattr(self.s, 'pressure_drop') and hasattr(self.s, 'position'):
            # Pressure drop varies with position
            opening_factor = self.s.position / 100.0
            self.s.pressure_drop = 50.0 * (1.0 - opening_factor)
            
        if hasattr(self.s, 'efficiency'):
            # Efficiency based on position (partial opening reduces efficiency)
            opening_factor = getattr(self.s, 'position', 50.0) / 100.0
            self.s.efficiency = 0.95 - abs(0.5 - opening_factor) * 0.2

        
        # Always update efficiency and status for all components
        if hasattr(self.s, 'efficiency'):
            # Slight efficiency degradation over time (wear)
            self.s.efficiency = max(0.5, self.s.efficiency - 0.0001)
            
        if hasattr(self.s, 'status'):
            # Status remains operational if no faults
            self.s.status = 1.0

    def _handle_stuck_open_fault(self):
        """Handle stuck_open fault."""
        # Stuck/Jammed fault handling
        if hasattr(self.s, 'position'):
            # Position becomes fixed
            pass  # Position doesn't change
        if hasattr(self.s, 'flow_coefficient'):
            self.s.flow_coefficient = 0.0
        if hasattr(self.s, 'rpm'):
            self.s.rpm = 0.0
        if hasattr(self.s, 'status'):
            self.s.status = 0.0

    def _handle_stuck_closed_fault(self):
        """Handle stuck_closed fault."""
        # Stuck/Jammed fault handling
        if hasattr(self.s, 'position'):
            # Position becomes fixed
            pass  # Position doesn't change
        if hasattr(self.s, 'flow_coefficient'):
            self.s.flow_coefficient = 0.0
        if hasattr(self.s, 'rpm'):
            self.s.rpm = 0.0
        if hasattr(self.s, 'status'):
            self.s.status = 0.0

    def _handle_spring_failure_fault(self):
        """Handle spring_failure fault."""
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
        
        # Valve dynamics
        if hasattr(self.s, 'position'):
            # Position control dynamics (if not stuck)
            if not self.m.has_fault('stuck') and not self.m.has_fault('jam'):
                # Smooth position changes
                target_position = 50.0  # Default middle position
                position_rate = (target_position - self.s.position) * 0.1
                self.s.position += position_rate * dt


    def classify(self, nominal_history=None, scenario=None):
        """Classify simulation results."""
        # Default implementation - can be overridden for specific behavior
        if self.m.has_fault():
            return "faulty"
        return "nominal"