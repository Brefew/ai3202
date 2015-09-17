#Ian Moore
#ai3202 Assignment 3

import argparse
import heapq

class Node(object):
	def __init__(self, t, x, y):
		
		self.typ = t
		self.x = x
		self.y = y
		self.distanceToStart = 0
		self.heuristic = 0
		self.f = 0
		self.parent = None
		
	def xval(self):
		return self.x
		
	def yval(self):
		return self.y
		
	def fval(self):
		return self.f
	
	def hval(self):
		return self.heuristic
		
	def setF(self, val):
		self.f = val
		
	def distVal(self):
		return self.distanceToStart
		
	def setParent(self, p):
		self.parent = p
		
	def setDistance(self, val):
		self.distanceToStart = val
		
	def setHeuristic(self, val):
		self.heuristic = val

class Map(object): 
	def __init__(self, l): 
		
		self.map = l
		self.y_bound = len(l)
		if self.y_bound > 0:
			self.x_bound = len(l[0])
		else:
			self.x_bound = 0
			
	def get(self, x, y): #gets the coordinates of x and y
		return self.map[y][x]
		
	def heur1(self):
		for y in range(0, self.y_bound):
			for x in range(0, self.x_bound):
				node = self.get(x,y) #Get x,y coordinate of node
				heuristic = ((self.x_bound-x-1) + (self.y_bound-y-1)) * 10
				node.setHeuristic(heuristic)
				
	def heur2(self):
		
		value = 0
		if self.y_bound > self.x_bound:
			value = self.y_bound-1
		else:
			value = self.x_bound-1
		
		for y in range(0,self.y_bound):
			for x in range(0,self.x_bound):
				node = self.get(x,y) #receives self coordinate
				
				self_x = node.xval()
				self_y = node.yval()
				coordSum = x+y
				heuristic = 0
				
				if coordSum == value:
					heuristic = 14*self_y
				elif coordSum < value:
					heuristic = 14*self_y + 10*(self.x_bound-(self_x + self_y)-1)
				else:
					heuristic = 14*(self.x_bound - self_x -1) + 10*(self_y-(self.x_bound - self_x -1))
					
				node.setHeuristic(heuristic)
				
def parseMap(worldFile): #parses the map file and returns a graph of the data
					
	data = open(worldFile,'r')
	
	matrix = data.readlines() #reads lines
	data.close() #closes file
	
	tiles = []
	for line in matrix:
		tiles.append(line.split()) 
		
	while tiles.count([]) > 0:
		tiles.remove([]) #gets rid of empty lines
		
	#turn tiles into nodes with node attributes
		
	for y in range(0,len(tiles)):
		for x in range(0,len(tiles[0])):
			tiles[y][x] = Node(tiles[y][x],x,y)
			
	worldmap = Map(tiles)
	
	return worldmap

def adjacent(worldMap, node): 
	
	validList = [] #return will give a list of valid nodes
	
	x_bound = worldMap.x_bound-1
	y_bound = worldMap.y_bound-1
	
	for x in range (-1,2):
		x_adj = node.xval() + x
		if (x_adj < 0) or (x_adj > x_bound):
			continue
		
		for y in range (-1,2):
			y_adj = node.yval() + y
			if (y_adj < 0) or (y_adj > y_bound):
				continue
			elif (y == 0) and (x == 0):
				continue
			else:
				adjNode = worldMap.get(x_adj, y_adj)
				if adjNode.typ != '2':
					validList.append(adjNode)
			
	return validList

def aStarSearch(worldMap):
	
	x_start = 0
	y_start = worldMap.y_bound - 1
	
	goal = worldMap.get(worldMap.x_bound-1,0)
	
	openList = []
	closedList = []
	explored = 0
	cost = 0
	
	openList.append((0, worldMap.get(x_start, y_start)))
	
	while openList:
		curr = heapq.heappop(openList)[1]
		heapq.heapify(openList)
		explored += 1
		
		curr_x = curr.xval()
		curr_y = curr.yval()
		curr_dist = curr.distVal()
		closedList.append(curr)
		
		if goal in closedList:
			cost = goal.distVal()
			break
			
		adjNodes = adjacent(worldMap, curr) #Return the list of valid adjacent nodes

		for node in adjNodes: #check if node has been closed
			if node in closedList:
				continue
			
			next_x = node.xval()
			next_y = node.yval()
			
			if (node.fval(), node) in openList:
				next_dist = node.distVal()
				if (curr_x-next_x == 0) or (curr_y-next_y == 0):
					if node.typ == '0':
						if (curr_dist + 10) < next_dist:
							openList.remove((node.fval(), node))
							node.setParent(curr)
							node.setDistance(curr_dist + 10)
							node.setF(node.distVal() + node.hval())
							openList.append((node.fval(),node))
					else:
						if (curr_dist + 20) < next_dist:
							openList.remove((node.fval(),node))
							node.setParent(curr)
							node.setDistance(curr_dist + 20)
							node.setF(node.distVal() + node.hval())
							openList.append((node.fval(),node))
				else:
					if node.typ == '0':
						if (curr_dist + 14) < next_dist:
							openList.remove((node.fval(), node))
							node.setParent(curr)
							node.setDistance(curr_dist + 14)
							node.setF(node.distVal() + node.hval())
							openList.append((node.fval(), node))
					else:
						if (curr_dist + 24) < next_dist:
							openList.remove((node.fval(), node))
							node.setParent(curr)
							node.setDistance(curr_dist + 24) 
							node.setF(node.distVal() + node.hval())
							openList.append((node.fval(), node))
			
			#This finds if node is not in current list
			#and where it is positioned relative to the current node
			else:
				node.setParent(curr)
				if (curr_x-next_x == 0) or (curr_y-next_y == 0):
					if node.typ == '0':
						node.setDistance(curr_dist + 10)
					else:
						node.setDistance(curr_dist + 20)
					
					Fval = node.hval() + node.distVal()
					node.setF(Fval)
					heapq.heappush(openList, (Fval,node))
				else:
					if node.typ == '0':
						node.setDistance(curr_dist + 14)
					else:
						node.setDistance(curr_dist + 24)
					
					Fval = node.hval() + node.distVal()
					node.setF(Fval)
					heapq.heappush(openList, (Fval,node))
					
		heapq.heapify(openList)
		
	#Begin printing the path from start to end	
		
	print 'Path to reach goal:\nEND\n',(goal.xval(), goal.yval())
		
	g = goal.parent
		
	while g.parent is not None:
		print (g.xval(), g.yval())
		g = g.parent
		
	print (g.xval(),g.yval()),'\nSTART'
	print 'This path\'s cost: ', cost
	print 'Explored nodes: ',explored
		
	return
	

def main(): 
	
	argParser = argparse.ArgumentParser()
	argParser.add_argument('world', nargs=1, help = 'Name of World File')
	argParser.add_argument('heuristic', type=int, nargs=1, help = 'Type of Heuristic Used')
	
	args = argParser.parse_args()
	
	heur = args.heuristic[0]
	worldFile = args.world[0]
	
	worldMap = parseMap(worldFile)
	
	if heur == 1:
		worldMap.heur1()
	else:
		worldMap.heur2()
		
	aStarSearch(worldMap)

if __name__ == "__main__": main()
