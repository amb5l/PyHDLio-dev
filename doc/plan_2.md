# PyHDLio pyVHDLModel Integration Plan

## Overview

This plan outlines the integration of **pyVHDLModel** into **PyHDLio** to provide a rich object hierarchy for VHDL analysis while maintaining PyHDLio's lightweight design. The integration will use PyHDLio's ANTLR4 parser as the frontend and convert the AST to pyVHDLModel objects.

### Objectives

- **Fork and integrate pyVHDLModel** as a submodule for object hierarchy support
- **Extend PyHDLio** with pyVHDLModel conversion capabilities
- **Bundle minimal artifacts** to keep PyHDLio distribution slim
- **Preserve existing functionality** while adding new capabilities
- **Create comprehensive examples** demonstrating both approaches

### Key Benefits

- **Dual Access Modes**: PyHDLio AST (lightweight) + pyVHDLModel objects (rich)
- **Port Group Support**: Enhanced with source-proximity-based grouping
- **Clean Architecture**: Minimal coupling, optional functionality
- **Backwards Compatibility**: Existing PyHDLio functionality unchanged

---

## Prerequisites

### Environment Requirements
- **Python**: 3.8+ with virtual environment (`.venv`)
- **Java**: JDK 11+ for ANTLR4 code generation
- **Git**: For submodule management
- **Platform**: Windows (current setup)

### Current Status Verification
```bash
# Verify virtual environment
cd D:\work\PyHDLio-dev
.venv\Scripts\Activate.ps1

# Verify PyHDLio functionality (unified example)
.venv\Scripts\python.exe PyHDLio\examples\vhdl\simple\simple.py

# Run existing tests
pytest tests/unit/test_vhdl_parser.py -v
```

---

## Implementation Steps

### Step 1: Fork and Setup pyVHDLModel Submodule

#### 1.1 Fork pyVHDLModel Repository
```bash
# Navigate to: https://github.com/VHDL/pyVHDLModel
# Click "Fork" to create fork under your GitHub account
```

#### 1.2 Add Submodule to PyHDLio-dev
```bash
cd D:\work\PyHDLio-dev

# Add forked repository as submodule
git submodule add https://github.com/<your-username>/pyVHDLModel pyVHDLModel

# Initialize and update
git submodule update --init --recursive

# Commit submodule addition
git commit -m "Add pyVHDLModel submodule for object hierarchy support"
```

#### 1.3 Install pyVHDLModel for Development
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install in editable mode
cd pyVHDLModel
pip install -e .

# Verify installation
pip list | grep pyVHDLModel
```

#### **Success Criteria**
- [ ] pyVHDLModel submodule at `PyHDLio-dev/pyVHDLModel`
- [ ] Package installed in virtual environment
- [ ] Can import `from pyVHDLModel import *`

---

### Step 2: Extend pyVHDLModel for Port Groups

#### 2.1 Create PortGroup Class
**File**: `pyVHDLModel/pyVHDLModel/PortGroup.py`
```python
from typing import List
from dataclasses import dataclass
from .InterfaceItems import PortInterfaceItem

@dataclass
class PortGroup:
    """Represents a group of VHDL ports separated by blank lines or comments."""
    ports: List[PortInterfaceItem]

    def __post_init__(self):
        """Validate port group contents."""
        if not self.ports:
            raise ValueError("PortGroup cannot be empty")
```

#### 2.2 Extend Entity Class
**File**: `pyVHDLModel/pyVHDLModel/DesignUnit.py`
```python
# Add import at top
from .PortGroup import PortGroup

# Modify Entity class __init__ method
class Entity(PrimaryUnit):
    def __init__(self, ...):
        super().__init__(...)
        self.PortGroups: List[PortGroup] = []  # Add port groups support
