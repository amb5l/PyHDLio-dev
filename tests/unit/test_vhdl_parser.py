import os
import pytest
from hdlio.vhdl.parse_vhdl import parse_vhdl


class TestVHDLParser:
    """Unit tests for VHDL parser functionality."""

    def test_parse_life_signs_vhdl(self):
        """Test basic VHDL parsing functionality with life_signs.vhd fixture.

        This is a basic 'life signs' test to ensure the VHDL parser can successfully
        parse a minimal VHDL entity without errors.
        """
        # Get the path to the life_signs.vhd fixture
        fixture_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # Go up to tests/
            'fixtures',
            'vhdl',
            'life_signs.vhd'
        )

        # Ensure the fixture file exists
        assert os.path.exists(fixture_path), f"Fixture file not found: {fixture_path}"

        # Parse the VHDL file - this should not raise any exceptions
        parse_tree = parse_vhdl(fixture_path)

        # Basic assertions
        assert parse_tree is not None, "Parse tree should not be None"
        assert isinstance(parse_tree, str), "Parse tree should be a string representation"
        assert len(parse_tree) > 0, "Parse tree should not be empty"

        # The parse tree should contain evidence of parsing the entity
        assert 'life_signs' in parse_tree, "Parse tree should contain the entity name 'life_signs'"

    def test_parse_nonexistent_file(self):
        """Test that parsing a non-existent file raises FileNotFoundError."""
        nonexistent_file = "does_not_exist.vhd"

        with pytest.raises(FileNotFoundError):
            parse_vhdl(nonexistent_file)

    def test_parse_vhdl_file_path_handling(self):
        """Test that the parser correctly handles file paths."""
        # Test with absolute path
        fixture_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # Go up to tests/
            'fixtures',
            'vhdl',
            'life_signs.vhd'
        ))

        # This should work without issues
        parse_tree = parse_vhdl(fixture_path)
        assert parse_tree is not None
        assert 'life_signs' in parse_tree