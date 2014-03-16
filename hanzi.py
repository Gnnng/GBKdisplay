# coding=utf8
import pygame
import struct

from pygame.locals import *
from sys import exit

SCREEN_SIZE = (800, 600)
pygame.init()


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("中文显示")

qu = 47;
wei = 16;

hzk = open('Hzk16', 'rb')

# pointSize = (1, 1)

def updateHanzi(pos, size, q, w):
	hzk.seek(32*((qu-1)*94+wei-1))
	char = hzk.read(32)
	x, y = pos
	pointSize = (size, size)
	board = pygame.Surface((16*pointSize[1], 16*pointSize[0]))
	foreColor = pygame.Surface(pointSize)
	backColor = pygame.Surface(pointSize)

	pygame.draw.rect(foreColor, Color('red'), (0, 0, pointSize[1], pointSize[0]))
	pygame.draw.rect(backColor, Color('black'), (0, 0, pointSize[1], pointSize[0]))

	for i in range(16):
		s = struct.unpack('h', char[2*i+1]+char[2*i])[0]
		for j in range(15, -1, -1):
			if (s & (1 << j)) is not 0:
				# board.set_at(((15-j), i), Color('red'))
				board.blit(foreColor, ((15-j)*pointSize[1], i*pointSize[0]))
			else:
				board.blit(backColor, ((15-j)*pointSize[1], i*pointSize[0]))
				# board.set_at(((15-j), i), Color('black'))
	screen.blit(board, pos)

ctrlFlag = False
shiftFlag = False
posx, posy = (400 ,300)
cursorVelocity = 10
psize = 2
charSpeed = 1000
clock = pygame.time.Clock()

move = {K_LEFT:0, K_RIGHT:0, K_UP:0, K_DOWN:0}
# pygame.key.set_repeat(50, 50)
while True:
	timePassed = clock.tick()
	timePassedSecs = timePassed / 1000.0
	cursorVelocity = timePassedSecs * charSpeed

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYUP:
			if (event.key == K_LCTRL): 
				ctrlFlag = False
			if (event.key == K_LSHIFT): 
				shiftFlag = False
			if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
				move[event.key] = 0
		if event.type == KEYDOWN:
			if (event.key == K_LCTRL): 
				ctrlFlag = True
				print "ctrl down"
			if (event.key == K_LSHIFT): 
				shiftFlag = True
				print "shift down"
			if (event.key == K_ESCAPE): exit()
			if ctrlFlag and not shiftFlag:
				if (event.key == K_LEFT) and (wei > 1): wei = wei-1
				if (event.key == K_RIGHT) and (wei < 86): wei = wei+1
				if (event.key == K_UP) and (qu > 1): qu = qu-1
				if (event.key == K_DOWN) and (qu < 94): qu = qu+1
			# if not ctrlFlag and shiftFlag:
			if (event.key == K_PAGEUP) and (psize < 30): psize = psize + 1
			if (event.key == K_PAGEDOWN) and (psize > 1): psize = psize - 1
			if not ctrlFlag and not shiftFlag:
			# 	if (event.key == K_LEFT) and (posx > 0): posx = posx - cursorVelocity
			# 	if (event.key == K_RIGHT) and (posx < SCREEN_SIZE[0]): posx = posx + cursorVelocity
			# 	if (event.key == K_UP) and (posy > 0): posy = posy - cursorVelocity
			# 	if (event.key == K_DOWN) and (posy < SCREEN_SIZE[1]): posy = posy + cursorVelocity
				if (event.key == K_LEFT) and (posx > 0): 
					move[K_LEFT] = cursorVelocity				
				if (event.key == K_RIGHT) and (posx < SCREEN_SIZE[0]): 
					move[K_RIGHT] = cursorVelocity
				if (event.key == K_UP) and (posy > 0): 
					move[K_UP] = cursorVelocity
				if (event.key == K_DOWN) and (posy < SCREEN_SIZE[1]): 
					move[K_DOWN] = cursorVelocity
	posx -= move[K_LEFT]
	posx +=	move[K_RIGHT]
	posy -= move[K_UP]
	posy += move[K_DOWN]

	screen.fill(0)
	updateHanzi((posx, posy), psize, qu, wei)
	pygame.display.update()