```

#### 2.3 Update Exports
**File**: `pyVHDLModel/pyVHDLModel/__init__.py`
```python
# Add to existing exports
from .PortGroup import PortGroup
```

#### 2.4 Commit Changes
```bash
cd pyVHDLModel
git add .
git commit -m "Add PortGroup class and extend Entity for port grouping"
git push origin main
```

#### **Success Criteria**
- [ ] PortGroup class created and functional
- [ ] Entity.PortGroups attribute available
- [ ] Changes committed to fork

---

### Step 3: Bundle Minimal pyVHDLModel Artifacts

#### 3.1 Create Bundle Directory
```bash
mkdir PyHDLio\hdlio\vhdl\pyVHDLModel
```

#### 3.2 Copy Essential Modules
**Copy these files** from `pyVHDLModel/pyVHDLModel/` to `PyHDLio/hdlio/vhdl/pyVHDLModel/`:
- `Common.py` - Base types and enums
- `DesignUnit.py` - Entity and other design units
- `InterfaceItems.py` - Generic and Port classes
- `PortGroup.py` - New port group class
- `__init__.py` - Module exports

#### 3.3 Create Bundle Init File
**File**: `PyHDLio/hdlio/vhdl/pyVHDLModel/__init__.py`
```python
"""
Minimal pyVHDLModel artifacts for VHDL object hierarchy.
Bundled subset of pyVHDLModel to support entity analysis.
"""

from .Common import Mode
from .DesignUnit import Entity
from .InterfaceItems import GenericInterfaceItem, PortInterfaceItem
from .PortGroup import PortGroup

__all__ = [
    'Mode',
    'Entity',
    'GenericInterfaceItem',
    'PortInterfaceItem',
    'PortGroup'
]
```

#### 3.4 Update PyHDLio Package Configuration
**File**: `PyHDLio/pyproject.toml`
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["hdlio*"]  # Will include hdlio.vhdl.pyVHDLModel automatically
```

#### **Success Criteria**
- [ ] Essential modules copied to `hdlio/vhdl/pyVHDLModel/`
- [ ] Can import: `from hdlio.vhdl.pyVHDLModel import Entity`
- [ ] Bundle size < 50KB (minimal footprint)

---

### Step 4: Create PyHDLio ↔ pyVHDLModel Converter

#### 4.1 Implement Converter Module
**File**: `PyHDLio/hdlio/vhdl/pyVHDLModel_converter.py`
```python
"""Convert PyHDLio AST to pyVHDLModel object hierarchy."""

from typing import List
from .ast.ast import VHDLModule, Entity as PyHDLioEntity
from .pyVHDLModel import (
    Entity as VHDLModelEntity,
    GenericInterfaceItem,
    PortInterfaceItem,
    PortGroup,
    Mode
)

def convert_to_pyVHDLModel(module: VHDLModule) -> List[VHDLModelEntity]:
    """
    Convert PyHDLio VHDLModule to list of pyVHDLModel Entity objects.

    Args:
        module: PyHDLio VHDLModule containing parsed entities

    Returns:
        List of pyVHDLModel Entity objects with port groups
    """
    entities = []

    for pyhdlio_entity in module.entities:
        # Convert generics
        generics = [
            GenericInterfaceItem(
                identifiers=[generic.name],
                subtype=generic.type,
                defaultValue=generic.default_value
            )
            for generic in pyhdlio_entity.generics
        ]

        # Convert ports
        ports = []
        for port in pyhdlio_entity.ports:
            mode = _convert_port_direction(port.direction)
            subtype = _format_port_type(port.type, port.constraint)
            ports.append(PortInterfaceItem(
                identifiers=[port.name],
                mode=mode,
                subtype=subtype
            ))

        # Convert port groups
        port_groups = []
        for group in pyhdlio_entity.port_groups:
            group_ports = []
            for port in group.ports:
                mode = _convert_port_direction(port.direction)
                subtype = _format_port_type(port.type, port.constraint)
                group_ports.append(PortInterfaceItem(
                    identifiers=[port.name],
                    mode=mode,
                    subtype=subtype
                ))
            port_groups.append(PortGroup(ports=group_ports))

        # Create pyVHDLModel Entity
        entity = VHDLModelEntity(
            identifier=pyhdlio_entity.name,
            genericItems=generics,
            portItems=ports
        )
        entity.PortGroups = port_groups

        entities.append(entity)

    return entities

def _convert_port_direction(direction: str) -> Mode:
    """Convert PyHDLio port direction to pyVHDLModel Mode."""
    direction_map = {
        'in': Mode.In,
        'out': Mode.Out,
        'inout': Mode.InOut
    }
    return direction_map.get(direction.lower(), Mode.In)

def _format_port_type(type_name: str, constraint: str = None) -> str:
    """Format port type with optional constraint."""
    if constraint:
        return f"{type_name}({constraint})"
    return type_name
```

