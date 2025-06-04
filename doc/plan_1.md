# Plan 1: VHDL Entity Reporting with Generics, Ports, and Port Groups

## Overview

**Objective**: Enhance PyHDLio to parse VHDL files and report all entities with their generics and ports. Ports should be accessible both as a flat list and grouped by empty lines/comments between port clauses.

**Current State**:
- ✅ ANTLR4-based VHDL parser exists in `PyHDLio/hdlio/vhdl/parse_vhdl.py`
- ✅ Basic "life signs" test implemented
- ✅ Test infrastructure in place

## Key Deliverables

1. **AST Classes**: VHDL entities, generics, ports, and port groups
2. **Parse Tree Visitor**: Convert ANTLR4 parse trees to structured ASTs with port grouping
3. **Entity Reporter**: Output entity details in flat or grouped format
4. **Comprehensive Tests**: Verify entity extraction and port group handling
5. **Updated Documentation**: Reflect new functionality

## Assumptions

- VHDL grammar supports VHDL-2008+ with entity declarations, generics, ports
- ANTLR4 parser generates correct parse trees for valid VHDL
- Empty lines and comments are preserved in parse tree/token stream
- Python 3.8+ in virtual environment

---

## Implementation Steps

### Step 1: Define AST Classes

**Objective**: Create Python dataclasses for structured VHDL representation

**Tasks**:

1. **Create AST module structure**:
   ```bash
   mkdir -p PyHDLio/hdlio/vhdl/ast
   touch PyHDLio/hdlio/vhdl/ast/__init__.py
   ```

2. **Create `PyHDLio/hdlio/vhdl/ast/ast.py`**:
   ```python
   from dataclasses import dataclass
   from typing import List, Optional

   @dataclass
   class Generic:
       """Represents a VHDL generic parameter."""
       name: str
       type: str
       default_value: Optional[str] = None

   @dataclass
   class Port:
       """Represents a VHDL port."""
       name: str
       direction: str  # "in", "out", "inout"
       type: str
       constraint: Optional[str] = None  # e.g., "(3 downto 0)"

   @dataclass
   class PortGroup:
       """Represents a group of ports separated by empty/comment lines."""
       ports: List[Port]

   @dataclass
   class Entity:
       """Represents a VHDL entity with dual port access."""
       name: str
       generics: List[Generic]
       ports: List[Port]  # Flat list of all ports
       port_groups: List[PortGroup]  # Grouped ports

   @dataclass
   class VHDLModule:
       """Represents a complete VHDL file with multiple entities."""
       entities: List[Entity]
   ```

3. **Update `PyHDLio/hdlio/vhdl/__init__.py`**:
   ```python
   from .ast.ast import Generic, Port, PortGroup, Entity, VHDLModule
   ```

**Expected Outcome**: AST classes ready for parse tree conversion with port group support.

---

### Step 2: Implement Parse Tree Visitor

**Objective**: Create visitor to build AST with port group detection

**Tasks**:

