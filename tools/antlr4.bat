@echo off
set "TOOLS_DIR=%~dp0"
set "VHDL_DIR=%TOOLS_DIR%..\PyHDLio\pyhdlio\vhdl\grammar"
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o "%VHDL_DIR%" "%VHDL_DIR%/vhdl.g4"
