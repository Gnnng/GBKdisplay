#coding=utf8
import pygame
import struct

from pygame.locals import *
from sys import exit

SCREEN_SIZE = (800, 600)
pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("中文显示")
hzk = open('Hzk16', 'rb')

class Hanzi(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.pos = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
		self.speed = 500
		self.quwei = (47, 16)
		self.color = Color('red')
		self.pixelSize = 2
		self.hanziSize = (16*self.pixelSize, 16*self.pixelSize)
		self.image = pygame.Surface(self.hanziSize)
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0] - self.hanziSize[0]/2, self.pos[1] - self.hanziSize[1]/2)
		self.key = {K_LEFT:0, K_RIGHT:0, K_UP:0, K_DOWN:0}
		self.adjustSizeFlag = False
		self.selectCharFlag = False
	def keySet(self, event):
		mods = pygame.key.get_mods()
		if (mods & KMOD_LALT):
			self.adjustSizeFlag = True
			print 'alt'
		else:
			self.adjustSizeFlag = False
		if (mods & KMOD_LCTRL):
			print 'ctrl'
			self.selectCharFlag = True
		else:
			self.selectCharFlag = False
		if (event.type == KEYDOWN) or (event.type == KEYUP) and event.key in self.key:
			self.key[event.key] = (event.type == KEYDOWN)

	def update(self, timePassed):
		velocity = timePassed / 1000.0 * self.speed;
		if self.adjustSizeFlag and not self.selectCharFlag:
			self.pixelSize = self.pixelSize + self.key[K_UP] - self.key[K_DOWN]
			if self.pixelSize < 2: self.pixelSize = 2
		elif self.selectCharFlag and not self.adjustSizeFlag:
			qu = self.quwei[0] + self.key[K_UP] - self.key[K_DOWN]
			wei = self.quwei[1] + self.key[K_RIGHT] - self.key[K_LEFT]
			if qu >= 1 and qu <= 94 and wei >=1 and wei <= 86:
				self.quwei = (qu, wei)
		else:
			x = self.pos[0] + (self.key[K_RIGHT] - self.key[K_LEFT]) * velocity
			y = self.pos[1] + (self.key[K_DOWN] - self.key[K_UP]) * velocity
			if x >= 0 and x < SCREEN_SIZE[0] and y >= 0 and y < SCREEN_SIZE[1]:
				self.pos = (x, y)

		hzk.seek(32*((self.quwei[0]-1)*94+self.quwei[1]-1))
		char = hzk.read(32)
		self.hanziSize = (16*self.pixelSize, 16*self.pixelSize)
		self.image = pygame.Surface(self.hanziSize)
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0] - self.rect.w/2, self.pos[1] - self.rect.h/2)
		pointSize = (self.pixelSize, self.pixelSize)
		foreColor = pygame.Surface(pointSize)
		backColor = pygame.Surface(pointSize)
		pygame.draw.rect(foreColor, Color('red'), (0, 0, pointSize[1], pointSize[0]))
		pygame.draw.rect(backColor, Color('black'), (0, 0, pointSize[1], pointSize[0]))
		for i in range(16):
			s = struct.unpack('h', char[2*i+1]+char[2*i])[0]
			for j in range(15, -1, -1):
				if (s & (1 << j)) is not 0:
					self.image.blit(foreColor, ((15-j)*pointSize[1], i*pointSize[0]))
				else:
					self.image.blit(backColor, ((15-j)*pointSize[1], i*pointSize[0]))
					

clock = pygame.time.Clock()

hanzi = Hanzi();

while True:
	timePassed = clock.tick()
	
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			exit()
		hanzi.keySet(event);

	screen.fill(0)
	hanzi.update(timePassed)
	screen.blit(hanzi.image, hanzi.rect)
	pygame.display.update()