1. **Create `PyHDLio/hdlio/vhdl/visitor.py`**:
   ```python
   from antlr4 import ParseTreeVisitor, Token
   from pyhdlio.vhdl.grammar.vhdlParser import vhdlParser
   from .ast.ast import Generic, Port, PortGroup, Entity, VHDLModule

   class VHDLVisitor(ParseTreeVisitor):
       """Visitor to convert ANTLR4 parse tree to AST with port grouping."""

       def visitDesign_file(self, ctx: vhdlParser.Design_fileContext):
           entities = []
           for design_unit in ctx.design_unit():
               entity = self.visit(design_unit)
               if entity:
                   entities.append(entity)
           return VHDLModule(entities=entities)

       def visitDesign_unit(self, ctx: vhdlParser.Design_unitContext):
           if ctx.library_unit() and ctx.library_unit().primary_unit():
               primary = ctx.library_unit().primary_unit()
               if primary.entity_declaration():
                   return self.visit(primary.entity_declaration())
           return None

       def visitEntity_declaration(self, ctx: vhdlParser.Entity_declarationContext):
           # Extract entity name
           name = ctx.identifier(0).getText()
           generics = []
           ports = []
           port_groups = []

           # Extract generics if present
           if ctx.entity_header() and ctx.entity_header().generic_clause():
               generics = self.visitGeneric_clause(ctx.entity_header().generic_clause())

           # Extract ports with grouping if present
           if ctx.entity_header() and ctx.entity_header().port_clause():
               ports, port_groups = self.visitPort_clause_with_grouping(ctx.entity_header().port_clause())

           return Entity(name=name, generics=generics, ports=ports, port_groups=port_groups)

       def visitGeneric_clause(self, ctx: vhdlParser.Generic_clauseContext):
           generics = []
           if ctx.generic_list():
               for interface in ctx.generic_list().interface_element():
                   generic = self.visitGeneric_interface(interface)
                   if generic:
                       generics.extend(generic)
           return generics

       def visitGeneric_interface(self, interface):
           """Extract generic from interface element."""
           generics = []
           if interface.interface_constant_declaration():
               const_decl = interface.interface_constant_declaration()
               if const_decl.identifier_list() and const_decl.subtype_indication():
                   type_str = const_decl.subtype_indication().getText()
                   default = None
                   if const_decl.expression():
                       default = const_decl.expression().getText()

                   for identifier in const_decl.identifier_list().identifier():
                       generics.append(Generic(
                           name=identifier.getText(),
                           type=type_str,
                           default_value=default
                       ))
           return generics

       def visitPort_clause_with_grouping(self, ctx: vhdlParser.Port_clauseContext):
           """Extract ports and group them based on empty/comment lines."""
           ports = []
           port_groups = []
           current_group = []

           if not ctx.port_list():
               return ports, port_groups

           # Process each interface element
           for interface in ctx.port_list().interface_element():
               interface_ports = self.visitPort_interface(interface)
               ports.extend(interface_ports)
               current_group.extend(interface_ports)

               # Simple grouping: each interface element is its own group
               # TODO: Implement proper empty line/comment detection
               if current_group:
                   port_groups.append(PortGroup(ports=current_group.copy()))
                   current_group = []

           return ports, port_groups

       def visitPort_interface(self, interface):
           """Extract ports from interface element."""
           ports = []
           if interface.interface_signal_declaration():
               signal_decl = interface.interface_signal_declaration()
               if signal_decl.identifier_list() and signal_decl.subtype_indication():
                   direction = "in"  # default
                   if signal_decl.signal_mode():
                       direction = signal_decl.signal_mode().getText()

                   type_str = signal_decl.subtype_indication().getText()

                   for identifier in signal_decl.identifier_list().identifier():
                       ports.append(Port(
                           name=identifier.getText(),
                           direction=direction,
                           type=type_str,
                           constraint=None  # TODO: Extract constraints
                       ))
           return ports
   ```

2. **Update `PyHDLio/hdlio/vhdl/__init__.py`**:
   ```python
   from .ast.ast import Generic, Port, PortGroup, Entity, VHDLModule
   from .visitor import VHDLVisitor
   ```

**Expected Outcome**: VHDLVisitor that builds AST with basic port grouping.

---

### Step 3: Enhance parse_vhdl.py

**Objective**: Add AST mode to parser with error handling

**Tasks**:

