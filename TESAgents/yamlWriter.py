import sys
import os
import yaml

YAMLPath = "./yamlFiles/"
TSAgent = 'ames' 

input_file_name = sys.argv[1] + ".dat"
current_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.abspath(os.path.join(current_directory, '..', 'data'))
input_data_file = os.path.join(data_directory, input_file_name)
print(f"Data directory: +{data_directory}")

NLSE = None
NTxBus = None

if len(sys.argv) == 4:
    ITD = int(sys.argv[2])
    TxBus = int(sys.argv[3])
if len(sys.argv) == 3:
    ITD = int(sys.argv[2])
    TxBus = 1
if len(sys.argv) == 2:
    ITD = 0
    TxBus = 1

try:
    with open(input_data_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                if parts[0] == 'NLSE':
                    NLSE = int(parts[1])  
                elif parts[0] == 'NumberOfBuses':
                    NTxBus = int(parts[1]) 
except FileNotFoundError:
    print(f"Error: The file {input_data_file} was not found.")

# NLSE = int(sys.argv[1])
# NTxBus = int(sys.argv[2])
# ITD = int(sys.argv[3])
# TxBus = int(sys.argv[4])
	
print("NLSE:", NLSE,"NTxBus:", NTxBus, "ITD:", ITD, "TxBus:", TxBus) 
NHours = 24

auction_datayaml = {}
auction_datayaml['name'] = TSAgent
auction_datayaml['time_delta'] = '1s'
auction_datayaml['broker'] = 'tcp://localhost:5570'
auction_datayaml['values'] = {}
#auction_datayaml['values']['LoadCheck'] = {'topic': 'player/LoadCheck', 'default': 1}

for k in range(NLSE):
	auction_datayaml['values']['loadforecastRTM_LSE'+str(k+1)] = {'topic': 'NetLoadForecastRTM/loadforecastRTM_LSE'+str(k+1), 'default': 1}
	for j in range(NHours):
		auction_datayaml['values']['loadforecastDAM_LSE'+str(k+1)+'_H'+str(j+1)] = {'topic': 'NetLoadForecastDAM/loadforecastDAM_LSE'+str(k+1)+'_H'+str(j+1), 'default': 1}

if ITD == 1:
	for n in range(NTxBus):
		if n == (TxBus-1):
			for j in range(NHours):
				auction_datayaml['values']['DALoadForecast_IDSO_'+ str(TxBus) +'_H'+str(j+1)] = {'topic': 'IDSO_'+ str(TxBus)+'/DALoadForecast_IDSO_'+str(TxBus)+'_H'+str(j+1), 'default': 1}

with open( YAMLPath + TSAgent + '.yaml', 'w') as outfile: 
    yaml.dump(auction_datayaml, outfile, default_flow_style=False)

print("The yamlWriteer.py has executed successfully.")