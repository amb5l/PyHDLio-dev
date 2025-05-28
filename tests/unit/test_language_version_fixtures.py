"""
Unit tests for language version specific fixtures
Tests the comprehensive language version specific fixtures in tests/fixtures/lrm/
"""

import pytest
from pathlib import Path

from PyHDLio.hdlio.core.parsers.vhdl_parser import VHDLParser
from PyHDLio.hdlio.core.parsers.verilog_parser import VerilogParser


class TestVHDLLanguageVersionFixtures:
    """Test VHDL language version specific fixtures"""
    
    @pytest.mark.parametrize("fixture_name,expected_version", [
        ("vhdl_1993_file", "1993"),
        ("vhdl_2000_file", "2000"), 
        ("vhdl_2008_file", "2008"),
        ("vhdl_2019_file", "2019"),
    ])
    def test_vhdl_version_fixture_exists(self, fixture_name, expected_version, request):
        """Test that VHDL version fixtures exist and are readable"""
        fixture_path = request.getfixturevalue(fixture_name)
        assert fixture_path.exists(), f"VHDL {expected_version} fixture file should exist"
        assert fixture_path.is_file(), f"VHDL {expected_version} fixture should be a file"
        assert fixture_path.suffix == ".vhd", f"VHDL {expected_version} fixture should have .vhd extension"
        
        # Verify file is readable and not empty
        content = fixture_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"VHDL {expected_version} fixture should not be empty"
    
    @pytest.mark.parametrize("fixture_name,expected_version", [
        ("vhdl_1993_file", "1993"),
        ("vhdl_2000_file", "2000"),
        ("vhdl_2008_file", "2008"), 
        ("vhdl_2019_file", "2019"),
    ])
    def test_vhdl_version_fixture_parsing(self, fixture_name, expected_version, request):
        """Test that VHDL version fixtures can be parsed successfully"""
        fixture_path = request.getfixturevalue(fixture_name)
        content = fixture_path.read_text(encoding='utf-8')
        
        # Map version to language constant
        version_map = {
            "1993": "VHDL_1993",
            "2000": "VHDL_2000", 
            "2008": "VHDL_2008",
            "2019": "VHDL_2019"
        }
        language = version_map[expected_version]
        
        parser = VHDLParser(language)
        try:
            result = parser.parse(str(fixture_path), content)
            assert result is not None, f"VHDL {expected_version} fixture should parse successfully"
        except Exception as e:
            pytest.fail(f"VHDL {expected_version} parsing failed: {str(e)}")


class TestVerilogLanguageVersionFixtures:
    """Test Verilog language version specific fixtures"""
    
    @pytest.mark.parametrize("fixture_name,expected_version", [
        ("verilog_1995_file", "1995"),
        ("verilog_2001_file", "2001"),
        ("verilog_2005_file", "2005"),
    ])
    def test_verilog_version_fixture_exists(self, fixture_name, expected_version, request):
        """Test that Verilog version fixtures exist and are readable"""
        fixture_path = request.getfixturevalue(fixture_name)
        assert fixture_path.exists(), f"Verilog {expected_version} fixture file should exist"
        assert fixture_path.is_file(), f"Verilog {expected_version} fixture should be a file"
        assert fixture_path.suffix == ".v", f"Verilog {expected_version} fixture should have .v extension"
        
        # Verify file is readable and not empty
        content = fixture_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"Verilog {expected_version} fixture should not be empty"
    
    @pytest.mark.parametrize("fixture_name,expected_version", [
        ("verilog_1995_file", "1995"),
        ("verilog_2001_file", "2001"),
        ("verilog_2005_file", "2005"),
    ])
    def test_verilog_version_fixture_parsing(self, fixture_name, expected_version, request):
        """Test that Verilog version fixtures can be parsed"""
        fixture_path = request.getfixturevalue(fixture_name)
        content = fixture_path.read_text(encoding='utf-8')
        
        # Map version to language constant
        version_map = {
            "1995": "VERILOG_1995",
            "2001": "VERILOG_2001",
            "2005": "VERILOG_2005"
        }
        language = version_map[expected_version]
        
        parser = VerilogParser(language)
        try:
            result = parser.parse(str(fixture_path), content)
            assert result is not None, f"Verilog {expected_version} fixture should parse successfully"
        except Exception as e:
            pytest.fail(f"Verilog {expected_version} parsing failed: {str(e)}")