#### 4.2 Extend Parser Interface
**File**: `PyHDLio/hdlio/vhdl/parse_vhdl.py` (modify existing)
```python
# Add import
from .pyVHDLModel_converter import convert_to_pyVHDLModel

def parse_vhdl(file_path: str, mode: str = 'tree'):
    """
    Parse VHDL file and return results in specified format.

    Args:
        file_path: Path to VHDL file
        mode: Output format - 'tree', 'ast', or 'pyVHDLModel'

    Returns:
        Parse tree string, PyHDLio AST, or pyVHDLModel entities
    """
    # ... existing parsing logic ...

    if mode == 'ast':
        visitor = VHDLVisitor()
        return visitor.visit(tree)
    elif mode == 'pyVHDLModel':
        visitor = VHDLVisitor()
        ast_module = visitor.visit(tree)
        return convert_to_pyVHDLModel(ast_module)

    return tree.toStringTree(recog=parser)
```

#### **Success Criteria**
- [ ] Converter handles generics, ports, and port groups
- [ ] Parser supports `mode='pyVHDLModel'`
- [ ] Returns proper pyVHDLModel Entity objects

---

### Step 5: Create pyVHDLModel Reporter

#### 5.1 Implement Reporter Module
**File**: `PyHDLio/hdlio/vhdl/pyVHDLModel_reporter.py`
```python
"""Reporting functions for pyVHDLModel entities."""

from typing import List
from .pyVHDLModel import Entity, PortGroup

def report_entity_name(entity: Entity) -> str:
    """Report entity name."""
    return f"Entity: {entity.identifier}"

def report_generics(entity: Entity, indent: int = 2) -> str:
    """Report entity generics."""
    spaces = " " * indent
    lines = [f"{spaces}Generics:"]

    if entity.genericItems:
        for generic in entity.genericItems:
            name = generic.identifiers[0] if generic.identifiers else "unnamed"
            type_info = generic.subtype or "unknown"
            default = f" = {generic.defaultValue}" if generic.defaultValue else ""
            lines.append(f"{spaces}  - {name}: {type_info}{default}")
    else:
        lines.append(f"{spaces}  None")

    return "\n".join(lines)

def report_ports_flat(entity: Entity, indent: int = 2) -> str:
    """Report entity ports in flat format."""
    spaces = " " * indent
    lines = [f"{spaces}Ports (flat):"]

    if entity.portItems:
        for port in entity.portItems:
            name = port.identifiers[0] if port.identifiers else "unnamed"
            direction = port.mode.name.lower() if port.mode else "unknown"
            type_info = port.subtype or "unknown"
            lines.append(f"{spaces}  - {name}: {direction} {type_info}")
    else:
        lines.append(f"{spaces}  None")

    return "\n".join(lines)

def report_ports_grouped(entity: Entity, indent: int = 2) -> str:
    """Report entity ports grouped by source proximity."""
    spaces = " " * indent
    lines = [f"{spaces}Ports (grouped):"]

    if hasattr(entity, 'PortGroups') and entity.PortGroups:
        for i, group in enumerate(entity.PortGroups, 1):
            lines.append(f"{spaces}  Group {i}:")
            for port in group.ports:
                name = port.identifiers[0] if port.identifiers else "unnamed"
                direction = port.mode.name.lower() if port.mode else "unknown"
                type_info = port.subtype or "unknown"
                lines.append(f"{spaces}    - {name}: {direction} {type_info}")
    else:
        lines.append(f"{spaces}  No groups (using flat format)")
        return report_ports_flat(entity, indent)

    return "\n".join(lines)

def report_entity(entity: Entity, indent: int = 0) -> str:
    """Complete entity report with generics and both port formats."""
    lines = []
    base_spaces = " " * indent

    lines.append(f"{base_spaces}{report_entity_name(entity)}")
    lines.append(report_generics(entity, indent + 2))
    lines.append(report_ports_flat(entity, indent + 2))
    lines.append(report_ports_grouped(entity, indent + 2))

    return "\n".join(lines)

def report_entities(entities: List[Entity]) -> str:
    """Report all entities with complete information."""
    return "\n\n".join(report_entity(entity) for entity in entities)
```

