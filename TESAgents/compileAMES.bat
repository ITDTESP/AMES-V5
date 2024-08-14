set AMESDir=%cd%/../

cd %AMESDir%
call ant clean
call ant jar

cd %AMESDir%/TESAgents