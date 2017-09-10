@ECHO OFF
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
ECHO %PYTHONPATH%
python.exe %PYTHONPATH%\Scripts\csgogsilcd