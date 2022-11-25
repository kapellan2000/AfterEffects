echo off
CD /D "%~dp0"

start ..\..\..\Python37\pythonw.exe .\Scripts\Prism_AfterEffects_MenuTools.py Export
REM exit