@echo off
set "TOOLS_DIR=%~dp0"
set "VHDL_DIR=%TOOLS_DIR%..\PyHDLio\pyhdlio\vhdl\grammar"
set "VHDL_LEXER=%VHDL_DIR%\VHDLLexer.g4"
set "VHDL_PARSER=%VHDL_DIR%\VHDLParser.g4"

java -jar %TOOLS_DIR%\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o "%VHDL_DIR%" "%VHDL_LEXER%"
java -jar %TOOLS_DIR%\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o "%VHDL_DIR%" "%VHDL_PARSER%"
