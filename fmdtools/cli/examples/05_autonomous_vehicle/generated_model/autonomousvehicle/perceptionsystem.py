#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Perceptionsystem function for AutonomousVehicle model.

Multi-sensor perception system with camera, lidar, and radar"""

from fmdtools.define.block.function import Function
from fmdtools.define.container.state import State
from fmdtools.define.container.mode import Mode
import numpy as np

class PerceptionsystemState(State):
    """State for Perceptionsystem function."""
    camera_quality: float = 1.0
    lidar_range: float = 200.0
    radar_detection: float = 1.0
    sensor_fusion_accuracy: float = 0.95
    object_detection_rate: float = 0.98

class PerceptionsystemMode(Mode):
    """Mode for Perceptionsystem function."""
    failrate = 1e-5
    fault_camera_failure = (1e-6,)
    fault_lidar_failure = (1e-6,)
    fault_radar_failure = (1e-6,)
    fault_sensor_calibration_drift = (1e-6,)
    fault_weather_impact = (1e-6,)
    default_phases = (('na', 1.0),)
    default_units = 'sec'

class Perceptionsystem(Function):
    """Perceptionsystem function implementation."""
    container_s = PerceptionsystemState
    container_m = PerceptionsystemMode

    def static_behavior(self):
        """Static behavior implementation."""
        
        # Handle fault conditions first
        if self.m.has_fault():
            if self.m.has_fault('camera_failure'):
                self._handle_camera_failure_fault()
            if self.m.has_fault('lidar_failure'):
                self._handle_lidar_failure_fault()
            if self.m.has_fault('radar_failure'):
                self._handle_radar_failure_fault()
            if self.m.has_fault('sensor_calibration_drift'):
                self._handle_sensor_calibration_drift_fault()
            if self.m.has_fault('weather_impact'):
                self._handle_weather_impact_fault()
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

    def _handle_camera_failure_fault(self):
        """Handle camera_failure fault."""
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

    def _handle_lidar_failure_fault(self):
        """Handle lidar_failure fault."""
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

    def _handle_radar_failure_fault(self):
        """Handle radar_failure fault."""
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

    def _handle_sensor_calibration_drift_fault(self):
        """Handle sensor_calibration_drift fault."""
        # Sensor fault handling
        if hasattr(self.s, 'reading'):
            # Erratic readings
            self.s.reading *= (0.5 + np.random.random())
        if hasattr(self.s, 'accuracy'):
            self.s.accuracy *= 0.1
        if hasattr(self.s, 'noise_level'):
            self.s.noise_level *= 10.0
        if hasattr(self.s, 'status'):
            self.s.status = 0.1

    def _handle_weather_impact_fault(self):
        """Handle weather_impact fault."""
        # Generic fault handling
        if hasattr(self.s, 'efficiency'):
            self.s.efficiency *= 0.5
        if hasattr(self.s, 'power_output'):
            self.s.power_output *= 0.3
        if hasattr(self.s, 'flow_rate'):
            self.s.flow_rate *= 0.7
        if hasattr(self.s, 'temperature') and "heat" not in "weather_impact":
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