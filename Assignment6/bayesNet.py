#Ian Moore
#Assignment 6: Bayes Nets

import argparse
import re

def subArgs(symbols, net):
	eventList = []
	for i in symbols:
		if i == 'p' or i == 'P':
			eventList.append(net.getNode('pollution'))
		elif i == 's' or i == 'S':
			eventList.append(net.getNode('smoking'))
		elif i == 'c' or i == 'C':
			eventList.append(net.getNode('cancer'))
		elif i == 'd' or i == 'D':
			eventList.append(net.getNode('dys'))
		elif i == 'x' or i == 'X':
			eventList.append(net.getNode('xray'))
		else:
			continue
	return eventList

class Node(object):
	
	def __init__(self, name):
		
		self.name = name
		self.parents = None
		self.prior = None
		self.cond = None
		self.true = True
		self.false = False
		
	def getName(self):
		return self.name
		
	def getParents(self):
		return self.parents
		
	def getPrior(self):
		return self.prior
		
	def setPrior(self, prior):
		self.prior = prior
		
	def getCond(self):
		return self.cond
		
class Net(object):
	
	def __init__(self):
		self.nodeDict = {}
		
	def insertNode(self, node, dep):
		self.nodeDict[node] = dep
		
	def jointProb(self, events):
		if len(events) is 2:
			ev0 = events[0]
			ev1 = events[1]
			ev0_p = events[0].getParents()
			ev1_p = events[1].getParents()
			ev0_c = self.nodeDict[ev0]
			ev1_c = self.nodeDict[ev1]
			
			if ev0_p is None and ev1_p is None:
				ret = {
					(ev0.true, ev1.true):ev0.prior*ev1.prior,
					(ev0.true, ev1.false):ev0.prior*(1-ev1.prior),
					(ev0.false, ev1.true):(1-ev0.prior)*ev1.prior,
					(ev0.false, ev1.false):(1-ev0.prior)*(1-ev1.prior)
				}
				
				desc = 'Variable order:' + ev0.getName() + ','+ev1.getName()
				
				return(desc, ret)
			
			elif len(ev0_c) is 0 and len(ev1_c) is 0:
				prob_ev0 = self.marginalProb([ev0])[1][True]
				prob_ev1 = self.marginalProb([ev1])[1][True]
				
				ret = {
					(ev0.true, ev1.true):prob_ev0*prob_ev1,
					(ev0.true, ev1.false):prob_ev0*(1-prob_ev1),
					(ev0.false, ev1.true):(1-prob_ev0)*prob_ev1,
					(ev0.false, ev1.false):(1-prob_ev0)*(1-prob_ev1)
				}
				
				desc = 'Variable order:' + ev0.getName() + ',' + ev1.getName()
				
				return(desc, ret)
			
			else: #In this case, we will need conditional dependency
				(desc, ret) = self.condProb(ev0, [ev1])
				prob = self.marginalProb([ev1])[1][True]
				for key, value in ret.iteritems():
					if key[1] is True:
						ret[key] = value*prob
					else:
						ret[key] = value*(1-prob)
				desc = ev0.name + '' + ev1.name
				
				return(desc,ret)
		else:
			return
			
	def condProb(self,event0, events1): #conditional probability for 1 and 1
		if len(events1) is 1:
			ev1 = events1[0]
			ev1_p = ev1.getParents()
			if ev1_p is None:
				ev1_p = []
			ev0 = event0
			ev0_p = ev0.getParents()
			if ev0_p is None:
				ev0_p = []
			if ev1 in ev0_p:
				prob_ev1 = self.marginalProb([ev1])[1][True]
				prob_ev0 = ev0.getCond()
				prob_ev0_T = 0
				prob_ev0_F = 0
				if ev0.name is 'cancer':
					if ev1.name is 'pollution':
						prob_s = self.getNode('smoking').prior
						prob_p = self.getNode('pollution').prior
						prob_ev0_T = prob_ev0[(True, True)]*prob_s*prob_p
						prob_ev0_T = prob_ev0_T + prob_ev0[(True, False)]*(1-prob_s)*prob_p
						prob_ev0_T = prob_ev0_T/prob_p
						prob_ev0_F = prob_ev0[(False, True)]*prob_s*(1-prob_p)
						prob_ev0_F = prob_ev0_F+prob_ev0[(False, False)]*(1-prob_s)*(1-prob_p)
						prob_ev0_F = prob_ev0_F/(1-prob_p)
						
					else:
						prob_s = self.getNode('smoking').prior
						prob_p = self.getNode('pollution').prior
						prob_ev0_T = prob_ev0[(True, True)]*prob_s*prob_p
						prob_ev0_T = prob_ev0_T+prob_ev0[(False, True)]*(1-prob_p)*prob_s
						prob_ev0_T = prob_ev0_T/prob_s
						prob_ev0_F = prob_ev0[(True, False)]*prob_p*(1-prob_s)
						prob_ev0_F = prob_ev0_F+prob_ev0[(False, False)]*(1-prob_s)*(1-prob_p)
						prob_ev0_F = prob_ev0_F/(1-prob_s)
						
				else:
					prob_ev0_T = prob_ev0[True]
					prob_ev0_F = prob_ev0[False]
				
				ret = {
					(ev0.true, ev1.true):prob_ev0_T,
					(ev0.true, ev1.false):prob_ev0_F,
					(ev0.false, ev1.true):1-prob_ev0_T,
					(ev0.false, ev1.false):1-prob_ev0_F
				}
				
				desc = 'Variable order:' + ev0.name + 'given' + ev1.name
				
				return(desc, ret)
				
			elif ev0 in ev1_p:
				desc, rets = self.condProb(ev1, [ev0])
				prob = self.marginalProb([ev1])[1][True]
				prob2 = self.marginalProb([ev0])[1][True]
				temp = rets[(True, False)]
				rets[(True, False)] = rets[(False, True)]
				rets[(False, True)] = temp
				for key, value in rets.iteritems():
					if key[0] is True:
						value = value*prob2
					else:
						value = value*(1-prob2)
					
					if key[1] is True:
						rets[key] = value/prob
					else:
						rets[key] = value/(1-prob)
				return desc,rets
			else: #ev1 is ancestor of ev0
				if len(ev0_p) is not 0:
					cancerN = self.getNode('cancer')
					pollN = self.getNode('pollution').prior
					smokingN = self.getNode('smoking').prior
					(desc, cancerProb) = self.marginalProb([ev0_p[0]])
					v1 = ev0.cond[True]
					v2 = ev0.cond[False]
					#v1(v3+v4)+v2(v5+v6)
					v3 = cancerN.cond[True, True]*pollN*smokingN
					v4 = 0
					if ev1.name is 'smoking':
						v4 = cancerN.cond[False, True]*(1-pollN)*smokingN
					else:
						v4 = cancerN.cond[True, False]*(1-smokingN)*pollN
					v5 = (1-cancerN.cond[True, True])*pollN*smokingN
					v6 = 0
					if ev1.name is 'smoking':
						v6 = (1-cancerN.cond[False, True])*(1-pollN)*smokingN
					else:
						v6 = (1-cancerN.cond[True, False])*(1-smokingN)*pollN
					ret = {}
					ret[True, True] = (v1*(v3+v4)+v2*(v5+v6))/(v3+v4+v5+v6)
					ret[False, True] = 1-ret[True, True]
					#v1(v3+v5)+v2(v5+v6)
					v3 = cancerN.cond[False, False]*(1-pollN)*(1-smokingN)
					v4 = 0
					if ev1.name is 'smoking':
						v4 = cancerN.cond[True, False]*(1-smokingN)*pollN
					else:
						v4 = cancerN.cond[False, True]*(1-pollN)*smokingN
					v5 = (1-cancerN.cond[False, False])*(1-pollN)*(1-smokingN)
					v6 = 0
					if ev1.name is 'smoking':
						v6 = (1-cancerN.cond[True, False])*(1-smokingN)*pollN
					else:
						v6 = (1-cancerN.cond[True, False])*(1-pollN)*smokingN
						
					ret[True, False] = (v1*(v3+v4)+v2*(v5+v6))/(v3+v4+v5+v6)
					ret[False, False] = 1-ret[True, False]
					desc = ev0.name + '' + ev1.name
					
					return(desc, ret)
					
				#case ev0 is ancestor of ev1
				else:
					(desc, rets) = self.condProb(ev1, [ev0])
					desc = ev0.name + '' + ev1.name
					p = ev0.prior
					(d, ret) = self.marginalProb([ev1])
					p2 = ret[True]
					retdict[True, True] = rets[True, True]*p/p2
					retdict[True, False] = rets[False, True]*p/(1-p2)
					retdict[False, True] = 1-retdict[True, True]
					retdict[False, False] = 1-retdict[True, False]
					
					return(desc, retdict)
					
			return
					
	def marginalProb(self, event):
		target = event[0]
		if target.getParents() is None:
			ret = {
				target.true:target.getPrior(),
				target.false:1-target.getPrior()
			}
			
			desc = 'Variable Key Order:' + target.getName()
			return(desc, ret)
		elif target.getName() is 'cancer':
			parent0 = target.getParents()[0]
			parent1 = target.getParents()[1]
			cancer_p = 0
			for key, value in target.cond.iteritems():
				factor_parent0 = parent0.prior if key[0] is parent0.true else 1-parent0.prior
				factor_parent1 = parent1.prior if key[1] is parent1.true else 1-parent1.prior
				cancer_p = cancer_p + value*factor_parent0*factor_parent1
			ret = {
				target.true:cancer_p,
				target.false:1-cancer_p
			}
			desc = "Variable Key Order:" + target.getName()
			
			return(desc, ret)
		else:
			parent0 = target.getParents()[0]
			target_p = 0
			prior_parent0 = self.marginalProb([parent0])[1][parent0.true]
			for key, value in target.cond.iteritems():
				factor_parent0 = prior_parent0 if key is parent0.true else 1-prior_parent0
				target_p = target_p + value*factor_parent0
				
			ret = {
				target.true:target_p,
				target.false:1-target_p
			}
			desc = 'Variable Key Order:' + target.getName()
			
			return(desc, ret)
			
	def getNode(self, name):
		for key, value in self.nodeDict.iteritems():
			if key.getName() == name:
				return key
	

	