1. **Update `PyHDLio/hdlio/vhdl/parse_vhdl.py`**:
   ```python
   from antlr4 import *
   from antlr4.error.ErrorListener import ErrorListener
   from pyhdlio.vhdl.grammar.vhdlLexer import vhdlLexer
from pyhdlio.vhdl.grammar.vhdlParser import vhdlParser
   from .visitor import VHDLVisitor
   from .ast.ast import VHDLModule

   class VHDLSyntaxError(Exception):
       """Exception raised for VHDL syntax errors."""
       pass

   class VHDLErrorListener(ErrorListener):
       """Custom error listener for VHDL parsing."""

       def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
           raise VHDLSyntaxError(f"Syntax error at line {line}, column {column}: {msg}")

   def parse_vhdl(file_path, mode='tree'):
       """Parse a VHDL file and return parse tree or AST.

       Args:
           file_path (str): Path to the VHDL file
           mode (str): 'tree' for string representation, 'ast' for structured AST

       Returns:
           str | VHDLModule: Parse tree string or VHDLModule AST

       Raises:
           FileNotFoundError: If file doesn't exist
           VHDLSyntaxError: If parsing fails
       """
       try:
           input_stream = FileStream(file_path)
       except FileNotFoundError:
           raise FileNotFoundError(f"VHDL file not found: {file_path}")

       lexer = vhdlLexer(input_stream)
       stream = CommonTokenStream(lexer)
       parser = vhdlParser(stream)

       # Add custom error handling
       parser.removeErrorListeners()
       parser.addErrorListener(VHDLErrorListener())

       try:
           tree = parser.design_file()
       except Exception as e:
           raise VHDLSyntaxError(f"Failed to parse {file_path}: {str(e)}")

       if mode == 'ast':
           visitor = VHDLVisitor()
           return visitor.visit(tree)

       return tree.toStringTree(recog=parser)

   if __name__ == "__main__":
       import sys
       if len(sys.argv) != 2:
           print("Usage: python parse_vhdl.py <vhdl_file>")
           sys.exit(1)

       try:
           result = parse_vhdl(sys.argv[1], mode='ast')
           print(f"Parsed module: {result}")
       except (FileNotFoundError, VHDLSyntaxError) as e:
           print(f"Error: {e}")
           sys.exit(1)
   ```

**Expected Outcome**: Parser supports both tree and AST modes with proper error handling.

---

### Step 4: Implement Entity Reporter

**Objective**: Create formatted output for entity information

**Tasks**:

1. **Create `PyHDLio/hdlio/vhdl/reporter.py`**:
   ```python
   from .ast.ast import VHDLModule, Entity, Generic, Port, PortGroup

   def report_entities(module: VHDLModule, group_ports: bool = False) -> str:
       """Generate formatted report of entities with generics and ports.

       Args:
           module: Parsed VHDL module
           group_ports: If True, show ports grouped; otherwise flat list

       Returns:
           Formatted string report
       """
       if not module.entities:
           return "No entities found."

       output = []

       for entity in module.entities:
           output.append(f"Entity: {entity.name}")

           # Report generics
           output.append("  Generics:")
           if entity.generics:
               for generic in entity.generics:
                   default = f" = {generic.default_value}" if generic.default_value else ""
                   output.append(f"    - {generic.name}: {generic.type}{default}")
           else:
               output.append("    None")

           # Report ports
           output.append("  Ports:")
           if group_ports and entity.port_groups:
               for i, group in enumerate(entity.port_groups, 1):
                   output.append(f"    Group {i}:")
                   for port in group.ports:
                       constraint = f" {port.constraint}" if port.constraint else ""
                       output.append(f"      - {port.name}: {port.direction} {port.type}{constraint}")
           elif entity.ports:
               for port in entity.ports:
                   constraint = f" {port.constraint}" if port.constraint else ""
                   output.append(f"    - {port.name}: {port.direction} {port.type}{constraint}")
           else:
               output.append("    None")

           output.append("")  # Blank line between entities

       return "\n".join(output)

   def print_report(module: VHDLModule, group_ports: bool = False):
       """Print entity report to stdout."""
       print(report_entities(module, group_ports=group_ports))
   ```

2. **Update `PyHDLio/hdlio/vhdl/__init__.py`**:
   ```python
   from .ast.ast import Generic, Port, PortGroup, Entity, VHDLModule
   from .visitor import VHDLVisitor
   from .reporter import report_entities, print_report
   ```

