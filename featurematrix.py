#import all required libraries
import string
import pandas as pd
alphabet= list(string.ascii_uppercase)
import os

#define function to get the feature matrix
def feature_matrix(Path):

	#map Hold Time of all Aplhabet to array
	filelist_hold = os.listdir(Path + "hold_time/")
	hold=[]
	for i in filelist_hold:
		if i.endswith(".txt"):  # You could also add "and i.startswith('f')
			with open(Path+ "hold_time/" + i, 'r') as f:
				content= (f.read()).split("\n")
				content = list(filter(None, content))
				hold.append(content)
	filelist_latencies = os.listdir(Path+ "latencies/")
	latencies=[]

	#Extract latency time related to each indivial character
	for latter in alphabet:
		latency=[]
		for i in filelist_latencies:
			if(i.endswith(latter +".txt") or i.startswith(latter)):
				with open(Path+ "latencies/" + i, 'r') as f:
					content= (f.read()).split("\n")
					latency= latency+content
					latency = list(filter(None, latency))
		latencies.append(latency)

	#Append hold time and latecy time of each character to main dataframe

	df_h=pd.DataFrame([],columns=['hold_time'])
	df_l=pd.DataFrame([],columns=['latency_time'])
	h_t = []
	l_t=[]
	for i in range(26):
		if(len(hold[i])<=len(latencies[i])):
			latency_time = [(pd.Series(latencies[i])[0:len(hold[i])]).astype(float)]
			hold_time = [(pd.Series(hold[i])).astype(float)]
			h_t = h_t+hold_time
			l_t = l_t + latency_time
		else:
			hold_time = [(pd.Series(hold[i])[0:len(latencies[i])]).astype(float)]
			latency_time = [(pd.Series(latencies[i])).astype(float)]
			h_t = h_t + hold_time
			l_t = l_t + latency_time
	for i in range(26):
		df2 = pd.DataFrame(h_t[i], columns=['hold_time'])
		df_h= df_h.append(df2, ignore_index=True)
		df2 = pd.DataFrame(l_t[i], columns=['latency_time'])
		df_l= df_l.append(df2, ignore_index=True)
	df= pd.concat([df_h, df_l], axis=1)
	return(df)