class TestSystemVerilogLanguageVersionFixtures:
    """Test SystemVerilog language version specific fixtures"""
    
    @pytest.mark.parametrize("fixture_name,expected_version", [
        ("systemverilog_2005_file", "2005"),
        ("systemverilog_2009_file", "2009"),
        ("systemverilog_2012_file", "2012"),
        ("systemverilog_2017_file", "2017"),
    ])
    def test_systemverilog_version_fixture_exists(self, fixture_name, expected_version, request):
        """Test that SystemVerilog version fixtures exist and are readable"""
        fixture_path = request.getfixturevalue(fixture_name)
        assert fixture_path.exists(), f"SystemVerilog {expected_version} fixture file should exist"
        assert fixture_path.is_file(), f"SystemVerilog {expected_version} fixture should be a file"
        assert fixture_path.suffix == ".sv", f"SystemVerilog {expected_version} fixture should have .sv extension"
        
        # Verify file is readable and not empty
        content = fixture_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"SystemVerilog {expected_version} fixture should not be empty"
    
    @pytest.mark.parametrize("fixture_name,expected_version", [
        ("systemverilog_2005_file", "2005"),
        ("systemverilog_2009_file", "2009"),
        ("systemverilog_2012_file", "2012"),
        ("systemverilog_2017_file", "2017"),
    ])
    def test_systemverilog_version_fixture_parsing(self, fixture_name, expected_version, request):
        """Test that SystemVerilog version fixtures can be parsed"""
        fixture_path = request.getfixturevalue(fixture_name)
        content = fixture_path.read_text(encoding='utf-8')
        
        # Map version to language constant  
        version_map = {
            "2005": "SYSTEMVERILOG_2005",
            "2009": "SYSTEMVERILOG_2009",
            "2012": "SYSTEMVERILOG_2012",
            "2017": "SYSTEMVERILOG_2017"
        }
        language = version_map[expected_version]
        
        # SystemVerilog uses the same parser as Verilog for now
        parser = VerilogParser(language)
        try:
            result = parser.parse(str(fixture_path), content)
            assert result is not None, f"SystemVerilog {expected_version} fixture should parse successfully"
        except Exception as e:
            pytest.fail(f"SystemVerilog {expected_version} parsing failed: {str(e)}")


class TestLanguageVersionFixtureCollections:
    """Test the fixture collections work correctly"""
    
    def test_all_vhdl_version_files_collection(self, all_vhdl_version_files):
        """Test that all VHDL version files collection contains expected files"""
        assert len(all_vhdl_version_files) == 4, "Should have 4 VHDL version files"
        
        # Check that all files exist and have correct extensions
        for file_path in all_vhdl_version_files.values():
            assert file_path.exists(), f"VHDL file {file_path} should exist"
            assert file_path.suffix == ".vhd", f"VHDL file {file_path} should have .vhd extension"
    
    def test_all_verilog_version_files_collection(self, all_verilog_version_files):
        """Test that all Verilog version files collection contains expected files"""
        assert len(all_verilog_version_files) == 3, "Should have 3 Verilog version files"
        
        # Check that all files exist and have correct extensions
        for file_path in all_verilog_version_files.values():
            assert file_path.exists(), f"Verilog file {file_path} should exist"
            assert file_path.suffix == ".v", f"Verilog file {file_path} should have .v extension"
    
    def test_all_systemverilog_version_files_collection(self, all_systemverilog_version_files):
        """Test that all SystemVerilog version files collection contains expected files"""
        assert len(all_systemverilog_version_files) == 4, "Should have 4 SystemVerilog version files"
        
        # Check that all files exist and have correct extensions
        for file_path in all_systemverilog_version_files.values():
            assert file_path.exists(), f"SystemVerilog file {file_path} should exist"
            assert file_path.suffix == ".sv", f"SystemVerilog file {file_path} should have .sv extension"
    
    def test_all_language_version_files_collection(self, all_language_version_files):
        """Test that all language version files collection contains all files"""
        expected_total = 4 + 3 + 4  # VHDL + Verilog + SystemVerilog
        assert len(all_language_version_files) == expected_total, f"Should have {expected_total} total language version files"
        
        # Check that all files exist
        for file_path in all_language_version_files:
            assert file_path.exists(), f"Language version file {file_path} should exist"
            assert file_path.suffix in [".vhd", ".v", ".sv"], f"File {file_path} should have valid HDL extension" 