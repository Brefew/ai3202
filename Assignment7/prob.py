#Ian Moore
#Assignment7

import re
import random

class Node(object):
	def __init__(self, n):
		self.name = n;
		self.prior = None;
		self.prob = None;
		
#Create the nodes for each type
cloud = Node('cloudy')
sprinkler = Node('sprinkler')
rain = Node('rain')
grass = Node('grass')

#Set the priors for each type
cloud.prior = 0.5

sprinkler.prob = {True:0.1, False:0.5}

rain.prob = {True:0.8, False:0.2}

grass.prob = {
	(True, True):0.99,
	(True, False):0.9,
	(False, True):0.9,
	(False, False):0
}

def priorSampling(lst):
	print '___PRIOR SAMPLING___\n'
	
	sampleSize = len(lst)
	cloudCount = 0
	
	print 'Calculating P(C=True):\n'
	
	for l in lst:
		if l['c'] == True:
			cloudCount += 1
	
	print 'Cloudy days:', cloudCount
	print 'Total samples:', sampleSize
	print 'P(C=True:)', cloudCount/float(sampleSize), '\n'
	
	print 'Calculating P(C|R)\n'
	
	rainCount = 0;
	cloudRainCount = 0;
	
	for l in lst:
		if l['r'] == True:
			rainCount += 1
			if l['c'] == True:
				cloudRainCount += 1
				
	print 'Total rainy days:', rainCount
	print 'Total rainy and cloudy days:', cloudRainCount
	print 'P(C|R):', cloudRainCount/float(rainCount), '\n'
	
	print 'Calculating P(S|W):\n'
	
	wetGrassCount = 0
	wetSprinklerCount = 0
	
	for l in lst:
		if l['w'] == True:
			wetGrassCount += 1
			if l['s'] == True:
				wetSprinklerCount += 1
				
	print 'Total days with wet grass:', wetGrassCount
	print 'Total days with wet grass and sprinkler:', wetSprinklerCount
	print 'P(S|W):', wetSprinklerCount/float(wetGrassCount), '\n'
	
	print 'Calculating P(S|C,W):\n'
	
	sprinklerCount = 0
	cloudWetCount = 0
	
	for l in lst:
		if l['c'] == True:
			if l['w'] == True:
				cloudWetCount += 1
				if l['s'] == True:
					sprinklerCount += 1
	
	print 'Total days with wet grass and clouds:', cloudWetCount
	print 'Total days with wet grass, clouds, and sprinklers:', sprinklerCount
	print 'P(S|W,C):', sprinklerCount/float(cloudWetCount), '\n'
	

def rejectionSampling(samples):
	print '___REJECTION SAMPLING___\n'
	
	print 'Calculating P(C):\n'
	
	cloudCount = 0
	
	for s in samples:
		if s <= cloud.prior:
			cloudCount += 1
			
	print 'Total cloudy days:', cloudCount
	print 'Total sampled days:', 100
	print 'P(C):', cloudCount/float(100), '\n'
	
	print 'Calculating P(C|R):\n'
	
	index = 0
	lst = []
	
	while True:
		if index >= 99: 
			break
		
		insert = {}
		currSample = samples[index]
		if currSample <= cloud.prior:
			insert['c'] = True
		else:
			insert['c'] = False
		index += 1
		currSample = samples[index]
		if currSample <= rain.prob[insert['c']]:
			insert['r'] = True
			lst.append(insert)
		else:
			insert['r'] = False
		index += 1
		
	cloudCount = 0
	
	for l in lst:
		if l['c'] == True:
			cloudCount += 1
	
	print 'Total rainy days:', len(lst)
	print 'Total rainy and cloudy days:', cloudCount
	print 'P(C|R):', cloudCount/float(len(lst)), '\n'
	
	print 'Calculating P(S|W):\n'
	
	index = 0
	lst = []
	
	while True:
		if index >= 96:
			break
		insert = {}
		currSample = samples[index]
		if currSample <= cloud.prior:
			insert['c'] = True
		else:
			insert['c'] = False
		cBool = insert['c']
		index += 1
		currSample = samples[index]
		if currSample <= sprinkler.prob[cBool]:
			insert['s'] = True
		else:
			insert['s'] = False
		sBool = insert['s']
		index += 1
		currSample = samples[index]
		if currSample <= rain.prob[cBool]:
			insert['r'] = True
		else:
			insert['r'] = False
		rBool = insert['r']
		index += 1
		if not sBool and not rBool:
			continue
		currSample = samples[index]
		if currSample <= grass.prob[sBool, rBool]:
			insert['w'] = True
			lst.append(insert)
		index += 1
		
	sprinklerCount = 0
	
	for l in lst:
		if l['s'] == True:
			sprinklerCount += 1
			
	print 'Total days with wet grass:', len(lst)
	print 'Total sprinklers on days with wet grass:', sprinklerCount
	print 'P(S|W):', sprinklerCount/float(len(lst)), '\n'
	
	index = 0
	lst = []
	
	while True:
	    if index >= 96:
	        break
	        
	    insert = {}
	    currSample = samples[index]
	    if currSample <= cloud.prior:
	        insert['c'] = True
	    else:
	        index += 1
	        continue
	    index += 1
	    currSample = samples[index]
	    if currSample <= sprinkler.prob[True]:
	        insert['s'] = True
	    else:
	        insert['s'] = False
	    sBool = insert['s']
	    index += 1
	    currSample = samples[index]
	    if currSample <= rain.prob[True]:
	        insert['r'] = True
	    else:
	        insert['r'] = False
	    rBool = insert['r']
	    index += 1
	    if not sBool and not rBool:
	        continue
	    currSample = samples[index]
	    if currSample <= grass.prob[sBool, rBool]:
	        insert['w'] = True
	        lst.append(insert)
	    index += 1
	
	sprinklerCount = 0
	for l in lst:
	    if l['s'] is True:
	        sprinklerCount += 1

	print 'Total cloudy days with wet grass:', len(lst)
	print 'Total cloudy, wet grass days with sprinklers:', sprinklerCount
	print 'P(S|C,W):', sprinklerCount/float(len(lst))
			


def main():
	
	samples = [0.82,	0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,	
	0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	
	0.8,	0.97,	0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19, 	0.6,	
	0.68,	0.36,	0.67,	0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	
	0.83,	0.96,	0.41,	0.65,	0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	
	0.97,	0.95,	0.01,	0.62,	0.32,	0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	
	0.99,	0.79,	0.21,	0.2,	0.43,	0.81,	0.9,	0.0,	0.91,	0.01]

	
	#Generate all samples in the order c->s->r->w
	lst = []
	index = 0
	
	while index < len(samples):
		insert = {}
		#Check cloud's prior: True/False
		if samples[index] <= cloud.prior: 
			insert['c'] = True
		else:
			insert['c'] = False
		index += 1
		cBool = insert['c']
		
		#Check sprinkler GIVEN cloud
		if samples[index] <= sprinkler.prob[cBool]:
			insert['s'] = True
		else:
			insert['s'] = False
		index += 1
		
		#Check rain GIVEN cloud 
		if samples[index] <= rain.prob[cBool]:
			insert['r'] = True
		else:
			insert['r'] = False
		index += 1
		sBool = insert['s']
		rBool = insert['r']
		
		#Check grass GIVEN sprinkler AND rain
		if samples[index] <= grass.prob[sBool, rBool]:
			insert['w'] = True
		else:
			insert['w'] = False
		index += 1
		
		lst.append(insert);
		
	#Prior Sampling
	priorSampling(lst)
	
	#Rejection Sampling
	rejectionSampling(samples)

if __name__ == "__main__": main()
