set AMESDir=%cd%\..\
set TempFiles=%AMESDir%\tempFiles\PyomoTempFiles
cd %TempFiles%

del *.lp
del *.log
del *.script
del *.sol
del *.dat

cd %AMESDir%/TESAgents
