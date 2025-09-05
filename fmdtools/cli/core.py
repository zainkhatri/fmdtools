#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Core fmdtools CLI functionality - consolidated module.
"""

import os
import sys
import re
import platform
from pathlib import Path
from typing import List, Dict, Any, Union
from dataclasses import dataclass

import typer
from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field


# SCHEMAS
class Fault(BaseModel):
    """Fault mode."""
    name: str


class FunctionSpec(BaseModel):
    """Function specification."""
    name: str
    description: str = ""
    states: Dict[str, Any] = Field(default_factory=dict)
    modes: List[str] = Field(default_factory=lambda: ["nominal"])
    faults: List[Fault] = Field(default_factory=list)


class FlowSpec(BaseModel):
    """Flow specification."""
    name: str
    description: str = ""
    vars: Dict[str, Any] = Field(default_factory=dict)


class ConnectionSpec(BaseModel):
    """Connection specification."""
    from_fn: str
    to_fn: str
    flow_name: str


class ArchitectureSpec(BaseModel):
    """Architecture specification."""
    name: str
    functions: List[str]
    connections: List[ConnectionSpec] = Field(default_factory=list)


class SimulationSpec(BaseModel):
    """Simulation specification."""
    sample_run: bool = True
    fault_analysis: bool = False
    parameter_study: bool = False


class LevelSpec(BaseModel):
    """Complete model specification."""
    name: str
    description: str = ""
    functions: List[FunctionSpec]
    flows: List[FlowSpec] = Field(default_factory=list)
    architecture: ArchitectureSpec
    simulation: SimulationSpec = Field(default_factory=SimulationSpec)
    is_quick_mode: bool = False

    def model_post_init(self, __context):
        """Basic validation."""
        if not self.functions:
            raise ValueError("Model must have at least one function")
        return self


# UTILITIES
@dataclass
class NameMapping:
    """Mapping between original and sanitized names."""
    safe_name: str
    class_name: str


@dataclass
class SanitizedNames:
    """Result of name sanitization."""
    spec_name: str
    function_mapping: Dict[str, NameMapping]
    flow_mapping: Dict[str, NameMapping]


def slugify_module(s: str) -> str:
    """Convert string to valid Python module name."""
    s = re.sub(r"[^0-9a-zA-Z_]+", "_", s).strip("_")
    if re.match(r"^[0-9]", s):
        s = "_" + s
    return s.lower()


def to_class_name(s: str) -> str:
    """Convert string to valid Python class name."""
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s).title().replace(" ", "")
    if re.match(r"^[0-9]", s):
        s = "_" + s
    return s


def sanitize_class_name(name: str) -> str:
    """Clean and sanitize a string to create a valid Python class name."""
    clean_name = re.sub(r'[^0-9a-zA-Z\\s]', '', name)
    class_name = clean_name.title().replace(' ', '')
    if class_name and class_name[0].isdigit():
        class_name = '_' + class_name
    return class_name or 'DefaultClass'


def sanitize_identifier(name: str) -> str:
    """Clean and sanitize a string to create a valid Python identifier."""
    clean_name = re.sub(r'[^0-9a-zA-Z_]', '_', str(name))
    clean_name = re.sub(r'_+', '_', clean_name)
    clean_name = clean_name.strip('_')
    if clean_name and clean_name[0].isdigit():
        clean_name = '_' + clean_name
    return clean_name or 'default_var'


def escape_string_for_python(text: str) -> str:
    """Escape a string to be safe for Python code generation."""
    if not text:
        return ""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace("'", "\\'")
    text = text.replace('\n', '\\n')
    text = text.replace('\t', '\\t')
    return text


def sanitize_names(spec_name: str, function_names: list, flow_names: list) -> SanitizedNames:
    """Sanitize all names and return structured mappings."""
    safe_spec_name = slugify_module(spec_name)
    
    function_mapping = {}
    for name in function_names:
        safe_name = slugify_module(name)
        class_name = to_class_name(name)
        function_mapping[name] = NameMapping(safe_name, class_name)
    
    flow_mapping = {}
    for name in flow_names:
        safe_name = slugify_module(name)
        class_name = to_class_name(name)
        flow_mapping[name] = NameMapping(safe_name, class_name)
    
    return SanitizedNames(safe_spec_name, function_mapping, flow_mapping)


# INPUT PROCESSING
def clean_name(name: str) -> str:
    """Clean and sanitize a name to be consistent and professional."""
    if not name.strip():
        return name
    
    cleaned = ' '.join(name.strip().split())
    cleaned = ''.join(word.capitalize() for word in cleaned.split())
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', cleaned)
    
    if cleaned and cleaned[0].isdigit():
        cleaned = 'Model' + cleaned
    
    return cleaned or 'Component'


def detect_multiple_items(text: str) -> List[str]:
    """Detect if user provided multiple items separated by commas, 'and', etc."""
    if not text.strip():
        return []
    
    separators = [',', ' and ', ' & ', ';', '/', '|']
    items = [text.strip()]
    
    for sep in separators:
        new_items = []
        for item in items:
            new_items.extend(part.strip() for part in item.split(sep) if part.strip())
        items = new_items
    
    return [clean_name(item) for item in items if item]


def smart_input_prompt(prompt: str, context: str = '', allow_multiple: bool = False) -> Union[str, List[str]]:
    """Smart input prompt that provides examples and handles common input issues."""
    examples_map = {
        'component': 'engine, transmission, battery, pump, controller, sensor',
        'fault': 'overheat, mechanical_failure, stuck, leak, power_failure, degraded',
        'property': 'temperature, pressure, speed, voltage, power, flow_rate',
        'input': 'electricity, fuel, water, air, signals, materials',
        'output': 'power, heat, movement, pressure, data, processed_materials'
    }
    
    examples = examples_map.get(context, '')
    
    if examples:
        full_prompt = f"{prompt}\n  Examples: {examples}\n> "
    else:
        full_prompt = f"{prompt}\n> "
    
    try:
        user_input = input(full_prompt).strip()
    except EOFError:
        raise EOFError("Input terminated unexpectedly")
    except KeyboardInterrupt:
        raise KeyboardInterrupt("User cancelled operation")
    
    if not user_input:
        return "" if not allow_multiple else []
    
    if allow_multiple:
        items = detect_multiple_items(user_input)
        if len(items) > 1:
            print(f"\nDetected {len(items)} components: {', '.join(items)}")
            response = input("Did you mean these as separate components? (Y/n): ").strip().lower()
            if not response.startswith('n'):
                return [clean_name(item) for item in items]
    
    return clean_name(user_input)


# CODE GENERATION
def render_level(spec: LevelSpec, out_dir: str = ".", force: bool = False, dry_run: bool = False) -> List[Path]:
    """Render a complete level model from specification."""
    names = sanitize_names(
        spec.name, 
        [f.name for f in spec.functions], 
        [f.name for f in spec.flows]
    )
    
    out_path = Path(out_dir) / names.spec_name
    
    if not dry_run:
        out_path.mkdir(parents=True, exist_ok=True)
    
    if not dry_run:
        try:
            import fmdtools
            typer.echo(f"fmdtools {getattr(fmdtools, '__version__', 'unknown')} • Python {platform.python_version()}")
        except Exception:
            typer.echo(f"fmdtools (unknown version) • Python {platform.python_version()}")
        typer.echo(f"Output: {Path(out_dir).resolve() / names.spec_name}")
    
    files = []
    
    # Check for existing files if not forcing
    if not force and not dry_run:
        existing_files = []
        for func in spec.functions:
            safe_name = names.function_mapping[func.name].safe_name
            if (out_path / f"{safe_name}.py").exists():
                existing_files.append(f"{safe_name}.py")
        for check_file in ["flows.py", "architecture.py", f"level_{names.spec_name}.py"]:
            if (out_path / check_file).exists():
                existing_files.append(check_file)
        
        if existing_files:
            raise FileExistsError(
                f"Files already exist in {out_path}: {', '.join(existing_files)}. "
                f"Use --force to overwrite or --dry-run to preview."
            )
    
    # Set up Jinja2 environment
    env = Environment(
        loader=PackageLoader("fmdtools.cli", "templates"),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )
    env.filters["pyrepr"] = repr
    env.filters["sanitize_identifier"] = sanitize_identifier
    env.filters["escape_string"] = escape_string_for_python
    
    # Generate function files
    for func in spec.functions:
        mapping = names.function_mapping[func.name]
        target = out_path / f"{mapping.safe_name}.py"
        template = env.get_template("function.py.j2")
        content = template.render(func=func, spec=spec, class_name=mapping.class_name)
        if dry_run:
            print(f"\n--- {target} ---")
            print(content)
        else:
            target.write_text(content)
        files.append(target)
    
    # Generate flows file
    if spec.flows:
        target = out_path / "flows.py"
        template = env.get_template("flows.py.j2")
        content = template.render(spec=spec, flows=spec.flows, flow_mapping=names.flow_mapping)
        if dry_run:
            print(f"\n--- {target} ---")
            print(content)
        else:
            target.write_text(content)
        files.append(target)
    
    # Generate architecture file
    target = out_path / "architecture.py"
    template = env.get_template("architecture.py.j2")
    arch_class_name = sanitize_class_name(spec.architecture.name)
    content = template.render(spec=spec, arch=spec.architecture, functions=spec.functions, 
                             function_mapping=names.function_mapping, flow_mapping=names.flow_mapping,
                             arch_class_name=arch_class_name)
    if dry_run:
        print(f"\n--- {target} ---")
        print(content)
    else:
        target.write_text(content)
    files.append(target)
    
    # Generate main level file
    target = out_path / f"level_{names.spec_name}.py"
    template = env.get_template("level.py.j2")
    class_name = sanitize_class_name(spec.name)
    arch_class_name = sanitize_class_name(spec.architecture.name)
    content = template.render(spec=spec, safe_spec_name=names.spec_name, class_name=class_name, arch_class_name=arch_class_name)
    if dry_run:
        print(f"\n--- {target} ---")
        print(content)
    else:
        target.write_text(content)
    files.append(target)
    
    # Generate __init__.py
    target = out_path / "__init__.py"
    template = env.get_template("init.py.j2")
    class_name = sanitize_class_name(spec.name)
    arch_class_name = sanitize_class_name(spec.architecture.name)
    content = template.render(spec=spec, safe_spec_name=names.spec_name, 
                              class_name=class_name, arch_class_name=arch_class_name)
    if dry_run:
        print(f"\n--- {target} ---")
        print(content)
    else:
        target.write_text(content)
    files.append(target)
    
    return files