import os
import math,sys

# Given two rows ids as upindex and downindex and rows it calculates the time difference between both time stamps
def timeDiff(upindex, downindex, sample):
		# alclating time in seconds
		sec1= float(sample[upindex][5])*3600 + float(sample[upindex][6])*60 + float(sample[upindex][7]) + float(sample[upindex][8])/1000
		sec2= float(sample[downindex][5])*3600 + float(sample[downindex][6])*60 + float(sample[downindex][7]) + float(sample[downindex][8])/1000 
		time_diff = sec1 - sec2
		return round(time_diff,3)

# Saves the mood analyzed data in the format of continuos data (character wise files) 
def saveHoldData(Hold, folder):
	for i in range(97,123):
		s = ''
		for j in Hold[i-97]:
			s+= str(j)
			s+= '\n'
		file = open('MoodData/'+folder+'/hold_time/'+chr(i).upper()+'.txt', 'w')
		file.write(s)

# Reads the dictionary Lat with all the combinations and saves as files
def saveLatData(Lat, folder):
	for i in range(97,123):
		for j in range(i,123):
			s = ''
			for k in Lat[chr(i)+chr(j)]:
				s+= str(k)
				s+= '\n'
			file = open('MoodData/'+folder+'/latencies/'+chr(i).upper()+chr(j).upper()+'.txt', 'w')
			file.write(s)

# Update the holddata and latency data using every corresponding mood  
def getfeatures(sample, HoldData, LatData):
	numSamples = len(sample)
	currentChar = ''
	i = 0
	Skippedchar = 0
	# Interating over all the samples form a given txt file
	while(i<numSamples):
		if sample[i][1].isalpha():
			# KeyDown means we have to search for hold time
			if (sample[i][0]=='KeyDown'):
				currentChar = sample[i][1]
				j = i+1
				# Finding the next same charater
				while(j<numSamples):
					if(sample[j][1]==currentChar):
						holdtime = timeDiff(j, i, sample)
						break
					j+=1
				if(holdtime<2):
					# Adding the holdtime to holdtime list
					HoldData[ord(currentChar)-97].append(holdtime) 
			# Keydown means we have to find for latency
			elif(sample[i][0]=='KeyUp'):
				j = i+1
				# Looping until next keyDown
				while(j<numSamples and sample[j][0]!='KeyDown'):
					j+=1
				if(j!=numSamples and sample[j][1].isalpha()):
					valid = 1
				else:
					valid = 0
				if(valid):
					# We have to add latencies for BA in the same file as AB 
					if(ord(sample[i][1])<ord(sample[j][1])):
						a = sample[i][1]
						b = sample[j][1]
					else:
						a = sample[j][1]
						b = sample[i][1]
					lattime = timeDiff(j,i,sample)
					if(lattime<2):
						LatData[a+b].append(lattime)					

		i+=1
	return HoldData, LatData
				
# Extracts array for a text files
def openfile(s):
	f = open(s,'r')
	content = f.read()
	rows = content.split('\n')
	data = []
	for i in xrange(len(rows)):
		if('Key' in rows[i]): 
			data.append([])
			temp = rows[i].split('\t')[:-1]
			data[i].append(temp[0])
			data[i].append(temp[1])
			timestamp = temp[2]
			time = timestamp.split(':')
			for j in range(7):
				data[i].append(int(time[j]))
	f.close()
	return data

def main():
	num_characters = 26
	moodslocations = ['Neutral', 'Emotional/Happy', 'Emotional/Sad']
	for moodfolder in moodslocations:
		print moodfolder
		HoldData = []
		LatData= {}
		for i in range(num_characters):
		 	HoldData.append([])
		# print HoldData
		for i in range(26):
			for j in range(i,26):
				LatData[chr(97+i)+chr(97+j)] = []
		# print LatData
		dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
		for dr in dirs:
			if('sentence' in dr):
				Featurefiles = [files for root, dirs, files in os.walk("./"+dr+"/"+moodfolder)][0]
				for file in Featurefiles:
					print "./"+dr+"/"+moodfolder+"/"+file
					data = openfile("./"+dr+"/"+moodfolder+"/"+file)
		
					# data = openfile("./sentence/Neutral/1.txt")
					HoldData, LatData = getfeatures(data, HoldData, LatData)
		# print HoldData
		saveHoldData(HoldData,moodfolder)
		saveLatData(LatData,moodfolder)

if __name__ == '__main__':
 	main()