#### **Success Criteria**
- [ ] Modular reporter functions for different output formats
- [ ] Consistent with PyHDLio reporter interface
- [ ] Handles missing data gracefully

---

### Step 6: Create Unified Example Demonstrating Both Approaches

#### 6.1 Unified Example Structure
**Directory**: `PyHDLio/examples/vhdl/simple/`

The example demonstrates both PyHDLio AST and pyVHDLModel approaches in a single script, allowing users to compare and understand the benefits of each approach.

**File**: `PyHDLio/examples/vhdl/simple/simple.vhd`
```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity counter is
    generic (
        WIDTH : integer := 8;
        DEPTH : natural := 16
    );
    port (
        clk : in STD_LOGIC;
        reset : in STD_LOGIC;

        start : in  STD_LOGIC_VECTOR(WIDTH-1 downto 0);
        count : out STD_LOGIC_VECTOR(WIDTH-1 downto 0)
    );
end counter;
```

**File**: `PyHDLio/examples/vhdl/simple/simple.py`
```python
#!/usr/bin/env python3
"""
PyHDLio Dual-Mode Example
Demonstrates VHDL parsing using both PyHDLio AST and pyVHDLModel approaches.
"""

import os
from hdlio.vhdl.parse_vhdl import parse_vhdl, VHDLSyntaxError
from hdlio.vhdl.reporter import report_entities as report_ast_entities

def demonstrate_ast_approach(vhdl_file):
    """Demonstrate PyHDLio AST approach - lightweight and fast."""
    print("=" * 60)
    print("PyHDLio AST Approach (Lightweight)")
    print("=" * 60)

    # Parse using PyHDLio AST
    module = parse_vhdl(vhdl_file, mode='ast')

    # Display formatted report
    print(report_ast_entities(module))

    # Demonstrate programmatic access
    print("\n--- Programmatic AST Access ---")
    for entity in module.entities:
        print(f"Entity: {entity.name}")
        print(f"  Generics: {len(entity.generics)}")
        print(f"  Ports: {len(entity.ports)}")
        print(f"  Port groups: {len(entity.port_groups)}")

def demonstrate_model_approach(vhdl_file):
    """Demonstrate pyVHDLModel approach - rich object hierarchy."""
    print("\n" + "=" * 60)
    print("pyVHDLModel Approach (Rich Object Hierarchy)")
    print("=" * 60)

    # When implemented:
    # entities = parse_vhdl(vhdl_file, mode='pyVHDLModel')
    # from hdlio.vhdl.pyVHDLModel_reporter import report_entities
    # print(report_entities(entities))

    print("Note: pyVHDLModel integration planned for future implementation")
    print("Expected benefits: Rich object model, standards compliance")

def compare_approaches():
    """Compare both approaches with recommendations."""
    print("\n" + "=" * 60)
    print("Approach Comparison & Recommendations")
    print("=" * 60)

    print("AST: Lightweight, fast, currently available")
    print("pyVHDLModel: Rich semantics, ecosystem compatibility (future)")
    print("Recommendation: Both approaches complement each other")

def main():
    """Main demonstration function."""
    vhdl_file = os.path.join(os.path.dirname(__file__), "simple.vhd")

    print("PyHDLio Dual-Mode VHDL Parsing Demonstration")
    print(f"Analyzing: {os.path.basename(vhdl_file)}")

    try:
        demonstrate_ast_approach(vhdl_file)
        demonstrate_model_approach(vhdl_file)
        compare_approaches()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

#### 6.2 Update Examples README
**File**: `PyHDLio/examples/README.md`
```markdown
# PyHDLio Examples

