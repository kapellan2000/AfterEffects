@echo off
echo AfterEffects plugin add
echo -----------------

set /p Input=Input path to Prism root: 
cd %~dp0
rmdir /s %Input%"\Plugins\Apps\AfterEffects"
mkdir %Input%"\Plugins\Apps\AfterEffects"
del %Input%"\ProjectFiles\EmptyScenes\EmptyScene After Effects 2021.aep"

xcopy ".\Integration" %Input%"\Plugins\Apps\AfterEffects\Integration" /s /e /y /i /o
xcopy ".\Scripts" %Input%"\Plugins\Apps\AfterEffects\Scripts" /s /e /y /i /o
xcopy ".\UserInterfaces" %Input%"\Plugins\Apps\AfterEffects\UserInterfaces" /s /e /y /i /o

xcopy ".\Export.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Project Browser.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Save Extended.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Save Version.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Settings.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o




xcopy /S /Q /Y /F ".\Integration\EmptyScene After Effects 2021.aep" %Input%"\ProjectFiles\EmptyScenes\"

echo Complite
pause
