"""
Test utility functions for formatting VHDL entity reports using pyVHDLModel.

This module provides functions for generating formatted reports of VHDL entities
for use in tests using pyVHDLModel objects.
"""

import sys
import os

# Add PyHDLio package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'PyHDLio'))

# pyVHDLModel imports
from pyVHDLModel.DesignUnit import Entity as PyVHDLModelEntity
from pyVHDLModel.Interface import GenericConstantInterfaceItem, PortSignalInterfaceItem, PortGroup as PyVHDLModelPortGroup


def report_generics(entity: PyVHDLModelEntity, indent: int = 2) -> str:
    """Generate formatted report of pyVHDLModel entity generics.
    
    Args:
        entity: pyVHDLModel Entity to report
        indent: Number of spaces for indentation
        
    Returns:
        Formatted string report of generics
    """
    istr = " " * indent
    output = [f"{istr}Generics:"]
    if entity.GenericItems:
        for generic in entity.GenericItems:
            name = generic.Identifiers[0] if generic.Identifiers else "unknown"
            # Try to get our stored type string, fallback to str(Subtype)
            if generic.Subtype is not None and hasattr(generic.Subtype, '_typeString'):
                type_str = generic.Subtype._typeString
            else:
                type_str = str(generic.Subtype) if generic.Subtype else "unknown"
            default = f" = {generic.DefaultExpression}" if generic.DefaultExpression else ""
            output.append(f"{istr}    - {name}: {type_str}{default}")
    else:
        output.append(f"{istr}    None")
    return "\n".join(output)


def report_ports_flat(entity: PyVHDLModelEntity, indent: int = 2) -> str:
    """Generate formatted report of pyVHDLModel entity ports in flat format.
    
    Args:
        entity: pyVHDLModel Entity to report
        indent: Number of spaces for indentation
        
    Returns:
        Formatted string report of ports
    """
    istr = " " * indent
    output = [f"{istr}Ports (flat):"]
    if entity.PortItems:
        for port in entity.PortItems:
            name = port.Identifiers[0] if port.Identifiers else "unknown"
            direction = port.Mode.name.lower() if port.Mode else "unknown"
            # Try to get our stored type string, fallback to str(Subtype)
            if port.Subtype is not None and hasattr(port.Subtype, '_typeString'):
                type_str = port.Subtype._typeString
            else:
                type_str = str(port.Subtype) if port.Subtype else "unknown"
            output.append(f"{istr}    - {name}: {direction} {type_str}")
    else:
        output.append(f"{istr}    None")
    return "\n".join(output)


def report_ports_grouped(entity: PyVHDLModelEntity, indent: int = 2) -> str:
    """Generate formatted report of pyVHDLModel entity ports in grouped format.
    
    Args:
        entity: pyVHDLModel Entity to report
        indent: Number of spaces for indentation
        
    Returns:
        Formatted string report of grouped ports
    """
    istr = " " * indent
    output = [f"{istr}Ports (grouped):"]
    if hasattr(entity, 'PortGroups') and entity.PortGroups:
        for i, group in enumerate(entity.PortGroups, 1):
            output.append(f"{istr}  Group {i}:")
            for port in group.PortItems:
                name = port.Identifiers[0] if port.Identifiers else "unknown"
                direction = port.Mode.name.lower() if port.Mode else "unknown"
                # Try to get our stored type string, fallback to str(Subtype)
                if port.Subtype is not None and hasattr(port.Subtype, '_typeString'):
                    type_str = port.Subtype._typeString
                else:
                    type_str = str(port.Subtype) if port.Subtype else "unknown"
                output.append(f"{istr}    - {name}: {direction} {type_str}")
    else:
        output.append(f"{istr}    None")
    return "\n".join(output)


def report_entity(entity: PyVHDLModelEntity, indent: int = 0) -> str:
    """Generate complete formatted report of a pyVHDLModel entity.
    
    Args:
        entity: pyVHDLModel Entity to report
        indent: Number of spaces for indentation
        
    Returns:
        Formatted string report of the entity
    """
    istr = " " * indent
    entity_name = entity.Identifier

    output = [f"{istr}Entity: {entity_name}"]
    output.append(report_generics(entity, indent + 2))
    output.append(report_ports_flat(entity, indent + 2))
    output.append(report_ports_grouped(entity, indent + 2))
    return "\n".join(output)


def report_pyvhdlmodel_entities(entities: list) -> str:
    """Generate formatted report of pyVHDLModel entities.

    Args:
        entities: List of pyVHDLModel Entity objects

    Returns:
        Formatted string report
    """
    if not entities:
        return "No entities found."
    output = []
    for entity in entities:
        output.append(report_entity(entity))
    return "\n".join(output) 