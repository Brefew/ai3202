#Ian Moore 
#Assignemtn 6: Bayes Net Disease Probability 

import argparse
import re

def subArgs(character, net):
    eventList = []
    for char in character:
        if char == 'c' or char == 'C':
            eventList.append(net.getNode('cancer'))
        elif char == 'd' or char == 'D':
            eventList.append(net.getNode('dys'))
        elif char == 's' or char == 'S':
            eventList.append(net.getNode('smoking'))
        elif char == 'p' or char == 'P':
            eventList.append(net.getNode('pollution'))
        elif char == 'x' or char == 'X':
            eventList.append(net.getNode('xray'))
        else:
            continue
    return eventList
            
class Node(object):
    
    def __init__(self, name):
        
        self.name = name
        self.cond = None  #dict of conditional probabilities
        self.parents = None  #List of parent Nodes
        self.prior = None #prior probabilities
        self.true = True
        self.false = False

    def getName(self):
        return self.name

    def getParents(self):
        return self.parents

    def getCond(self):
        return self.cond

    def getPrior(self):
        return self.prior

    def setPrior(self, prior):
        self.prior = prior
        return


class Net(object):

    def __init__(self):
        self.nodeDict = {}

    def insertNode(self, node, dep):
        self.nodeDict[node] = dep

    def jointProb(self, events):
        if len(events) is 2:
            ev0 = events[0]
            ev1 = events[1]
            ev0_par = events[0].getParents()
            ev1_p = events[1].getParents()
            ev0_c = self.nodeDict[ev0]
            ev1_c = self.nodeDict[ev1]
            if ev0_par is None and ev1_p is None:
                retdict = {
                        (ev0.true, ev1.true):ev0.prior*ev1.prior,
                        (ev0.true, ev1.false):ev0.prior*(1-ev1.prior),
                        (ev0.false, ev1.true):(1-ev0.prior)*ev1.prior,
                        (ev0.false, ev1.false):(1-ev0.prior)*(1-ev1.prior)
                        }
                        
                desc = "Variable order: " + ev0.getName() + ', '+ev1.getName()
                return (desc, retdict)
            elif len(ev0_c) is 0 and len(ev1_c) is 0:
                prob_ev0 = self.marginalProb([ev0])[1][True]
                prob_ev1 = self.marginalProb([ev1])[1][True]
                retdict = {
                        (ev0.true, ev1.true):prob_ev0*prob_ev1,
                        (ev0.true, ev1.false):prob_ev0*(1-prob_ev1),
                        (ev0.false, ev1.true):(1-prob_ev0)*prob_ev1,
                        (ev0.false, ev1.false):(1-prob_ev0)*(1-prob_ev1)
                        }
                desc = "Variable order: "+ev0.getName()+', '+ev1.getName()
                return (desc, retdict)
            else: #In this case, a conditional probability is required
                (desc, ret) = self.condProb(ev0, [ev1])
                prob = self.marginalProb([ev1])[1][True]
                for key, val in ret.iteritems():
                    if key[1] is True:
                        ret[key] = val*prob
                    else:
                        ret[key] = val*(1-prob)
                desc = ev0.name+' '+ev1.name
                return (desc, ret)
        else:
            return
    
    def condProb(self, event0, events1): #conditional probability for 1 and 1
        if len(events1) is 1:
            ev1 = events1[0]
            ev1_p = ev1.getParents()
            if ev1_p is None:
                ev1_p = []
            ev0 = event0
            ev0_par = ev0.getParents()
            if ev0_par is None:
                ev0_par = []
            if ev1 in ev0_par:
                prob_ev1 = self.marginalProb([ev1])[1][True]
                prob_ev0 = ev0.getCond()
                prob_ev0_T = 0 
                prob_ev0_F = 0
                if ev0.name is 'cancer':
                    if ev1.name is 'pollution':
                        sprob = self.getNode('smoking').prior
                        pprob = self.getNode('pollution').prior
                        prob_ev0_T = prob_ev0[(True, True)]*sprob*pprob
                        prob_ev0_T = prob_ev0_T+prob_ev0[(True, False)]*(1-sprob)*pprob
                        prob_ev0_T = prob_ev0_T/pprob
                        prob_ev0_F = prob_ev0[(False, True)]*sprob*(1-pprob)
                        prob_ev0_F = prob_ev0_F+prob_ev0[(False, False)]*(1-sprob)*(1-pprob)
                        prob_ev0_F = prob_ev0_F/(1-pprob)

                    else:
                        sprob = self.getNode('smoking').prior
                        pprob = self.getNode('pollution').prior
                        prob_ev0_T = prob_ev0[(True, True)]*sprob*pprob
                        prob_ev0_T = prob_ev0_T+prob_ev0[(False, True)]*(1-pprob)*sprob
                        prob_ev0_T = prob_ev0_T/sprob
                        prob_ev0_F = prob_ev0[(True, False)]*pprob*(1-sprob)
                        prob_ev0_F = prob_ev0_F+prob_ev0[(False, False)]*(1-sprob)*(1-pprob)
                        prob_ev0_F = prob_ev0_F/(1-sprob)
                else:
                    prob_ev0_T = prob_ev0[True]
                    prob_ev0_F = prob_ev0[False]
                retdict = {
                        (ev0.true, ev1.true):prob_ev0_T,
                        (ev0.true, ev1.false):prob_ev0_F,
                        (ev0.false, ev1.true):1-prob_ev0_T,
                        (ev0.false, ev1.false):1-prob_ev0_F
                        }
                desc = 'Variable order: '+ev0.name+' given '+ev1.name
                return (desc, retdict)

            elif ev0 in ev1_p:
                desc, rets = self.condProb(ev1, [ev0])
                prob = self.marginalProb([ev1])[1][True]
                prob2 = self.marginalProb([ev0])[1][True]
                tmp = rets[(True, False)]
                rets[(True, False)] = rets[(False, True)]
                rets[(False, True)] = tmp
                for key, val in rets.iteritems():
                    if key[0] is True:
                        val = val*prob2
                    else:
                        val = val*(1-prob2)
                    if key[1] is True:
                        rets[key] = val/prob
                    else:
                        rets[key] = val/(1-prob)
                return desc, rets
            else:  #case ev1 is an ancestor of ev0
                
                if len(ev0_par) is not 0:
                    cancerN = self.getNode('cancer')
                    pollN = self.getNode('pollution').prior
                    smokingN = self.getNode('smoking').prior
                    (desc, cancProb) = self.marginalProb([ev0_par[0]])
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
                    retdict = {}
                    retdict[True, True] = (v1*(v3+v4)+v2*(v5+v6))/(v3+v4+v5+v6)
                    retdict[False, True] = 1-retdict[True, True]

                    #v1(v3+v4)+v2(v5+v6)
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

                    retdict[True, False] = (v1*(v3+v4)+v2*(v5+v6))/(v3+v4+v5+v6)
                    retdict[False, False] = 1-retdict[True, False]
                    desc = ev0.name+' '+ev1.name
                    return (desc, retdict)

                #case ev0 is an ancestor of en1
                else:
                    (desc, rets) = self.condProb(ev1, [ev0])
                    desc = ev0.name+' '+ev1.name
                    p = ev0.prior
                    (d, ret) = self.marginalProb([ev1])
                    p2 = ret[True]
                    retdict = {}
                    retdict[True,True] = rets[True, True]*p/p2
                    retdict[True, False] = rets[False, True]*p/(1-p2)
                    retdict[False, True] =  1-retdict[True, True]
                    retdict[False, False] =  1-retdict[True, False]
                    return (desc, retdict)
            return
                

    def marginalProb(self, event):
        target = event[0]
        if target.getParents() is None:
            retdict = {
                    target.true:target.getPrior(),
                    target.false:1-target.getPrior()
                    }
            desc = 'Variable Key Order: '+target.getName()
            return (desc,retdict)
        elif target.getName() is 'cancer':
            p0 = target.getParents()[0]
            p1 = target.getParents()[1]
            pcancer = 0
            for key, val in target.cond.iteritems():
                p0factor = p0.prior if key[0] is p0.true else 1-p0.prior
                p1factor = p1.prior if key[1] is p1.true else 1-p1.prior
                pcancer = pcancer + val*p0factor*p1factor
            retdict = {
                    target.true:pcancer,
                    target.false:1-pcancer
                    }
            desc = 'Variable Key Order: '+target.getName()
            return(desc, retdict)
        else:
            p0 = target.getParents()[0]
            ptarget = 0
            p0prior = self.marginalProb([p0])[1][p0.true]
            for key, val in target.cond.iteritems():
                p0factor =  p0prior if key is p0.true else 1-p0prior
                ptarget = ptarget + val*p0factor

            retdict = {
                    target.true:ptarget,
                    target.false:1-ptarget
                    }
            desc = 'Variable Key Order: '+target.getName()
            return (desc, retdict)
        
    def getNode(self, nodeName):
        for key, val in self.nodeDict.iteritems():
            if key.getName() == nodeName:
                return key

