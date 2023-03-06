echo on
CD /D "%~dp0"
CD "C:\Program Files\Prism2"
start "C:\Program Files\Prism2\Python39\python.exe" "c:\ProgramData\Prism2\plugins\AfterEffects\Scripts\Prism_AfterEffects_MenuTools.py" ProjectBrowser
REM start ..\..\..\Python39\python.exe .\Scripts\Prism_AfterEffects_MenuTools.py ProjectBrowser
pause