This directory demonstrates PyHDLio's capabilities for VHDL parsing and analysis.

## Simple Example (`simple/`)

The simple example demonstrates both PyHDLio AST and pyVHDLModel approaches:

- **File**: `simple/simple.py`
- **Features**:
  - PyHDLio AST parsing (lightweight, currently available)
  - pyVHDLModel integration preview (rich semantics, future)
  - Direct comparison of both approaches
  - Programmatic access examples

### Running the Example

```bash
# Setup
git clone --recurse-submodules <repo-url>
cd PyHDLio-dev
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install
pip install -e ./PyHDLio
pip install .[dev]

# Run unified example (demonstrates both AST and pyVHDLModel approaches)
.venv\Scripts\python.exe PyHDLio\examples\vhdl\simple\simple.py
```

### Expected Output

```
PyHDLio Dual-Mode VHDL Parsing Demonstration
Analyzing: simple.vhd

============================================================
PyHDLio AST Approach (Lightweight)
============================================================
Entity: counter
  Generics:
    - WIDTH: integer = 8
    - DEPTH: natural = 16
  Ports (flat):
    - clk: in STD_LOGIC
    - reset: in STD_LOGIC
    - start: in STD_LOGIC_VECTOR(WIDTH-1 downto 0)
    - count: out STD_LOGIC_VECTOR(WIDTH-1 downto 0)
  Ports (grouped):
    Group 1:
      - clk: in STD_LOGIC
      - reset: in STD_LOGIC
    Group 2:
      - start: in STD_LOGIC_VECTOR(WIDTH-1 downto 0)
      - count: out STD_LOGIC_VECTOR(WIDTH-1 downto 0)

--- Programmatic AST Access ---
Entity: counter
  Generics count: 2
  Ports count: 4
  Port groups count: 2
  Generic details:
    WIDTH: integer = 8
    DEPTH: natural = 16
  Port group structure:
    Group 1: clk, reset
    Group 2: start, count

============================================================
pyVHDLModel Approach (Rich Object Hierarchy)
============================================================
Note: pyVHDLModel integration planned for future implementation
Expected usage:
  entities = parse_vhdl(vhdl_file, mode='pyVHDLModel')
  from hdlio.vhdl.pyVHDLModel_reporter import report_entities
  print(report_entities(entities))

Expected benefits:
  - Rich object model with full VHDL semantics
  - Standards-compliant entity representation
  - Enhanced analysis capabilities
  - Compatibility with pyVHDLModel ecosystem

============================================================
Approach Comparison
============================================================

PyHDLio AST Approach:
  ✓ Lightweight and fast
  ✓ Minimal dependencies
  ✓ Currently implemented
  ✓ Source-proximity port grouping
  ✓ Perfect for quick analysis
  - Limited to PyHDLio's AST model

pyVHDLModel Approach (Future):
  ✓ Rich, standards-compliant object model
  ✓ Full VHDL semantic support
  ✓ Ecosystem compatibility
  ✓ Advanced analysis capabilities
  ✓ Pythonic object access
  - Higher overhead
  - Additional dependencies

Recommendation:
  - Use AST approach for quick parsing and simple analysis
  - Use pyVHDLModel approach for complex analysis and tool integration
  - Both approaches can coexist and complement each other
```