def main():

	parser = argparse.ArgumentParser(description = 'Calculator for Bayes Net Probabilities')
	parser.add_argument('-p', nargs='+', help = 'Update prior for Smoking')
	
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-g', metavar='Conditional', nargs='+', help='conditional probability')
	group.add_argument('-j', metavar='Joint', nargs='+', help='joint probability')
	group.add_argument('-m', metavar='Marginal', nargs='+', help='marginal probability')
	
	parser.set_defaults(p=None, j=None, m=None, g=None)
	
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
	p = cancerNode.parents
	cancerNode.cond = {
		(p[0].false, p[1].true): 0.05,
		(p[0].false, p[1].false): 0.02,
		(p[0].true, p[1].true): 0.03,
		(p[0].true, p[1].false): 0.001
	}
	
	xrayNode.parents = [cancerNode]
	p = xrayNode.parents
	xrayNode.cond = {
		(p[0].true): 0.9,
		(p[0].false): 0.2
	}
	
	dysNode.parents = [cancerNode]
	p = dysNode.parents
	dysNode.cond = {
		(p[0].true): 0.65,
		(p[0].false): 0.30
	}
	
	bayesNet.insertNode(smokingNode, [cancerNode])
	bayesNet.insertNode(pollutionNode, [cancerNode])
	bayesNet.insertNode(cancerNode, [xrayNode, dysNode])
	bayesNet.insertNode(xrayNode, [])
	bayesNet.insertNode(dysNode, [])
	
	
	#setting the priors if its flagged
	if priorArgs is not None:
	    setValue = float(priorArgs[1])
	    if priorArgs[0] == 'S':
	        editNode = bayesNet.getNode('smoking')
	        editNode.setPrior(setValue)
	    else:
	        editNode = bayesNet.getNode('pollution')
	        editNode.setPrior(setValue)
	events = None
	#finding which probability we're returning
	if args.j is not None:
	    eventlist = subArgs(list(args.j[0]), bayesNet)
	    (desc, ret) = bayesNet.jointProb(eventlist)
	    params = args.j[0]
	    print desc
	    if re.search("[PSCXD]", params) is not None:
	        pass
	    elif re.search('~', params) is not None:
	        pass
	    else:
	        pass
	    print ret
	#pipe has to be in quotes for this to work?
	elif args.g is not None:
	    splitargs = list(args.g[0])
	    splitdex = splitargs.index('|')
	    target = splitargs[0:splitdex]
	    conditions = splitargs[splitdex+1:]
	    ev0 = subArgs(target, bayesNet)
	    ev1 = subArgs(conditions, bayesNet)
	    (desc, ret) = bayesNet.condProb(ev0[0], ev1)
	    print desc
	    if re.search("[PSCXD]", target[0]) is not None:
	        if re.search("[PSCXD]", conditions[0]) is not None:
	            print ret
	        elif re.search("~", conditions[0]) is not None:
	            for key, val in ret.iteritems():
	                if key[1] is False:
	                    print key, ret[key]
	        else:
	            for key, val in ret.iteritems():
	                if key[1] is True:
	                    print key, ret[key]
	    
	    elif re.search("~", target[0]) is not None:
	        if re.search("[PSCXD]", conditions[0]) is not None:
	            for key, val in ret.iteritems():
	                if key[0] is False:
	                    print key,ret[key]
	        elif re.search("~", conditions[0]) is not None:
	            for key, val in ret.iteritems():
	                if key[0] is False and key[1] is False:
	                    print key, ret[key]
	        else:
	            for key, val in ret.iteritems():
	                if key[0] is False and key[1] is True:
	                    print key, ret[key]
	    
	    else:
	        if re.search("[PSCXD]", conditions[0]) is not None:
	            for key, val in ret.iteritems():
	                if key[0] is True:
	                    print key,ret[key]
	        elif re.search("~", conditions[0]) is not None:
	            for key, val in ret.iteritems():
	                if key[0] is True and key[1] is False:
	                    print key, ret[key]
	        else:
	            for key, val in ret.iteritems():
	                if key[0] is True and key[1] is True:
	                    print key, ret[key]
	
	else:
	    eventlist = subArgs(list(args.m[0]), bayesNet)
	    (desc, ret) = bayesNet.marginalProb(eventlist)
	    params = args.m[0]
	    event = eventlist[0]
	    print 'In the case of pollution, True corresponds to Low'
	    if re.search("[PSCXD]", params) is not None:
	        print desc
	        print ret
	    elif re.search('~', params) is not None:
	        print desc + ' False'
	        print ret[event.false]
	    else:
	        print desc + ' True'
	        print ret[event.true]

if __name__ == "__main__": main()
