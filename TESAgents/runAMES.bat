for /f "tokens=5" %%a in ('netstat -aon ^| find ":5570" ') do taskkill /f /pid %%a

set TESDir=%cd%
set AMESDir=%TESDir%/../

for /d %%i in (../../AMES-V5*) do set AmesVersion=%%i

set fncsLibDir=%AMESDir%\fncsDependencies
set ForecastDir=%TESDir%\forecast
set YAMLFilesDir=%TESDir%\yamlFiles
set OutputFilesDir=%TESDir%\outputFiles
set LogFilesDir=%OutputFilesDir%\logFiles

md %OutputFilesDir% 2> nul
md %LogFilesDir% 2> nul

SET LookForFile1="%OutputFilesDir%\CaseName.txt"
IF EXIST %LookForFile1% del "%OutputFilesDir%\CaseName.txt"

cd %AMESDir%

set FNCS_FATAL=no
set FNCS_LOG_STDOUT=yes
set FNCS_TRACE=no
set FNCS_LOG_LEVEL=DEBUG2
set FNCS_CONFIG_FILE=%YAMLFilesDir%\ames.yaml
start /b cmd /c java -jar -Djava.library.path=%fncsLibDir% "%AMESDir%/dist/%AmesVersion%.jar"^ > %LogFilesDir%/ames.log 2^>^&1

cd %TESDir%

@ECHO OFF
SET LookForFile="%OutputFilesDir%/CaseName.txt"

:CheckForFile
IF EXIST %LookForFile% GOTO FoundIt

GOTO CheckForFile

:FoundIt
ECHO Found: %LookForFile%


set "file_path=%OutputFilesDir%\CaseName.txt"

set /p content=<%file_path%
echo Content: %content%

set Param=MaxDay

for /f "tokens=1,2" %%a in (%AMESDir%/DATA/%content%.dat) do ( if %%a==%Param% set MaxDay=%%b )

set Param=RTOPDur

for /f "tokens=1,2" %%a in (%AMESDir%/DATA/%content%.dat) do ( if %%a==%Param% set RTOPDur=%%b )

set "NHour=4"
set "deltaT=300"
set /a "tmax=%MaxDay%*86400+%NHour%*3600"
set /a "NoOfProcesses=3"
@ECHO ON


set FNCS_CONFIG_FILE=%YAMLFilesDir%/NetLoadForecastDAM.yaml
set FNCS_LOG_LEVEL=
start /b cmd /c python %ForecastDir%/NetLoadForecastDAM.py %tmax% %RTOPDur% %content% ^>%LogFilesDir%/NetLoadForecastDAM.log 2^>^&1

set FNCS_CONFIG_FILE=%YAMLFilesDir%/NetLoadForecastRTM.yaml
set FNCS_LOG_LEVEL=
start /b cmd /c python %ForecastDir%/NetLoadForecastRTM.py %tmax% %RTOPDur% %content% ^>%LogFilesDir%/NetLoadForecastRTM.log 2^>^&1

set FNCS_LOG_LEVEL=DEBUG2
start /b cmd /c fncs_broker %NoOfProcesses% ^>%LogFilesDir%/broker.log 2^>^&1