def main():
	parser = argparse.ArgumentParser(description = 'Bayes Net Probability Calculator')

	group = parser.add_mutually_exclusive_group(required = True)
	group.add_argument('-g', nargs='+', metavar='conditional', help = 'Conditional Probability')
	group.add_argument('-j', nargs='+', metavar='joint', help = 'Joint Probability')
	group.add_argument('-m', nargs='+', metavar='marginal', help = 'Marginal Probability')

	parser.add_argument('-p', nargs='+', help = 'Prior for smoking or pollution')

	parser.set_defaults(g=None, j=None, m=None, p=None)

	args = parser.parse_args()
	priorArgs = args.p
	
	bayesNet = Net()
	
	smokingNode = Node('smoking')
	pollutionNode = Node('pollution')
	cancerNode = Node('cancer')
	xrayNode = Node('xray')
	dysNode = Node('dys')
	
	smokingNode.prior = 0.3
	pollutionNode.prior = 0.9
	
	cancerNode.parents = [pollutionNode, smokingNode]
	parents = cancerNode.parents
	cancerNode.cond = {
		(parents[0].false, parents[1].true):0.05,
		(parents[0].false, parents[1].false):0.02,
		(parents[0].true, parents[1].true):0.03,
		(parents[0].true, parents[1].false):0.001
	}
	
	xrayNode.parents = [cancerNode]
	parents = xrayNode.parents
	xrayNode.cond = {
		(parents[0].true): 0.9,
		(parents[0].false): 0.2
	}
	
	bayesNet.insertNode(smokingNode, [cancerNode])
	bayesNet.insertNode(pollutionNode, [cancerNode])
	bayesNet.insertNode(cancerNode, [xrayNode, dysNode])
	bayesNet.insertNode(xrayNode, [])
	bayesNet.insertNode(dysNode, [])
	
	
	#Here we set the priors if it's flagged
	if priorArgs is not None:
		setValue = float(priorArgs[1])
		if priorArgs[0] == 'S':
			editNode = bayesNet.getNode('smoking')
			editNode.setPrior(setValue)
		else:
			editNode = bayesNet.getNode('pollution')
			editNode.setPrior(setValue)
	events = None
	
	
	#Here is where we find which probability that needs to be returned
	if args.j is not None:
		eventList = subArgs(list(args.j[0]), bayesNet)
		(desc, ret) = bayesNet.jointProb(eventList)
		params = args.j[0]
		print desc
		if re.search("[PSCDX]", params) is not None:
			pass
		elif re.search('~', params) is not None:
			pass
		else:
			pass
		
		print ret
		
		
	elif args.g is not None:
		split_args = list(args.g[0])
		split_dex = split_args.index("|")
		target = split_args[0:split_dex]
		conditions = split_args[split_dex+1]
		ev0 = subArgs(target, bayesNet)
		ev1 = subArgs(conditions, bayesNet)
		(desc, ret) = bayesNet.condProb(ev0[0], ev1)
		
		print desc
		
		if re.search("[PSCDX]", target[0]) is not None:
			if re.search("[PSCDX]", conditions[0]) is not None:
				print ret
			elif re.search("!", conditions[0]) is not None:
				for key, value in ret.iteritems():
					if key[1] is False:
						print key, ret[key]
			else:
				for key, value in ret.iteritems():
					if key[1] is True:
						print key, ret[key]
		elif re.search("~", target[0]) is not None:
			if re.search("[PSCDX]", conditions[0]) is not None:
				for key, value in ret.iteritems():
					if key[0] is False:
						print key, ret[key]
			elif re.search("~", conditions[0]) is not None:
				for key, value in ret.iteritems():
					if key[0] is False and key[1] is False:
						print key, ret[key]
			else:
				for key, value in ret.iteritems():
					if key[0] is False and key[1] is True:
						print key, ret[key]
		else:
			if re.search("[PSCDX]", conditions[0]) is not None:
				for key, value in ret.iteritems():
					if key[0] is True:
						print key, ret[key]
			elif re.search("~", conditions[0]) is not None:
				for key, value in ret.iteritems():
					if key[0] is True and key[1] is False:
						print key, ret[key]
			else:
				for key, value in ret.iteritems():
					if key[0] is True and key[1] is True:
						print key, ret[key]
	else:
		eventList = subArgs(list(args.m[0]), bayesNet)
		(desc, ret) = bayesNet.marginalProb(eventList)
		params = args.m[0]
		event = eventList[0]
		
		print 'True = Low for Pollution'
		
		if re.search("[PSCDX]", params) is not None:
			print desc 
			print ret
		elif re.search('~', params) is not None:
			print desc + 'False'
			print ret[event.false]
		else:
			print desc + 'True'
			print ret[event.true]

if __name__ == '__main__': main()