3. **Update example `PyHDLio/examples/vhdl/simple/simple.py`**:
   ```python
   import os
   from hdlio.vhdl.parse_vhdl import parse_vhdl, VHDLSyntaxError
   from hdlio.vhdl.reporter import print_report

   def main():
       """Demonstrate VHDL parsing and entity reporting."""
       vhdl_file = os.path.join(os.path.dirname(__file__), "simple.vhd")

       try:
           # Parse as AST
           module = parse_vhdl(vhdl_file, mode='ast')

           print("=== Flat Ports ===")
           print_report(module, group_ports=False)

           print("=== Grouped Ports ===")
           print_report(module, group_ports=True)

       except FileNotFoundError:
           print(f"Error: {vhdl_file} not found")
       except VHDLSyntaxError as e:
           print(f"Syntax error: {e}")
       except Exception as e:
           print(f"Unexpected error: {e}")

   if __name__ == "__main__":
       main()
   ```

**Expected Outcome**: Working entity reporter with example demonstrating both modes.

---

### Step 5: Add Comprehensive Tests

**Objective**: Ensure functionality works correctly with edge cases

**Tasks**:

1. **Update `tests/unit/test_vhdl_parser.py`**:
   ```python
   import os
   import pytest
   from hdlio.vhdl.parse_vhdl import parse_vhdl, VHDLSyntaxError
   from hdlio.vhdl.reporter import report_entities

   class TestVHDLParser:
       """Unit tests for VHDL parser functionality."""

       def test_parse_life_signs_vhdl(self):
           """Test basic VHDL parsing with life_signs.vhd fixture."""
           fixture_path = os.path.join(
               os.path.dirname(os.path.dirname(__file__)),
               'fixtures', 'vhdl', 'life_signs.vhd'
           )

           # Test tree mode
           parse_tree = parse_vhdl(fixture_path, mode='tree')
           assert parse_tree is not None
           assert isinstance(parse_tree, str)
           assert 'life_signs' in parse_tree

       def test_parse_life_signs_ast(self):
           """Test AST parsing with life_signs.vhd fixture."""
           fixture_path = os.path.join(
               os.path.dirname(os.path.dirname(__file__)),
               'fixtures', 'vhdl', 'life_signs.vhd'
           )

           module = parse_vhdl(fixture_path, mode='ast')
           assert module is not None
           assert len(module.entities) == 1
           assert module.entities[0].name == "life_signs"
           assert len(module.entities[0].ports) == 0
           assert len(module.entities[0].generics) == 0

       def test_parse_nonexistent_file(self):
           """Test parsing non-existent file raises FileNotFoundError."""
           with pytest.raises(FileNotFoundError):
               parse_vhdl("does_not_exist.vhd")

       def test_entity_reporting(self):
           """Test entity reporting functionality."""
           fixture_path = os.path.join(
               os.path.dirname(os.path.dirname(__file__)),
               'fixtures', 'vhdl', 'life_signs.vhd'
           )

           module = parse_vhdl(fixture_path, mode='ast')
           report = report_entities(module)

           assert "Entity: life_signs" in report
           assert "Generics:" in report
           assert "Ports:" in report

       def test_invalid_mode(self):
           """Test invalid mode parameter."""
           fixture_path = os.path.join(
               os.path.dirname(os.path.dirname(__file__)),
               'fixtures', 'vhdl', 'life_signs.vhd'
           )

           # Should default to tree mode for invalid mode
           result = parse_vhdl(fixture_path, mode='invalid')
           assert isinstance(result, str)
   ```

2. **Create test fixture `tests/fixtures/vhdl/entity_with_ports.vhd`**:
   ```vhdl
   library IEEE;
   use IEEE.STD_LOGIC_1164.ALL;

   entity test_entity is
       generic (
           WIDTH : integer := 8;
           DEPTH : natural := 16
       );
       port (
           clk   : in  STD_LOGIC;
           reset : in  STD_LOGIC;
           data  : out STD_LOGIC_VECTOR(WIDTH-1 downto 0)
       );
   end test_entity;
   ```

