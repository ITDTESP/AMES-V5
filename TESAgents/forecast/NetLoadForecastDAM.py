import sys
import json
import click

from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
import fncs



def NetLoadScenarioDataJsonFormat(filename):
	NLSE = 0
	NDay = 0
	f = open(FilePath + filename,'r')
	NetLoadScenarioData = json.load(f)
	NLSE = len(NetLoadScenarioData)
	NDay = [len(val) for key, val in NetLoadScenarioData[0].items()]
	return NDay[0], NLSE, NetLoadScenarioData

def loadforecast_RP(h, d, filename):
	time = []
	NDay, NLSE, NetLoadScenarioData = NetLoadScenarioDataJsonFormat(filename)
	ListLSENodes = []
	loadforecastRTM = [[] for i in range(3)]
	loadforecastDAM = []
	unit = 1 #1000000000
	for ele in NetLoadScenarioData:
		for k in ele:
			ListLSENodes.append(k)
	#print('ListLSENodes:', ListLSENodes)
	d1 = 0 if d >= NDay else d
	
	print('h, d:', h, d)
	#24 hour vector -> DAM
	x = (d* day_len)*unit + (H-1) * (hour_len)*unit # - 1*unit
	print('x:',x)
	print('NLSE:'+str(NLSE))
	for i in range(NLSE):
		for j in range(24):
			#load.append((x,'loadforecastDAM_h'+str(j), float(loadforecast[j])*1)) # replace 1 with
			load.append((x,'loadforecastDAM_LSE' +str(i+1)+ '_H'+str(j+1), float(NetLoadScenarioData[i][ListLSENodes[i]][d1][j])))
	return None

def get_number(value):
	return float(''.join(ele for ele in value if ele.isdigit() or ele == '.'))





if len(sys.argv) == 4:
	tmax = int(sys.argv[1])
	RTOPDur = int(sys.argv[2])
	name = str(sys.argv[3])
	
	
	print('NetLoadForecastDAM, tmax, RTOPDur', tmax, RTOPDur)
elif len(sys.argv) == 1:
	tmax = 2 * 24 * 3600 #172800
	RTOPDur = 5
	print('NetLoadForecastDAM, tmax, RTOPDur', tmax, RTOPDur)
else:
	print ('usage: python loadforecast.py [tmax deltaT]')
	sys.exit()

fncs.initialize()

ts = 0
timeSim = 0

H = 6
M = 60 
min_len = 60
hour_len = 60 * min_len #100 # in s
day_len = 24* hour_len # in s
prev_hour = 0
prev_day = 0

deltaT = RTOPDur * min_len
print('deltaT:', deltaT)

load = []

FileName = f'{name}DAM.json'
FilePath = './forecast/data/'

# error msg if not present 

import os

def check_file_in_folder(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_name} is not present in the folder {folder_path}")

    # Continue with your code if the file exists
    # For example, you can open the file or perform any other operations

try:
    check_file_in_folder(FilePath, FileName)
    # Continue with your code if the file exists
except FileNotFoundError as e:
    click.echo(e)
    # Handle the error or exit the program as needed





while ts <= tmax:
	print ('time step: ',ts, flush = True)
	day = int(ts / day_len)# - ts % 2400 # day = 24*100s $ day_len = 2400s
	hour = int((ts - (day * day_len)) / hour_len)
	minute = (ts - (day * day_len) - hour * hour_len)/60
	#print ('day:', day, 'hour:', hour, 'minute:', minute, flush= True)

	if (day>0):
		if (ts%((day)*(day_len))) == 0:
			#print ('ts2: ',ts, flush = True)
			loadforecast_RP(hour, day, FileName)
	#print ('ts3: ',ts, flush = True)
	if(len(load)!=0):
		#print ('ts3: ',ts, flush = True)
		for i in range(len(load)):
			#print('ts3:', ts, 'load[i][0]:', load[i][0], flush=True)
			if(ts >= load[i][0]):
				#print ('ts4: ',ts, flush = True)
				if(ts == load[i][0]):
					print('Publishing load forecast to AMES: ', str(load[i][0]), str(load[i][1]), load[i][2], flush = True)
					fncs.publish(str(load[i][1]), load[i][2])
			else:
				break
	if(ts < (timeSim + deltaT)) :
		ts = fncs.time_request(timeSim + deltaT)
	else:
		#print('time_granted2:', ts, flush = True)
		timeSim = timeSim + deltaT
		ts = fncs.time_request(timeSim + deltaT)

	#print('Day:', day, 'Hour:', hour, flush=True)
	prev_day = day
	prev_hour = hour


fncs.finalize()