## Features Demonstrated

- **Entity Parsing**: Extract entity names, generics, and ports
- **Port Grouping**: Group ports based on source code proximity (blank lines)
- **Dual Access**: Both lightweight AST and rich object model approaches
- **Error Handling**: Graceful handling of file and syntax errors
- **Programmatic Access**: Direct manipulation of parsed structures
- **Comparison**: Clear guidance on when to use each approach

## Prerequisites

```bash
# Install PyHDLio in development mode
pip install -e ./PyHDLio

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
```
```

#### **Success Criteria**
- [ ] Single `simple/` directory with unified example
- [ ] Example demonstrates both AST and pyVHDLModel approaches
- [ ] Clear comparison and recommendations provided
- [ ] Documentation explains benefits of each approach
- [ ] Example works with current PyHDLio implementation

---

### Step 7: Add Comprehensive Tests

#### 7.1 Create pyVHDLModel Test Fixtures
**File**: `tests/fixtures/vhdl/entity_with_generics.vhd`
```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity test_generics is
    generic (
        WIDTH : integer := 8;
        DEPTH : natural := 16;
        NAME  : string := "test"
    );
    port (
        clk   : in  STD_LOGIC;
        reset : in  STD_LOGIC;

        data_in  : in  STD_LOGIC_VECTOR(WIDTH-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(WIDTH-1 downto 0)
    );
end test_generics;
```

#### 7.2 Extend Test Suite
**File**: `tests/unit/test_vhdl_parser.py` (add to existing)
```python
def test_pyVHDLModel_conversion_basic(self):
    """Test basic PyHDLio to pyVHDLModel conversion."""
    from hdlio.vhdl.pyVHDLModel import Entity as VHDLModelEntity

    result = parse_vhdl(self.simple_entity_path, mode='pyVHDLModel')

    assert isinstance(result, list)
    assert len(result) == 1

    entity = result[0]
    assert isinstance(entity, VHDLModelEntity)
    assert entity.identifier == "counter"

def test_pyVHDLModel_generics_conversion(self):
    """Test generics conversion to pyVHDLModel."""
    fixture_path = os.path.join(self.fixture_dir, 'entity_with_generics.vhd')
    result = parse_vhdl(fixture_path, mode='pyVHDLModel')

    entity = result[0]
    assert len(entity.genericItems) == 3

    # Check generic details
    width_generic = next(g for g in entity.genericItems if g.identifiers[0] == 'WIDTH')
    assert width_generic.subtype == 'integer'
    assert width_generic.defaultValue == '8'

def test_pyVHDLModel_port_groups(self):
    """Test port group conversion to pyVHDLModel."""
    fixture_path = os.path.join(self.fixture_dir, 'entity_with_generics.vhd')
    result = parse_vhdl(fixture_path, mode='pyVHDLModel')

    entity = result[0]
    assert hasattr(entity, 'PortGroups')
    assert len(entity.PortGroups) == 2  # Two groups separated by blank line

    # Check first group
    group1 = entity.PortGroups[0]
    assert len(group1.ports) == 2
    assert group1.ports[0].identifiers[0] == 'clk'
    assert group1.ports[1].identifiers[0] == 'reset'

def test_pyVHDLModel_reporter(self):
    """Test pyVHDLModel reporter functions."""
    from hdlio.vhdl.pyVHDLModel_reporter import report_entities

    fixture_path = os.path.join(self.fixture_dir, 'entity_with_generics.vhd')
    entities = parse_vhdl(fixture_path, mode='pyVHDLModel')

    report = report_entities(entities)

    # Verify report content
    assert "Entity: test_generics" in report
    assert "WIDTH: integer = 8" in report
    assert "clk: in STD_LOGIC" in report
    assert "Group 1:" in report
    assert "Group 2:" in report
```

#### **Success Criteria**
- [ ] All tests pass consistently
- [ ] Coverage includes conversion, reporting, and error handling
- [ ] Test fixtures cover various VHDL constructs

---

### Step 8: Update Package Exports

#### 8.1 Update Main Package Init
**File**: `PyHDLio/hdlio/vhdl/__init__.py`
```python
# Existing exports
from .ast.ast import VHDLModule, Entity, Generic, Port, PortGroup
from .visitor import VHDLVisitor
from .reporter import (
    report_entities, report_entity, report_generics,
    report_ports_flat, report_ports_grouped
)

# New pyVHDLModel exports
from .pyVHDLModel_converter import convert_to_pyVHDLModel
from .pyVHDLModel_reporter import (
    report_entities as report_pyVHDLModel_entities,
    report_entity as report_pyVHDLModel_entity
)

# Optional: Direct access to pyVHDLModel classes
try:
    from .pyVHDLModel import Entity as VHDLModelEntity, PortGroup as VHDLModelPortGroup
    _PYVHDLMODEL_AVAILABLE = True
except ImportError:
    _PYVHDLMODEL_AVAILABLE = False

__all__ = [
    # Core PyHDLio
    'VHDLModule', 'Entity', 'Generic', 'Port', 'PortGroup',
    'VHDLVisitor',
    'report_entities', 'report_entity', 'report_generics',
    'report_ports_flat', 'report_ports_grouped',

    # pyVHDLModel integration
    'convert_to_pyVHDLModel',
    'report_pyVHDLModel_entities', 'report_pyVHDLModel_entity',
]

if _PYVHDLMODEL_AVAILABLE:
    __all__.extend(['VHDLModelEntity', 'VHDLModelPortGroup'])
```

#### **Success Criteria**
- [ ] Clean import structure
- [ ] Backwards compatibility maintained
- [ ] Optional pyVHDLModel imports don't break core functionality

---

## Testing and Validation

### Comprehensive Test Plan

#### Phase 1: Unit Tests
```bash
# Run all VHDL parser tests
pytest tests/unit/test_vhdl_parser.py -v

# Test specific pyVHDLModel functionality
pytest tests/unit/test_vhdl_parser.py::test_pyVHDLModel_conversion_basic -v
```

#### Phase 2: Integration Tests
```bash
# Test unified example (demonstrates both approaches)
cd D:\work\PyHDLio-dev
.venv\Scripts\python.exe PyHDLio\examples\vhdl\simple\simple.py

# Verify AST functionality specifically
cd PyHDLio\examples\vhdl\simple
.venv\Scripts\python.exe -c "
from hdlio.vhdl.parse_vhdl import parse_vhdl
module = parse_vhdl('simple.vhd', mode='ast')
print(f'Found {len(module.entities)} entity(ies)')
print(f'Entity: {module.entities[0].name}')
"
```

#### Phase 3: Error Handling Tests
```bash
# Test with invalid files
cd PyHDLio\examples\vhdl\simple
.venv\Scripts\python.exe simple.py nonexistent.vhd

# Test with syntax errors
# (Create intentionally malformed VHDL file)
echo "entity bad" > bad.vhd
.venv\Scripts\python.exe -c "
from hdlio.vhdl.parse_vhdl import parse_vhdl, VHDLSyntaxError
try:
    parse_vhdl('bad.vhd', mode='ast')
except VHDLSyntaxError as e:
    print(f'Expected syntax error: {e}')
"
```

### Performance Verification
- **AST Mode**: < 100ms for simple entities
- **pyVHDLModel Mode**: < 500ms for simple entities (acceptable overhead)
- **Memory Usage**: < 50MB additional for pyVHDLModel bundle

---

## Documentation Updates

### README.md Updates

#### PyHDLio-dev/README.md
```markdown
# PyHDLio Development Repository

Enhanced PyHDLio with pyVHDLModel integration for rich VHDL object hierarchy.

## Features

- **Dual Access Modes**:
  - Lightweight PyHDLio AST parsing
  - Rich pyVHDLModel object hierarchy
- **Port Group Analysis**: Source-proximity-based port grouping
- **Comprehensive Reporting**: Multiple output formats
- **Minimal Footprint**: Optional pyVHDLModel integration

## Quick Start

```bash
# Setup
git clone --recurse-submodules <repo-url>
cd PyHDLio-dev
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install
pip install -e ./PyHDLio
pip install .[dev]

# Run unified example (demonstrates both AST and pyVHDLModel approaches)
.venv\Scripts\python.exe PyHDLio\examples\vhdl\simple\simple.py
```
```

#### PyHDLio/README.md
```markdown
# PyHDLio

HDL parsing library with optional pyVHDLModel integration.

## Installation

```bash
pip install hdlio
```

## Usage

```python
from hdlio.vhdl.parse_vhdl import parse_vhdl

# PyHDLio AST (lightweight)
ast = parse_vhdl("entity.vhd", mode='ast')

# pyVHDLModel objects (rich, optional)
entities = parse_vhdl("entity.vhd", mode='pyVHDLModel')
```
```

---

## Risk Mitigation

### Potential Issues and Solutions

| Risk | Impact | Mitigation |
|------|--------|------------|
| pyVHDLModel API changes | High | Pin to specific version, maintain fork |
| Bundle size too large | Medium | Include only essential modules |
| Performance degradation | Medium | Profile and optimize conversion layer |
| Import conflicts | Low | Use proper namespacing |
| Test suite complexity | Low | Modular test design |

### Rollback Strategy

If integration fails:
1. **Remove pyVHDLModel submodule**: `git submodule deinit pyVHDLModel`
2. **Remove bundle directory**: Delete `hdlio/vhdl/pyVHDLModel/`
3. **Revert parser changes**: Remove `mode='pyVHDLModel'` support
4. **Keep existing functionality**: PyHDLio AST mode remains intact

---

## Success Metrics

### Technical Metrics
- [ ] All existing tests continue to pass
- [ ] New pyVHDLModel tests achieve >90% coverage
- [ ] Both example modes work correctly
- [ ] Bundle size < 50KB
- [ ] Performance overhead < 5x for pyVHDLModel mode

### Usability Metrics
- [ ] Clear documentation with examples
- [ ] Intuitive API design
- [ ] Backwards compatibility maintained
- [ ] Error messages are helpful

### Maintenance Metrics
- [ ] Code follows existing patterns
- [ ] Minimal coupling between components
- [ ] Easy to update pyVHDLModel version
- [ ] Fork can be maintained independently

---

## Future Enhancements

### Phase 2 Possibilities
- **Advanced Port Analysis**: Port dependency analysis
- **Entity Relationships**: Architecture and component analysis
- **VHDL Generation**: Convert pyVHDLModel objects back to VHDL
- **IDE Integration**: Language server protocol support
- **Performance Optimization**: Caching and incremental parsing

### Ecosystem Integration
- **Cocotb Integration**: Generate testbench stubs
- **Synthesis Tool Support**: Export to various tool formats
- **Documentation Generation**: Auto-generate entity documentation
- **Static Analysis**: VHDL coding style and best practices checking

---

## Conclusion

This plan provides a structured approach to integrating pyVHDLModel into PyHDLio while maintaining the project's lightweight philosophy. The dual-mode approach allows users to choose the right tool for their needs:

- **PyHDLio AST**: Fast, lightweight, perfect for simple analysis
- **pyVHDLModel**: Rich, comprehensive, ideal for complex analysis

The modular design ensures that the integration doesn't compromise PyHDLio's core functionality while opening up new possibilities for VHDL analysis and manipulation.