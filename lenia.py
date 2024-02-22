import pygame
from math import exp,sqrt
from random import uniform
import win32api
import time

WIDTH,HEIGHT = 1280,720
GWIDTH,GHEIGHT = 128,72
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
WINDOW.fill((0,0,0))


def initGrid(w,h):
	grid = []
	for i in range(w):
		grid.append([])
		for j in range(h):
			grid[i].append(0)
			
	return grid	


def randomGrid(w,h):
	grid = []
	for i in range(w):
		grid.append([])
		for j in range(h):
			grid[i].append(uniform(0,1))
			
	return grid	


def f(t : int,a : float = 10, c : float = 90)->int:
	return exp(-((t-c)**2)/(2*(a**2))) - 0.5


def donut(grid : list, w : int, h : int, pos : tuple,r1 : float, r2 : float)->int:
	s = 0
	for x in range(max(0,pos[0]-r2),min(w,pos[0]+r2)):
		for y in range(max(0,pos[1]-r2),min(h,pos[1]+r2)):
			s+= grid[x][y]
	return s	


def smartdonut(grid : list, w : int, h : int, pos : tuple,r1 : float, r2 : float,prev : int, init : bool,dt : float = 1)->int:
	s = 0
	if init:	s = donut(grid, w, h, pos, r1, r2)
	else:
		s = prev
		xmin = pos[0]-r2
		xmax = pos[0]+r2
		ymin = max(0,pos[1]-r2)
		ymax = min(h,pos[1]+r2)
		#add
		if w > xmax:
			for y in range(ymin,ymax): 
				s += grid[xmax][y]
			
		#sub
		if 0 <= xmin:
			for y in range(ymin,ymax): 
				s -= grid[xmin][y]
			
	s -= grid[pos[0]][pos[1]]
	grid[pos[0]][pos[1]] = max(0,min(1,grid[pos[0]][pos[1]] + f(s)*dt))
	
	return s + grid[pos[0]][pos[1]]


def update(grid,w,h):
	m = 0
	
	s = 0
	
	for y in range(0,h):				
			s = smartdonut(grid,w,h,(0,y),5,10,s,True)				
			
			for x in range(1,w):
				s = smartdonut(grid,w,h,(x,y),5,10,s,False)			
				x += 1
				
def updatet(grid,w,h,dt):
	m = 0
	
	s = 0
	
	for y in range(0,h):				
			s = smartdonut(grid,w,h,(0,y),5,10,s,True,dt)				
			
			for x in range(1,w):
				s = smartdonut(grid,w,h,(x,y),5,10,s,False,dt)			
				x += 1
	
			
		

def draw(grid,w,h):
	for x in range(w):
		for y in range(h):
			p = grid[x][y]*255
			if p != 0:
				pygame.draw.rect(WINDOW,(min(255,int(p**(p/150))),min(255,int(p**(p/200))),min(255,int(p**(p/255)))),(x*10,y*10,10,10))
			else:
				pygame.draw.rect(WINDOW,(0,0,0),(x*10,y*10,10,10))
				



def spawnSphere(grid : list, w : int, h : int, pos : tuple,r : float)->int:
	s = 0
	for x in range(max(0,pos[0]-r),min(w,pos[0]+r)):
		for y in range(max(0,pos[1]-r),min(h,pos[1]+r)):
				grid[x][y] = 1
				
def eraseSphere(grid : list, w : int, h : int, pos : tuple,r : float)->int:
	s = 0
	for x in range(max(0,pos[0]-r),min(w,pos[0]+r)):
		for y in range(max(0,pos[1]-r),min(h,pos[1]+r)):
				grid[x][y] = 0

def main():
	run = True
	
	grid = initGrid(GWIDTH,GHEIGHT)
	
	timestamp = time.time()
	while run:
		dt = time.time()-timestamp
		timestamp = time.time()
		draw(grid,GWIDTH,GHEIGHT)
		updatet(grid,GWIDTH,GHEIGHT,dt*10)
	   
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	run = False
			
			if win32api.GetKeyState(0x01) < 0:	#dynamic cell spawner
				
				a,b = pygame.mouse.get_pos()
				
				spawnSphere(grid,GWIDTH,GHEIGHT,(a//10,b//10),3)
				
			if win32api.GetKeyState(0x02) < 0:	#dynamic cell eraser
				
				a,b = pygame.mouse.get_pos()
				
				eraseSphere(grid,GWIDTH,GHEIGHT,(a//10,b//10),10)
			
		pygame.display.update()

if __name__ == '__main__':
	main()

