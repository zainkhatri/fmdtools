#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intelligent conversational fmdtools model builder.
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from pydantic import ValidationError
from .core import (
    LevelSpec, FunctionSpec, FlowSpec, ArchitectureSpec, 
    SimulationSpec, ConnectionSpec, Fault, render_level, 
    sanitize_identifier, sanitize_class_name
)


class IntelligentBuilder:
    """Intelligent conversational fmdtools model builder."""
    
    def __init__(self, xml_file: Optional[Path] = None):
        self.spec: Optional[LevelSpec] = None
        self.last_spec: Optional[LevelSpec] = None
        self.conversation_history: List[str] = []
        self.extracted_info: Dict[str, Any] = {
            "components": {},
            "states": {},
            "faults": {},
            "flows": {},
            "connections": [],
            "system_name": "",
            "description": ""
        }
        
        # Initialize from XML if provided
        if xml_file and xml_file.exists():
            self._load_from_xml(xml_file)
    
    def _load_from_xml(self, xml_file: Path):
        """Load partial spec from Draw.io or Gaphor XML."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            functions = []
            flows = []
            
            # Basic XML parsing - can be enhanced for specific formats
            for elem in root.iter():
                if 'function' in elem.tag.lower() or 'component' in elem.tag.lower():
                    name = elem.get('name', elem.text or f"Function{len(functions)+1}")
                    functions.append(FunctionSpec(name=sanitize_class_name(name)))
                elif 'flow' in elem.tag.lower():
                    name = elem.get('name', elem.text or f"Flow{len(flows)+1}")
                    flows.append(FlowSpec(name=sanitize_class_name(name)))
            
            if functions:
                self.spec = LevelSpec(
                    name=sanitize_identifier(xml_file.stem),
                    description=f"Model loaded from {xml_file.name}",
                    functions=functions,
                    flows=flows,
                    architecture=ArchitectureSpec(
                        name=f"{sanitize_class_name(xml_file.stem)}Architecture",
                        functions=[f.name for f in functions],
                        connections=[]
                    ),
                    simulation=SimulationSpec()
                )
                
        except Exception as e:
            print(f"Warning: Could not parse XML file {xml_file}: {e}")
    
    def analyze_input(self, text: str) -> Dict[str, Any]:
        """Intelligently analyze user input to extract meaningful information."""
        text = text.strip()
        analysis = {
            "system_name": None,
            "components": [],
            "states": {},
            "faults": [],
            "flows": [],
            "intent": "describe",  # describe, clarify, generate, question, greeting
            "confidence": 0.0,
            "question_text": "",
            "greeting_text": ""
        }
        
        # Detect greetings and casual conversation FIRST
        greeting_patterns = [
            r"^hi\b", r"^hello\b", r"^hey\b", r"^good morning\b", r"^good afternoon\b",
            r"how are you", r"what's up", r"whats up", r"how's it going", r"hows it going"
        ]
        
        for pattern in greeting_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                analysis["intent"] = "greeting"
                analysis["greeting_text"] = text
                return analysis
        
        # Detect questions - be very broad to catch natural language
        question_patterns = [
            r"can you (?:explain|tell me|clarify|help)",
            r"how (?:do|does|should|can)",
            r"why (?:do|does|should)",
            r"what (?:do|does|should|can|is|are)",
            r"should i (?:add|do|include|give|tell|provide)",
            r"do you think (?:i|we|that)",
            r"(?:need|give you|tell you) more",
            r"you have enough",
            r"(?:that's|thats) enough",
            r"by (?:just )?(?:me )?saying",
            r"what.*(?:\?|mean)",
            r"(?:^|\s)(?:explain|clarify|help)(?:\s|$)",
            r"\?$",  # Any sentence ending with ?
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                analysis["intent"] = "question"
                analysis["question_text"] = text
                return analysis
        
        # Detect intent
        if any(word in text.lower() for word in ['generate', 'create', 'build files', 'make files']):
            analysis["intent"] = "generate"
            return analysis
        
        # Extract system name with better patterns
        name_patterns = [
            r"(?:model|build)\s+(?:a|an|the)?\s*([a-zA-Z0-9\s]+?)\s+(?:system|model|AC|engine|pump|motor|valve|sensor)",
            r"(?:for|of)\s+(?:a|an|the)?\s*([a-zA-Z0-9\s]+?)\s+(?:system|model|AC|engine|pump|motor|valve|sensor)",
            r"(\w+(?:\s+\w+)*)\s+(?:AC|engine|system|model|pump|motor|valve|sensor)",
            r"(?:^|\s)([A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*)*)\s+(?:AC|engine|system|pump|motor|valve|sensor)",
            # Capture system descriptions before "for" applications
            r"([a-zA-Z0-9\s]+?)\s+(?:for|in)\s+(?:a|an|the)?\s*([a-zA-Z0-9\s]+)",
            # Capture descriptive component types
            r"([a-zA-Z]+(?:\s+[a-zA-Z]+)*)\s+(pump|motor|engine|valve|sensor|compressor|fan|turbine)",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Handle patterns with multiple capture groups
                if len(match.groups()) > 1:
                    # For "X for Y" patterns, combine both parts
                    candidate = f"{match.group(1).strip()} {match.group(2).strip()}"
                else:
                    candidate = match.group(1).strip()
                
                if len(candidate.split()) <= 5 and not any(skip in candidate.lower() for skip in ['want', 'need', 'can', 'will', 'have']):
                    analysis["system_name"] = candidate
                    analysis["confidence"] += 0.3
                    break
        
        # Extract components more intelligently
        component_patterns = [
            r"\b(engine|motor|pump|valve|sensor|controller|battery|tank|compressor|fan|alternator|radiator)\b",
            r"\b(AC|air\s+conditioning|cooling|heating)\s+(system|unit|compressor)",
            r"\b(V6|V8|4\s*cylinder|6\s*cylinder|8\s*cylinder)\s+(engine|motor)",
        ]
        
        components = set()
        for pattern in component_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                component = match.group(0).strip()
                # Normalize component names
                if 'engine' in component.lower() or 'cylinder' in component.lower():
                    components.add('Engine')
                elif 'ac' in component.lower() or 'air conditioning' in component.lower():
                    components.add('AcSystem')
                elif 'battery' in component.lower():
                    components.add('Battery')
                elif 'pump' in component.lower():
                    components.add('Pump')
                elif 'compressor' in component.lower():
                    components.add('Compressor')
                else:
                    clean_name = sanitize_class_name(component)
                    if clean_name:
                        components.add(clean_name)
        
        analysis["components"] = list(components)
        if components:
            analysis["confidence"] += 0.4
        
        # Extract states intelligently with enhanced patterns
        state_patterns = [
            # Explicit values: "rpm: 1800", "temperature: 90C", "pressure: 100 PSI"
            r"\b(\w+)\s*:\s*(\d+(?:\.\d+)?)\s*(\w+)?",
            # Range values: "temperature range 80-120C", "pressure 50-200 PSI"
            r"\b(\w+)\s+(?:range\s+)?(\d+(?:\.\d+)?)\s*[-to]\s*(\d+(?:\.\d+)?)\s*(\w+)?",
            # Simple mentions: "temperature", "pressure", "rpm", etc.
            r"\b(temperature|temp|pressure|speed|rpm|voltage|current|flow\s*rate|power|efficiency|displacement|capacity|torque|vibration|accuracy|noise|position|charge|fuel)\b",
            # Technical specifications: "3.7L displacement", "200HP power", "12V system"
            r"\b(\d+(?:\.\d+)?)\s*([A-Z]{1,4}|hp|bhp|kw|psi|bar|gpm|lpm|cfm|hz|khz|mhz)\b",
            # Performance specs: "max RPM", "rated power", "operating pressure"
            r"\b(?:max|min|rated|operating|nominal)\s+(\w+)",
        ]
        
        states = {}
        for pattern in state_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                
                if len(groups) >= 2 and groups[1] and groups[1].replace('.','').isdigit():
                    # Explicit value pattern: "rpm: 1800"
                    state_name = groups[0].lower().replace(' ', '_')
                    value = float(groups[1])
                    
                    # Handle units and convert to standard values
                    unit = groups[2].lower() if len(groups) > 2 and groups[2] else ""
                    if "hp" in unit or "bhp" in unit:
                        state_name = "power_output"
                    elif "psi" in unit or "bar" in unit:
                        state_name = "pressure" 
                    elif "gpm" in unit or "lpm" in unit or "cfm" in unit:
                        state_name = "flow_rate"
                    elif "l" in unit and "displacement" in state_name:
                        state_name = "displacement"
                        value = value * 1000  # Convert to cc
                    
                    states[state_name] = value
                    
                elif len(groups) >= 3 and groups[1] and groups[2]:
                    # Range pattern: "temperature 80-120"
                    state_name = groups[0].lower().replace(' ', '_')
                    min_val = float(groups[1])
                    max_val = float(groups[2])
                    
                    # Use average of range as default value
                    states[state_name] = (min_val + max_val) / 2.0
                    states[f"{state_name}_min"] = min_val
                    states[f"{state_name}_max"] = max_val
                    
                elif len(groups) >= 2 and groups[0].replace('.','').isdigit():
                    # Technical spec pattern: "3.7L", "200HP"
                    value = float(groups[0])
                    unit = groups[1].lower()
                    
                    if unit in ["hp", "bhp", "kw"]:
                        states["power_output"] = value
                    elif unit in ["psi", "bar"]:
                        states["pressure"] = value
                    elif unit in ["gpm", "lpm", "cfm"]:
                        states["flow_rate"] = value
                    elif unit == "l" and "displacement" not in states:
                        states["displacement"] = value * 1000  # Convert to cc
                        
                else:
                    # Simple state name pattern
                    state_name = groups[0].lower().replace(' ', '_')
                    
                    # Assign realistic defaults based on state type
                    defaults = {
                        'temperature': 90.0, 'temp': 90.0,
                        'pressure': 100.0,
                        'rpm': 1800.0, 'speed': 1800.0,
                        'voltage': 12.0,
                        'current': 5.0,
                        'flow_rate': 10.0,
                        'power': 200.0, 'power_output': 200.0,
                        'efficiency': 0.85,
                        'displacement': 3500.0,  # cc
                        'capacity': 100.0,
                        'torque': 300.0,  # Nm
                        'vibration': 0.1,
                        'accuracy': 0.95,
                        'noise': 0.01,
                        'position': 50.0,  # %
                        'charge': 80.0,  # %
                        'fuel': 50.0   # %
                    }
                    
                    if state_name in defaults:
                        states[state_name] = defaults[state_name]
        
        analysis["states"] = states
        if states:
            analysis["confidence"] += 0.2
        
        # Extract faults intelligently
        fault_patterns = [
            r"can\s+(explode|combust|fail|break|malfunction|overheat|leak)",
            r"faults?\s*:\s*([a-zA-Z][a-zA-Z0-9\s,]*)",
            # Comma-separated fault lists (cavitation,seal_leak,motor_failure)
            r"([a-z_]+(?:,[a-z_]+)+)",
            r"\b(explosion|combustion|failure|breakdown|malfunction|overheating|leak|dropout|cavitation|seal_leak|motor_failure)\b",
        ]
        
        faults = set()
        for pattern in fault_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if pattern.startswith("faults?"):
                    # Explicit fault list with "faults:" prefix
                    fault_list = [f.strip() for f in match.group(1).split(',')]
                    for fault in fault_list:
                        if fault:
                            faults.add(fault.lower().replace(' ', '_'))
                elif "," in match.group(0):
                    # Comma-separated fault list (cavitation,seal_leak,motor_failure)
                    fault_list = [f.strip() for f in match.group(0).split(',')]
                    for fault in fault_list:
                        if fault:
                            faults.add(fault.lower().replace(' ', '_'))
                else:
                    fault = match.group(1 if len(match.groups()) >= 1 else 0).lower()
                    if fault in ['explode', 'explosion']:
                        faults.add('explosion')
                    elif fault in ['combust', 'combustion']:
                        faults.add('combustion')
                    elif fault in ['fail', 'failure', 'breakdown']:
                        faults.add('mechanical_failure')
                    elif fault in ['overheat', 'overheating']:
                        faults.add('overheating')
                    elif fault in ['leak']:
                        faults.add('leak')
                    else:
                        faults.add(fault.replace(' ', '_'))
        
        analysis["faults"] = list(faults)
        if faults:
            analysis["confidence"] += 0.1
        
        return analysis
    
    def update_extracted_info(self, analysis: Dict[str, Any]):
        """Update the extracted information based on analysis."""
        if analysis["system_name"] and not self.extracted_info["system_name"]:
            self.extracted_info["system_name"] = analysis["system_name"]
        
        # Update components
        for comp in analysis["components"]:
            if comp not in self.extracted_info["components"]:
                self.extracted_info["components"][comp] = {
                    "states": {},
                    "faults": []
                }
        
        # Update states - distribute to relevant components or all if unclear
        if analysis["states"]:
            if len(self.extracted_info["components"]) == 1:
                # Single component - add all states to it
                comp_name = list(self.extracted_info["components"].keys())[0]
                self.extracted_info["components"][comp_name]["states"].update(analysis["states"])
            else:
                # Multiple components - smart distribution
                for state_name, value in analysis["states"].items():
                    # Distribute states based on relevance
                    if state_name in ['temperature', 'rpm'] and 'Engine' in self.extracted_info["components"]:
                        self.extracted_info["components"]["Engine"]["states"][state_name] = value
                    elif state_name in ['pressure'] and any('Ac' in comp for comp in self.extracted_info["components"]):
                        for comp in self.extracted_info["components"]:
                            if 'Ac' in comp:
                                self.extracted_info["components"][comp]["states"][state_name] = value
                    else:
                        # Add to all components as fallback
                        for comp in self.extracted_info["components"]:
                            self.extracted_info["components"][comp]["states"][state_name] = value
        
        # Update faults - distribute to relevant components
        if analysis["faults"]:
            if len(self.extracted_info["components"]) == 1:
                comp_name = list(self.extracted_info["components"].keys())[0]
                self.extracted_info["components"][comp_name]["faults"].extend(analysis["faults"])
            else:
                # Smart fault distribution
                for fault in analysis["faults"]:
                    if fault in ['explosion', 'combustion', 'mechanical_failure'] and 'Engine' in self.extracted_info["components"]:
                        self.extracted_info["components"]["Engine"]["faults"].append(fault)
                    else:
                        # Add to all components as fallback
                        for comp in self.extracted_info["components"]:
                            self.extracted_info["components"][comp]["faults"].append(fault)
        
        # Remove duplicates
        for comp_info in self.extracted_info["components"].values():
            comp_info["faults"] = list(set(comp_info["faults"]))
    
    def build_spec(self) -> Optional[LevelSpec]:
        """Build LevelSpec from extracted information."""
        if not self.extracted_info["system_name"] or not self.extracted_info["components"]:
            return None
        
        # Create functions with enhanced details
        functions = []
        for comp_name, comp_info in self.extracted_info["components"].items():
            if comp_info["states"] or comp_info["faults"]:  # Only create if we have some info
                # Enhance states with realistic defaults and relationships
                enhanced_states = self._enhance_states(comp_name, comp_info["states"])
                
                # Create faults with realistic failure rates
                faults = [Fault(name=f) for f in comp_info["faults"]]
                
                # Add component-specific description
                description = self._generate_component_description(comp_name, enhanced_states, comp_info["faults"])
                
                functions.append(FunctionSpec(
                    name=comp_name,
                    description=description,
                    states=enhanced_states,
                    faults=faults,
                    modes=["nominal", "degraded", "failed"]  # Add realistic modes
                ))
        
        if not functions:
            return None
        
        # Create flows for multi-component systems
        flows = self._create_realistic_flows(functions)
        
        # Create connections between functions
        connections = self._create_realistic_connections(functions, flows)
        
        # Create architecture
        architecture = ArchitectureSpec(
            name=f"{sanitize_class_name(self.extracted_info['system_name'])}Architecture",
            functions=[f.name for f in functions],
            connections=connections
        )
        
        # Create spec with enhanced simulation settings
        try:
            spec = LevelSpec(
                name=sanitize_identifier(self.extracted_info["system_name"]),
                description=self._generate_system_description(),
                functions=functions,
                flows=flows,
                architecture=architecture,
                simulation=SimulationSpec(
                    sample_run=True, 
                    fault_analysis=True,
                    parameter_study=True,
                    end_time=100.0,
                    time_step=1.0
                )
            )
            return spec
        except ValidationError as e:
            return None
    
    def _enhance_states(self, comp_name: str, states: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance states with realistic values and additional derived states for ANY component."""
        enhanced = states.copy()
        
        # Always add efficiency and status for all components
        if "efficiency" not in enhanced:
            enhanced["efficiency"] = 0.85  # Default efficiency
        if "status" not in enhanced:
            enhanced["status"] = 1.0  # 1=operational, 0=failed
        
        # Engine-specific enhancements
        if "engine" in comp_name.lower() or "motor" in comp_name.lower():
            if "rpm" not in enhanced:
                enhanced["rpm"] = 1800.0
            if "temperature" not in enhanced:
                enhanced["temperature"] = 90.0
            if "fuel_level" not in enhanced and not any("fuel" in k.lower() for k in enhanced.keys()):
                enhanced["fuel_level"] = 50.0
            if "oil_pressure" not in enhanced:
                enhanced["oil_pressure"] = 40.0
            if "power_output" not in enhanced:
                enhanced["power_output"] = 200.0
                
        # AC/Climate system enhancements
        elif "ac" in comp_name.lower() or "air" in comp_name.lower() or "climate" in comp_name.lower():
            if "temperature" not in enhanced:
                enhanced["temperature"] = 22.0
            if "pressure" not in enhanced:
                enhanced["pressure"] = 250.0
            if "flow_rate" not in enhanced:
                enhanced["flow_rate"] = 15.0
            if "power_consumption" not in enhanced:
                enhanced["power_consumption"] = 2500.0
                
        # Battery/Electrical enhancements
        elif "battery" in comp_name.lower() or "electrical" in comp_name.lower():
            if "voltage" not in enhanced:
                enhanced["voltage"] = 12.6
            if "current" not in enhanced:
                enhanced["current"] = 0.0
            if "charge_level" not in enhanced:
                enhanced["charge_level"] = 80.0
            if "temperature" not in enhanced:
                enhanced["temperature"] = 25.0
                
        # Pump/Hydraulic system enhancements
        elif "pump" in comp_name.lower() or "hydraulic" in comp_name.lower():
            if "pressure" not in enhanced:
                enhanced["pressure"] = 100.0
            if "flow_rate" not in enhanced:
                enhanced["flow_rate"] = 10.0
            if "temperature" not in enhanced:
                enhanced["temperature"] = 40.0
            if "vibration" not in enhanced:
                enhanced["vibration"] = 0.1
                
        # Valve/Control system enhancements  
        elif "valve" in comp_name.lower() or "control" in comp_name.lower():
            if "position" not in enhanced:
                enhanced["position"] = 50.0  # Percent open
            if "pressure_drop" not in enhanced:
                enhanced["pressure_drop"] = 10.0
            if "flow_coefficient" not in enhanced:
                enhanced["flow_coefficient"] = 1.0
                
        # Sensor enhancements
        elif "sensor" in comp_name.lower():
            if "reading" not in enhanced:
                enhanced["reading"] = 1.0
            if "accuracy" not in enhanced:
                enhanced["accuracy"] = 0.95
            if "noise_level" not in enhanced:
                enhanced["noise_level"] = 0.01
                
        # Generic component enhancements
        else:
            # Add temperature if not present (most components have thermal behavior)
            if "temperature" not in enhanced:
                enhanced["temperature"] = 25.0
            
            # Add pressure if it seems flow-related
            if any(word in comp_name.lower() for word in ["flow", "fluid", "gas", "liquid"]):
                if "pressure" not in enhanced:
                    enhanced["pressure"] = 100.0
                if "flow_rate" not in enhanced:
                    enhanced["flow_rate"] = 5.0
            
            # Add power consumption for active components
            if any(word in comp_name.lower() for word in ["compressor", "fan", "heater", "cooler"]):
                if "power_consumption" not in enhanced:
                    enhanced["power_consumption"] = 1000.0
        
        return enhanced
    
    def _create_realistic_flows(self, functions: List[FunctionSpec]) -> List[FlowSpec]:
        """Create realistic flows between components."""
        flows = []
        
        # Determine what flows are needed based on components
        component_names = [f.name for f in functions]
        
        if "Engine" in component_names:
            flows.append(FlowSpec(
                name="FuelFlow",
                description="Fuel delivery to engine",
                vars={"flow_rate": 10.0, "pressure": 60.0, "temperature": 25.0}
            ))
            flows.append(FlowSpec(
                name="ExhaustFlow", 
                description="Exhaust gases from engine",
                vars={"flow_rate": 200.0, "temperature": 400.0, "pressure": 14.7}
            ))
            flows.append(FlowSpec(
                name="CoolantFlow",
                description="Engine coolant circulation",
                vars={"flow_rate": 50.0, "temperature": 90.0, "pressure": 15.0}
            ))
            
        if any("Ac" in name or "Air" in name for name in component_names):
            flows.append(FlowSpec(
                name="RefrigerantFlow",
                description="AC refrigerant circulation", 
                vars={"flow_rate": 5.0, "pressure": 250.0, "temperature": -10.0}
            ))
            flows.append(FlowSpec(
                name="AirFlow",
                description="Conditioned air flow",
                vars={"flow_rate": 300.0, "temperature": 22.0, "humidity": 50.0}
            ))
            
        if "Battery" in component_names or "Engine" in component_names:
            flows.append(FlowSpec(
                name="ElectricalPower",
                description="Electrical power distribution",
                vars={"voltage": 12.0, "current": 100.0, "power": 1200.0}
            ))
        
        return flows
    
    def _create_realistic_connections(self, functions: List[FunctionSpec], flows: List[FlowSpec]) -> List[ConnectionSpec]:
        """Create realistic connections between components."""
        connections = []
        
        if not flows:
            return connections
            
        component_names = [f.name for f in functions]
        flow_names = [f.name for f in flows]
        
        # Engine connections
        if "Engine" in component_names:
            for flow_name in flow_names:
                if flow_name in ["FuelFlow", "CoolantFlow"]:
                    connections.append(ConnectionSpec(
                        from_fn="Engine", to_fn="Engine", flow_name=flow_name
                    ))
                elif flow_name == "ElectricalPower" and "Battery" in component_names:
                    connections.append(ConnectionSpec(
                        from_fn="Engine", to_fn="Battery", flow_name=flow_name
                    ))
        
        # AC system connections 
        ac_components = [name for name in component_names if "Ac" in name or "Air" in name]
        if ac_components and "RefrigerantFlow" in flow_names:
            for ac_comp in ac_components:
                connections.append(ConnectionSpec(
                    from_fn=ac_comp, to_fn=ac_comp, flow_name="RefrigerantFlow"
                ))
        
        return connections
    
    def _generate_component_description(self, comp_name: str, states: Dict[str, Any], faults: List[str]) -> str:
        """Generate detailed component description."""
        if comp_name == "Engine":
            return f"Internal combustion engine with {len(states)} monitored states including RPM, temperature, and fuel systems. Critical faults: {', '.join(faults) if faults else 'mechanical failure, overheating'}."
        elif "Ac" in comp_name:
            return f"Air conditioning system managing cabin climate with refrigerant circulation and temperature control. Monitors {len(states)} states for optimal performance."
        elif comp_name == "Battery":
            return f"Vehicle electrical storage system with {len(states)} monitored parameters including voltage, current, and charge level."
        else:
            return f"{comp_name} component with {len(states)} state variables and {len(faults)} fault modes."
    
    def _generate_system_description(self) -> str:
        """Generate comprehensive system description."""
        system_name = self.extracted_info["system_name"]
        components = list(self.extracted_info["components"].keys())
        
        if "Engine" in components and any("Ac" in c for c in components):
            return f"{system_name} automotive system model including engine management and climate control subsystems with realistic fault modeling and state monitoring."
        elif "Engine" in components:
            return f"{system_name} engine system model with comprehensive state monitoring, fault detection, and performance analysis capabilities."
        else:
            return f"{system_name} system model with {len(components)} interconnected components: {', '.join(components)}."
    
    def generate_intelligent_response(self, analysis: Dict[str, Any]) -> str:
        """Generate intelligent response based on analysis and current state."""
        
        # Handle greetings naturally and conversationally
        if analysis.get("intent") == "greeting":
            return "Hi there! I'm here to help you build fmdtools models. What kind of system would you like to work on today? Could be anything - a car engine, a pump, a robot, whatever interests you!"
        
        # ALWAYS check for questions FIRST - even if we think we're ready
        if analysis.get("intent") == "question":
            return self._answer_user_question(analysis.get("question_text", ""))
        
        # Also check if they're asking questions even if not detected in intent
        question_text = (analysis.get("question_text") or "").lower()
        user_text = (analysis.get("system_name") or "").lower() + " " + " ".join(analysis.get("components") or []).lower()
        combined_text = (question_text + " " + user_text).lower()
        
        if any(phrase in combined_text for phrase in ["should i", "do you think", "need more", "enough", "what do you think", "you have enough", "by just me saying"]):
            return self._answer_user_question(combined_text)
        
        if analysis["intent"] == "generate":
            if self.spec and self.is_ready():
                return "generate"
            else:
                missing = self.get_missing_info()
                return f"I need more information before generating:\n{missing}\n\nPlease provide the missing details."
        
        # Update our knowledge
        self.update_extracted_info(analysis)
        
        # Try to build spec
        new_spec = self.build_spec()
        if new_spec:
            self.last_spec = self.spec
            self.spec = new_spec
        
        # Generate conversational response
        return self._generate_conversational_response(analysis)
    
    def _generate_conversational_response(self, analysis: Dict[str, Any]) -> str:
        """Generate a natural, conversational response."""
        # Acknowledge what we understood in a natural way
        understood_parts = []
        if analysis["system_name"]:
            understood_parts.append(f"system: {analysis['system_name']}")
        if analysis["components"]:
            understood_parts.append(f"components: {', '.join(analysis['components'])}")
        if analysis["states"]:
            understood_parts.append(f"states: {', '.join(analysis['states'].keys())}")
        if analysis["faults"]:
            understood_parts.append(f"faults: {', '.join(analysis['faults'])}")
        
        if understood_parts:
            response = f"Got it - {', '.join(understood_parts)}\n"
        else:
            response = ""
        
        # Generate natural follow-up based on what we have
        if not self.extracted_info["system_name"] and not self.extracted_info["components"]:
            response += "What kind of system would you like me to help you model?"
        elif not self.extracted_info["components"]:
            response += "What are the main components in your system?"
        elif self.extracted_info["components"]:
            # Check if we have enough detail for each component
            needs_more = False
            for comp_name, comp_info in self.extracted_info["components"].items():
                if not comp_info["states"] and not comp_info["faults"]:
                    response += f"Great, so we're modeling a {comp_name.lower()}! What might go wrong with it? How does it work? What are its key operating parameters?"
                    needs_more = True
                    break
            
            if not needs_more:
                if self.is_ready():
                    response += "This is looking good! I can generate a model now, or if you want to tell me more details to make it even better, I'm all ears!"
                else:
                    response += "That's a good start! What else can you tell me? Maybe more failure modes, operating conditions, or performance characteristics?"
        
        return response
    
    def _answer_user_question(self, question_text: str) -> str:
        """Answer user questions conversationally."""
        question_lower = question_text.lower()
        
        # Confusion/help responses
        if any(phrase in question_lower for phrase in ["dont know", "don't know", "not sure", "confused", "help"]):
            return "No worries! I'm here to help. What kind of system or thing would you like to create a model of? It could be anything - a car engine, a water pump, a robot, a building's air conditioning, whatever you're interested in!"
        
        # What should I do / Do you think responses  
        elif any(phrase in question_lower for phrase in ["what should", "what can", "what do", "how do", "should i", "do you think", "need more", "give you more", "tell you more", "you have enough", "by just me saying", "that's enough", "thats enough"]):
            if any(phrase in question_lower for phrase in ["more", "enough", "give you", "tell you", "by just me saying", "by saying"]):
                # They're asking if they should provide more details or if what they said is enough
                components = self.extracted_info.get("components", [])
                system_name = self.extracted_info.get("system_name", "")
                
                if "by just me saying" in question_lower or "by saying" in question_lower:
                    # They're asking if just saying "car" or whatever is enough
                    if not components or (len(components) == 0 and system_name in ["a", "car", "the"]):
                        return "No way! Just saying 'car' isn't nearly enough. I need to know what PART of the car - the engine? transmission? brakes? And then how it works, what might go wrong with it, etc. Think of me like an engineer who needs details to build something useful!"
                    elif components:
                        return f"Well, you mentioned {', '.join(components)}, which is a start! But I'll need more details to build a really useful model. What might go wrong with it? How does it work? What are its key parameters?"
                
                if components:
                    current_info = f" We have {', '.join(components)} so far."
                return f"I need MORE details to build a good model!{current_info} Tell me things like: What might break or go wrong? How does it work? What are its operating conditions? The more you tell me, the better the model will be!"
            else:
                return "You can tell me about any system you'd like to model! For example, you could say 'I want to model a car engine' or 'help me with a wind turbine' or 'I'm working on a water pump system'. Just describe it naturally and I'll help you build a model for it."
        
        # Asking for help with specific things
        elif any(phrase in question_lower for phrase in ["can you fill", "can we add", "what might go wrong", "fill it", "add that", "help with"]):
            components = self.extracted_info.get("components", [])
            if "engine" in str(components).lower():
                return "Absolutely! For a 2008 Audi A4 engine, common problems include: overheating, timing chain issues, carbon buildup, oil leaks, turbo failure (if turbocharged), ignition coil problems, fuel pump issues, and sensor failures. Want me to add some of these to your model?"
            elif components:
                comp_name = components[0].lower()
                return f"Sure! For a {comp_name}, common issues might include mechanical wear, overheating, electrical failures, leaks, blockages, or performance degradation. What specific problems are you thinking about?"
            else:
                return "I'd love to help! What component are we working with? Engine? Transmission? Brakes? Tell me what system you want to model and I can suggest realistic failure modes and operating parameters."
        
        # Knowledge questions  
        elif any(phrase in question_lower for phrase in ["you know", "know how", "how does", "how it works"]):
            components = self.extracted_info.get("components", [])
            if "engine" in str(components).lower():
                return "Yes! Car engines work by burning fuel to create power. Key things that can fail: overheating (cooling system), timing issues (timing chain/belt), fuel delivery problems, ignition system failures, oil system issues, and sensor/computer problems. What specific aspects interest you?"
            else:
                return "I know about lots of systems! What specifically are you curious about? I can explain how it works and what typically goes wrong with it."
        
        # General explanations
        elif any(word in question_lower for word in ["explain", "mean", "what is"]):
            return "I help you create technical models of systems using fmdtools. Just describe any system you're interested in - like engines, pumps, robots, HVAC systems, manufacturing equipment, whatever - and I'll help you build a detailed model that can simulate how it works and what might go wrong with it."
        
        # Default helpful response
        else:
            current_context = ""
            components = self.extracted_info.get("components", [])
            if components and "engine" in str(components).lower():
                current_context = " For your engine, I could suggest common failure modes like overheating, timing issues, fuel problems, etc."
            elif components:
                current_context = f" I see you're interested in {', '.join(components)}. I can help suggest what might go wrong with it."
            return f"I'd be happy to help!{current_context} What would you like to know more about, or shall we continue working on your model?"
    
    def generate_smart_questions(self) -> List[str]:
        """Generate comprehensive, expert-level questions to build the best model possible."""
        if not self.spec:
            if not self.extracted_info["system_name"]:
                return ["What system would you like to model? Be specific about the type and application."]
            elif not self.extracted_info["components"]:
                return ["What are the main components and subsystems in your system?"]
        
        questions = []
        
        # Get comprehensive questions for each component type
        for comp_name, comp_info in self.extracted_info["components"].items():
            comp_questions = self._get_expert_questions_for_component(comp_name, comp_info)
            questions.extend(comp_questions)
            if len(questions) >= 3:  # Limit to 3 for now, but make them really good
                break
        
        # If no component-specific questions, ask system-level questions
        if not questions:
            questions = self._get_system_level_questions()
        
        return questions[:3]
    
    def _get_expert_questions_for_component(self, comp_name: str, comp_info: Dict) -> List[str]:
        """Generate expert-level questions specific to component type."""
        questions = []
        comp_lower = comp_name.lower()
        
        # Engine/Motor expert questions
        if "engine" in comp_lower or "motor" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of engine is this? What are its key operating parameters (displacement, max RPM, power rating, operating temperature range, fuel consumption rate)?")
            if not comp_info["faults"]:
                questions.append("What are the critical failure modes for this engine? Consider mechanical failures (bearing wear, piston ring damage), thermal issues (overheating, coolant loss), and fuel system problems.")
            if len(questions) < 3:
                questions.append("What are the engine's performance characteristics? What's the efficiency curve, torque curve, and how does performance degrade under different operating conditions?")
                
        # Pump/Hydraulic expert questions  
        elif "pump" in comp_lower or "hydraulic" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of pump is this? What's the flow rate range, operating pressure, suction/discharge characteristics, and power requirements?")
            if not comp_info["faults"]:
                questions.append("What pump failure modes should we model? Consider cavitation, seal leaks, impeller damage, motor failure, and blockages.")
            if len(questions) < 3:
                questions.append("What are the pump's performance curves? How do efficiency, flow rate, and pressure relate? What about temperature effects and wear over time?")
                
        # Wind turbine/Windmill expert questions
        elif "wind" in comp_lower or "turbine" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of wind system? What's the rotor diameter, rated power, cut-in/cut-out wind speeds, rotational speed range, and pitch control system?")
            if not comp_info["faults"]:
                questions.append("What wind turbine failures should we model? Consider blade damage/imbalance, gearbox failure, generator issues, pitch system faults, and yaw system problems.")
            if len(questions) < 3:
                questions.append("What are the operating conditions and performance characteristics? Wind speed vs power curves, efficiency at different conditions, temperature effects, and maintenance schedules?")
                
        # AC/HVAC expert questions
        elif "ac" in comp_lower or "air" in comp_lower or "hvac" in comp_lower or "climate" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of AC system? What's the cooling capacity (BTU/hr), refrigerant type, operating pressures, temperature control range, and power consumption?")
            if not comp_info["faults"]:
                questions.append("What AC system failures should we model? Consider refrigerant leaks, compressor failure, condenser/evaporator fouling, fan motor failure, and control system issues.")
            if len(questions) < 3:
                questions.append("What are the AC system's performance characteristics? COP (coefficient of performance) curves, seasonal efficiency, humidity control, and how performance varies with ambient conditions?")
                
        # Battery/Electrical expert questions
        elif "battery" in comp_lower or "electrical" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of battery system? What's the chemistry (Li-ion, lead-acid, etc.), capacity (Ah), voltage range, charge/discharge rates, and thermal management?")
            if not comp_info["faults"]:
                questions.append("What battery failure modes should we model? Consider capacity fade, internal resistance increase, thermal runaway, cell imbalance, and charging system failures.")
            if len(questions) < 3:
                questions.append("What are the battery's performance characteristics? Discharge curves at different rates, temperature effects, cycle life, and state-of-health indicators?")
                
        # Valve expert questions
        elif "valve" in comp_lower or "control" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of valve? What's the size, pressure rating, flow coefficient (Cv), actuator type (pneumatic/electric), and control signal range?")
            if not comp_info["faults"]:
                questions.append("What valve failures should we model? Consider sticking (open/closed), seat leakage, actuator failure, positioner drift, and control signal loss.")
            if len(questions) < 3:
                questions.append("What are the valve's performance characteristics? Flow curves vs position, pressure drop relationships, response time, and hysteresis effects?")
                
        # Sensor expert questions
        elif "sensor" in comp_lower:
            if not comp_info["states"]:
                questions.append("What type of sensor and what does it measure? What's the measurement range, accuracy, resolution, response time, and operating environment?")
            if not comp_info["faults"]:
                questions.append("What sensor failures should we model? Consider drift, bias, noise increase, complete failure, and environmental effects (temperature, vibration, EMI).")
            if len(questions) < 3:
                questions.append("What are the sensor's performance characteristics? Accuracy vs range, temperature coefficients, aging effects, and calibration requirements?")
                
        # Generic component expert questions
        else:
            if not comp_info["states"]:
                questions.append(f"What are the critical operating parameters for the {comp_name}? Consider performance metrics, environmental factors, and control inputs/outputs.")
            if not comp_info["faults"]:
                questions.append(f"What are the primary failure modes for the {comp_name}? Think about wear mechanisms, environmental stresses, and operational limits.")
            if len(questions) < 3:
                questions.append(f"How does the {comp_name} interact with other components? What are the input/output flows, control signals, and performance dependencies?")
        
        return questions
    
    def _get_system_level_questions(self) -> List[str]:
        """Generate system-level questions when component questions are complete."""
        questions = [
            "What are the key system-level performance requirements and operating constraints?",
            "What external conditions affect system performance (temperature, pressure, load variations)?",
            "What are the system's safety-critical functions and what happens when they fail?"
        ]
        return questions
    
    def get_missing_info(self) -> str:
        """Get description of missing information."""
        missing = []
        
        if not self.extracted_info["system_name"]:
            missing.append("system name")
        
        if not self.extracted_info["components"]:
            missing.append("components")
        else:
            components_needing_states = []
            components_needing_faults = []
            
            for comp_name, comp_info in self.extracted_info["components"].items():
                if not comp_info["states"]:
                    components_needing_states.append(comp_name)
                if not comp_info["faults"]:
                    components_needing_faults.append(comp_name)
            
            if components_needing_states:
                missing.append(f"states for {', '.join(components_needing_states)}")
            if components_needing_faults:
                missing.append(f"fault modes for {', '.join(components_needing_faults)}")
        
        return ", ".join(missing) if missing else "nothing - you're all set!"
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return intelligent response."""
        self.conversation_history.append(user_input)
        
        # Analyze the input
        analysis = self.analyze_input(user_input)
        
        # Handle generation request
        if analysis["intent"] == "generate":
            if self.is_ready():
                return "READY_TO_GENERATE"
            else:
                missing = self.get_missing_info()
                return f"Cannot generate yet. Missing: {missing}\n\nPlease provide the missing information."
        
        # Generate intelligent response
        return self.generate_intelligent_response(analysis)
    
    def is_ready(self) -> bool:
        """Check if we have comprehensive information to generate a high-quality model."""
        if not self.spec or not self.spec.functions:
            return False
        
        # Check if we have comprehensive information for each component
        for comp_name, comp_info in self.extracted_info["components"].items():
            # Must have detailed states (more than just basic ones)
            if len(comp_info["states"]) < 3:
                return False
            
            # Must have identified failure modes
            if not comp_info["faults"]:
                return False
                
            # Component-specific readiness checks
            comp_lower = comp_name.lower()
            
            if "engine" in comp_lower or "motor" in comp_lower:
                required_states = ["rpm", "temperature", "power_output", "efficiency"]
                if not any(state in str(comp_info["states"]).lower() for state in ["rpm", "speed"]):
                    return False
                if not any(state in str(comp_info["states"]).lower() for state in ["temperature", "temp"]):
                    return False
                    
            elif "pump" in comp_lower or "hydraulic" in comp_lower:
                if not any(state in str(comp_info["states"]).lower() for state in ["pressure"]):
                    return False
                if not any(state in str(comp_info["states"]).lower() for state in ["flow", "rate"]):
                    return False
                    
            elif "wind" in comp_lower or "turbine" in comp_lower:
                if not any(state in str(comp_info["states"]).lower() for state in ["speed", "rpm", "power"]):
                    return False
                    
            elif "battery" in comp_lower:
                if not any(state in str(comp_info["states"]).lower() for state in ["voltage", "charge"]):
                    return False
        
        return True
    
    def get_status(self) -> str:
        """Get current status - conversational version."""
        if not self.spec:
            return "Gathering system information"
        
        func_count = len(self.spec.functions)
        
        if func_count == 0:
            return "Need components"
        
        if self.is_ready():
            return f"READY - {func_count} components defined"
        
        return f"{func_count} components"
    
    def get_diff(self) -> str:
        """Get changes from last state."""
        if not self.last_spec and self.spec:
            changes = []
            if self.spec.name:
                changes.append(f"+name: {self.spec.name}")
            for func in self.spec.functions:
                changes.append(f"+component: {func.name}")
                if func.states:
                    changes.append(f"+states: {func.name}")
                if func.faults:
                    changes.append(f"+faults: {func.name}")
            return "Added: " + ", ".join(changes) if changes else ""
        
        return ""
    
    def generate_files(self, output_dir: str = ".") -> str:
        """Generate model files."""
        if not self.is_ready():
            return f"Cannot generate - missing: {self.get_missing_info()}"
        
        try:
            files = render_level(self.spec, output_dir, force=True, dry_run=False)
            
            model_name = self.spec.name.lower()
            tree = f"{model_name}/\n"
            for file_path in files:
                tree += f"├── {file_path.name}\n"
            
            return f"Generated files:\n{tree}\nLocation: {files[0].parent.absolute()}"
            
        except Exception as e:
            return f"Generation failed: {e}"


def main(xml_file: Optional[str] = None):
    """Main conversational CLI."""
    print("🚀 fmdtools Intelligent Model Builder")
    print("Describe your system naturally and I'll build an fmdtools model for you.")
    print("Type 'help' for examples, 'generate' when ready, or 'quit' to exit.\n")
    
    xml_path = Path(xml_file) if xml_file else None
    builder = IntelligentBuilder(xml_path)
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            elif user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'help':
                print("\n💡 Examples of what you can say:")
                print("  • 'I want to model the G37 AC system with a V6 engine'")
                print("  • 'Build a pump system with temperature and pressure'")
                print("  • 'The engine can overheat and has rpm and temperature states'")
                print("  • 'temperature: 90, pressure: 100' (to add specific values)")
                print("\nI'll understand your description and ask smart follow-up questions.")
                print("Type 'generate' when I say READY.\n")
                    
            elif user_input.lower() == 'generate':
                if builder.is_ready():
                    print("\n🎯 Generating your model...")
                    result = builder.generate_files()
                    print(result)
                    print("\n✅ Model generated successfully!")
                    break
                else:
                    missing = builder.get_missing_info()
                    print(f"❌ Not ready to generate yet.\nMissing: {missing}")
                    
            else:
                response = builder.process_input(user_input)
                
                if response == "READY_TO_GENERATE":
                    print("\n🎯 Generating your model...")
                    result = builder.generate_files()
                    print(result)
                    print("\n✅ Model generated successfully!")
                    break
                else:
                    print(response)
            
        except EOFError:
            print("\nGoodbye! 👋")
            break
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try rephrasing your description.")


if __name__ == "__main__":
    import sys
    xml_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(xml_file)