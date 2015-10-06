#Ian Moore
#ai3202 Assignment 3
#With assistance from Dylan's code

import argparse

class Node(object):
	def __init__(self, t, x, y, r):
		
		self.typ = t
		self.x = x
		self.y = y
		self.reward = r
		self.delta = float('inf')
		self.util = 0
		self.optimal = None
		
	def getX(self):
		return self.x
	
	def getY(self):
		return self.y
	
	def getType(self):
		return self.typ
	
	def getReward(self):
		return self.reward
	
	def setUtility(self, value):
		self.util = value
		
	def getUtility(self):
		return self.util
		
	def setOptimal(self, value):
		self.optimal = value
		
	def getOptimal(self):
		return self.optimal
		
	def setDelta(self, value):
		self.delta = value
		
	def getDelta(self):
		return self.delta

class Map(object): 
	def __init__(self, l): 
		
		self.map = l
		self.y_bound = len(l)-1
		if self.y_bound >= 0:
			self.x_bound = len(l[0])-1
		else:
			self.x_bound < 0
			
	def getCoord(self, x, y): #gets the coordinates of x and y
		if x > self.x_bound or x < 0:
			return None
		elif y > self.y_bound or y < 0:
			return None
		elif self.map[y][x].typ == 'wall':
			return None
		else:
			return self.map[y][x]
		
	def printOptimalPath(self):
		for y in range(self.y_bound, -1, -1):
			for x in range(0, self.x_bound + 1):
				if self.getCoord(x,y) is not None:
					print (self.get(x,y).optimal, round(self.get(x,y).utility,2)),
				else:
					print 'Wall',
			print '\n'
				
def parseMap(worldFile): #parses the map file and returns a graph of the data
					
	data = open(worldFile,'r')
	
	mapData = data.readlines() #reads lines
	data.close() #closes file
	
	tiles = []
	for line in mapData:
		tiles.append(line.split()) 
		
	while tiles.count([]) > 0:
		tiles.remove([]) #gets rid of empty lines
	
	tiles.reverse()
	
	#turn tiles into nodes with node attributes
		
	for y in range(0,len(tiles)):
		for x in range(0,len(tiles[0])):
			if tiles[y][x] == '0':
				tiles[y][x] = Node('open', x, y, 0)
			elif tiles[y][x] == '1':
				tiles[y][x] = Node('mountain', x, y, -1)
			elif tiles[y][x] == '2':
				tiles[y][x] = Node('wall', x, y, 0)
			elif tiles[y][x] == '3':
				tiles[y][x] = Node('snake', x, y, -2)
			elif tiles[y][x] == '4':
				tiles[y][x] = Node('barn', x, y, 1)
			else:
				tiles[y][x] = Node('goal', x, y, 50)
			
	worldmap = Map(tiles) #creates a Map opject for use
	
	return worldmap
	
def newUtility(world, node, gamma):
	x_coord = node.getX()
	y_coord = node.getY()
	reward = node.getReward()
	self_util = node.getUtility()

	up = world.getCoord(x_coord, y_coord+1)
	down = world.getCoord(x_coord, y_coord-1)
	left = world.getCoord(x_coord-1, y_coord)
	right = world.getCoord(x_coord+1, y_coord)
	
	up_util = self_util
	down_util = self_util
	left_util = self_util
	right_util = self_util 
	
	if up is not None:
		up_util = up.getUtility()
	if down is not None:
		down_util = down.getUtility()
	if left is not None:
		left_util = left.getUtility()
	if right is not None:
		right_util = right.getUtility()
		
	up_EU = 0.8*up_util + 0.1*left_util + 0.1*right_util
	down_EU = 0.8*down_util + 0.1*left_util + 0.1*right_util
	left_EU = 0.8*left_util + 0.1*down_util + 0.1*up_util
	right_EU = 0.8*right_util + 0.1*up_util + 0.1*down_util
	
	max_EU = max(up_EU, down_EU, left_EU, right_EU)
	
	if max_EU == up_EU:
		return (gamma*up_EU + reward, 'up')
	if max_EU == down_EU:
		return (gamma*down_EU + reward, 'down')
	if max_EU == left_EU:
		return (gamma*left_EU + reward, 'left')
	else:
		return (gamma*right_EU + reward, 'right')

def valueIteration(world, epsilon):
	start = world.getCoord(0,0)
	goal = world.getCoord(world.x_bound, world.y_bound)
	goal.setUtility(50)
	
	gamma = 0.9
	flag = 1
	
	cutoff = epsilon*(1-gamma)/gamma
	
	while flag:
		flag = 0
		
		for x in range(world.x_bound,-1,-1):
			for y in range(world.y_bound,-1,-1):
				curr = world.getCoord(x,y)
				if curr is None:
					continue
				elif curr.typ is 'goal':
					continue
				prev_delta = curr.getDelta()
				curr_util = curr.getUtility()
				if prev_delta < cutoff:
					continue
				else:
					flag = 1
					next_util = newUtility(world, curr, gamma)
					curr.setUtility(next_util[0])
					curr.setOptimal(next_util[1])
					diff = abs(curr_util - next_util[0])
					if diff < prev_delta:
						curr.setDelta(diff)
	
def main(): 
	
	argParser = argparse.ArgumentParser()
	argParser.add_argument('world', nargs=1, help = 'Name of World File')
	argParser.add_argument('epsilon', type=float, nargs=1, help='number used for epsilon')
	args = argParser.parse_args()
	
	epsilon = args.epsilon[0]
	worldFile = args.world[0]
	worldMap = parseMap(worldFile)
	
	valueIteration(worldMap, epsilon)
	
	start = worldMap.getCoord(0,0)
	goal = worldMap.getCoord(worldMap.x_bound, worldMap.y_bound)
	utility = 0
	curr = start
	
	while curr.typ is not 'goal':
		curr_util = curr.util
		utility = utility + curr_util
		curr_x = curr.x
		curr_y = curr.y
		
		
		print 'Utility:', round(utility, 2), (curr_x, curr_y)
		
		next_move = curr.optimal
		if next_move is 'up':
			curr = worldMap.getCoord(curr_x, curr_y+1)
		elif next_move is 'left':
			curr = worldMap.getCoord(curr_x-1, curr_y)
		elif next_move is 'right':
			curr = worldMap.getCoord(curr_x+1, curr_y)
		else:
			curr = worldMap.getCoord(curr_x, curr_y-1)
			
	utility = curr.util + utility
	print 'Utility:', round(utility,2), (curr.x, curr.y)

if __name__ == "__main__": main()
