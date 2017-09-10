@setlocal enableextensions enabledelayedexpansion
@ECHO OFF
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
set PYTHONPATH=!PYTHONPATH:~0,-10!
python %PYTHONPATH%\Scripts\csgogsilcd