3. **Add test for entity with ports**:
   ```python
   def test_entity_with_ports_and_generics(self):
       """Test parsing entity with ports and generics."""
       fixture_path = os.path.join(
           os.path.dirname(os.path.dirname(__file__)),
           'fixtures', 'vhdl', 'entity_with_ports.vhd'
       )

       module = parse_vhdl(fixture_path, mode='ast')
       assert len(module.entities) == 1

       entity = module.entities[0]
       assert entity.name == "test_entity"

       # Check generics
       assert len(entity.generics) == 2
       generic_names = [g.name for g in entity.generics]
       assert "WIDTH" in generic_names
       assert "DEPTH" in generic_names

       # Check ports
       assert len(entity.ports) == 3
       port_names = [p.name for p in entity.ports]
       assert "clk" in port_names
       assert "reset" in port_names
       assert "data" in port_names
   ```

**Expected Outcome**: Comprehensive test suite covering basic functionality and edge cases.

---

### Step 6: Update Documentation

**Objective**: Document new functionality for users and developers

**Tasks**:

1. **Update main `README.md`** (already done in previous steps - verify it includes entity reporting features)

2. **Update `tests/README.md`** to include information about new test fixtures and AST testing

3. **Create example documentation in `PyHDLio/examples/README.md`**:
   ```markdown
   # PyHDLio Examples

   ## VHDL Entity Reporting

   The `simple.py` example demonstrates how to:
   - Parse VHDL files into ASTs
   - Report entities with their generics and ports
   - Use both flat and grouped port reporting

   ### Running the Example

   ```bash
   cd PyHDLio/examples/vhdl/simple
   python simple.py
   ```

   ### Expected Output

   ```
   === Flat Ports ===
   Entity: counter
     Generics:
       None
     Ports:
       - clk: in STD_LOGIC
       - reset: in STD_LOGIC
       - count: out STD_LOGIC_VECTOR

   === Grouped Ports ===
   Entity: counter
     Generics:
       None
     Ports:
       Group 1:
         - clk: in STD_LOGIC
         - reset: in STD_LOGIC
         - count: out STD_LOGIC_VECTOR
   ```
   ```

**Expected Outcome**: Clear documentation for new features with working examples.

---

### Step 7: Testing and Refinement

**Objective**: Ensure robust implementation

**Tasks**:

1. **Run tests and fix issues**:
   ```bash
   python -m pytest tests/ -v
   ```

2. **Test with real VHDL files**:
   ```bash
   python PyHDLio/examples/vhdl/simple/simple.py
   ```

3. **Refine implementation based on grammar**:
   - Verify ANTLR4 grammar rule names match visitor methods
   - Check token stream handling for port grouping
   - Add proper constraint extraction

4. **Handle edge cases**:
   - Empty VHDL files
   - Entities with no ports or generics
   - Complex generic types and default values
   - Multi-line port declarations

**Expected Outcome**: Robust, tested implementation ready for production use.

---

## Success Criteria

- ✅ Parse VHDL files into structured ASTs
- ✅ Extract entities with generics (name, type, default)
- ✅ Extract ports (name, direction, type, constraint)
- ✅ Support both flat and grouped port access
- ✅ Comprehensive test coverage
- ✅ Working examples and documentation
- ✅ Error handling for invalid VHDL

## Risk Mitigation

1. **Grammar Compatibility**: Test with actual VHDL grammar rules early
2. **Token Stream Access**: Verify ANTLR4 token stream provides needed information
3. **Complex VHDL**: Start with simple cases, gradually add complexity
4. **Performance**: Monitor parsing speed with large VHDL files

## Next Steps

1. **Start with Step 1**: Create AST classes and test immediately
2. **Incremental Development**: Test each step before proceeding
3. **Early Validation**: Run examples after Steps 2-3 to verify approach
4. **Grammar Alignment**: Adjust visitor based on actual grammar rules

This plan provides a structured approach to implementing VHDL entity reporting with clear milestones and success criteria.
