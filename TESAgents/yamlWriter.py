import sys
import yaml

YAMLPath = "./yamlFiles/"
TSAgent = 'ames' 


NLSE = int(sys.argv[1])
NTxBus = int(sys.argv[2])
ITD = int(sys.argv[3])
TxBus = int(sys.argv[4])
	
#print("NLSE:", NLSE,"NTxBus:", NTxBus, "ITD:", ITD, "TxBus:", TxBus) 
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