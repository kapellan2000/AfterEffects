echo off
CD /D "%~dp0"

start ..\..\..\Python37\pythonw.exe .\Scripts\Prism_AfterEffects_MenuTools.py ProjectBrowser
REM start ..\..\..\Python37\python.exe .\Scripts\Prism_AfterEffects_MenuTools.py ProjectBrowser
exit