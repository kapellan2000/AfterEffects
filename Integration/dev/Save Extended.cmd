echo off
CD /D "%~dp0"

start ..\..\..\Python39\pythonw.exe .\Scripts\Prism_AfterEffects_MenuTools.py SaveComment
exit