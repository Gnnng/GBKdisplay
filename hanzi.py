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
		self.rgb = (0, 0, 0)
		self.color = Color('black')
		self.pixelSize = 2
		self.hanziSize = (16*self.pixelSize, 16*self.pixelSize)
		self.image = pygame.Surface(self.hanziSize)
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0] - self.hanziSize[0]/2, self.pos[1] - self.hanziSize[1]/2)
		self.key = {K_LEFT:0, K_RIGHT:0, K_UP:0, K_DOWN:0, K_r:0, K_g:0, K_b:0}
		self.style = K_BACKQUOTE;
		self.adjustSizeFlag f= False
		self.selectCharFlag = False
	def keySet(self, event):
		mods = pygame.key.get_mods()
		if (mods & KMOD_LALT):
			self.adjustSizeFlag = True
		else:
			self.adjustSizeFlag = False
		if (mods & KMOD_LCTRL):
			self.selectCharFlag = True
		else:
			self.selectCharFlag = False
		if (event.type == KEYDOWN) or (event.type == KEYUP) and event.key in self.key:
			self.key[event.key] = (event.type == KEYDOWN)
		if (event.type == KEYDOWN) and (event.key == K_BACKQUOTE):
			self.style = K_BACKQUOTE
		if (event.type == KEYDOWN) and (event.key >= K_1 and event.key <= K_9):
			self.style = event.key
	timeCount = 0;
	def update(self, timePassed):
		self.timeCount += timePassed
		velocity = timePassed / 1000.0 * self.speed;
		if self.key[K_r] or self.key[K_g] or self.key[K_b]:
			r = self.rgb[0] + self.key[K_r]*(self.key[K_UP] - self.key[K_DOWN])
			g = self.rgb[1] + self.key[K_g]*(self.key[K_UP] - self.key[K_DOWN])
			b = self.rgb[2] + self.key[K_b]*(self.key[K_UP] - self.key[K_DOWN])
			for i in (r, g, b, "done"):
				if (i == "done"):
					self.rgb = (r, g, b)
				elif (i < 0 or i > 255):
					break
			self.color = Color(*(self.rgb))
		elif self.adjustSizeFlag and not self.selectCharFlag:
			self.pixelSize = self.pixelSize + self.key[K_UP] - self.key[K_DOWN]
			if self.pixelSize < 2: self.pixelSize = 2
		elif self.selectCharFlag and not self.adjustSizeFlag:
			if (self.timeCount > 100):
				self.timeCount = 0;
				qu = self.quwei[0] + self.key[K_DOWN] - self.key[K_UP]
				wei = self.quwei[1] + self.key[K_RIGHT] - self.key[K_LEFT]
				if qu >= 1 and qu <= 87 and wei >=1 and wei <= 94:
					self.quwei = (qu, wei)
		else:
			x = self.pos[0] + (self.key[K_RIGHT] - self.key[K_LEFT]) * velocity
			y = self.pos[1] + (self.key[K_DOWN] - self.key[K_UP]) * velocity
			if x >= 0 and x < SCREEN_SIZE[0] and y >= 0 and y < SCREEN_SIZE[1]:
				self.pos = (x, y)
				
		if self.style == K_BACKQUOTE: self.style0()
		if self.style == K_1: self.style1()
		if self.style == K_2: self.style2()
		self.image.set_colorkey(Color('white'))

	def style0(self):
		hzk.seek(32*((self.quwei[0]-1)*94+self.quwei[1]-1))
		char = hzk.read(32)
		self.hanziSize = (16*self.pixelSize, 16*self.pixelSize)
		self.image = pygame.Surface(self.hanziSize)
		self.image.fill(Color('white'))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0] - self.rect.w/2, self.pos[1] - self.rect.h/2)
		pointSize = (self.pixelSize, self.pixelSize)
		foreColor = pygame.Surface(pointSize)
		pygame.draw.rect(foreColor, self.color, (0, 0, pointSize[1], pointSize[0]))
		for i in range(16):
			s = struct.unpack('h', char[2*i+1]+char[2*i])[0]
			for j in range(15, -1, -1):
				if (s & (1 << j)) is not 0:
					self.image.blit(foreColor, ((15-j)*pointSize[1], i*pointSize[0]))
	
	def style1(self):
		hzk.seek(32*((self.quwei[0]-1)*94+self.quwei[1]-1))
		char = hzk.read(32)
		offset = self.pixelSize * 0.5
		self.hanziSize = (16*self.pixelSize, 16*self.pixelSize)
		self.image = pygame.Surface(self.hanziSize)
		self.image.fill(Color('white'))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0] - self.rect.w/2, self.pos[1] - self.rect.h/2)
		pointSize = (self.pixelSize, self.pixelSize)
		foreColor = pygame.Surface(pointSize)
		backColor = pygame.Surface(pointSize)
		pygame.draw.rect(foreColor, self.color, (0, 0, pointSize[1], pointSize[0]))
		for i in range(16):
			s = struct.unpack('h', char[2*i+1]+char[2*i])[0]
			for j in range(15, -1, -1):
				if (s & (1 << j)) is not 0:
					self.image.blit(foreColor, ((15-j)*pointSize[1], i*pointSize[0]))
					# self.image.blit(foreColor, ((15-j)*pointSize[1] - offset, i*pointSize[0]))
					self.image.blit(foreColor, ((15-j)*pointSize[1] + offset, i*pointSize[0]))
					# self.image.blit(foreColor, ((15-j)*pointSize[1], i*pointSize[0] - offset))
					self.image.blit(foreColor, ((15-j)*pointSize[1], i*pointSize[0] + offset))

	def style2(self):
		hzk.seek(32*((self.quwei[0]-1)*94+self.quwei[1]-1))
		char = hzk.read(32)
		offset = self.pixelSize * 0.5
		self.hanziSize = (32*self.pixelSize, 16*self.pixelSize)
		self.image = pygame.Surface(self.hanziSize)
		self.image.fill(Color('white'))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0] - self.rect.w/2, self.pos[1] - self.rect.h/2)
		pointSize = (self.pixelSize, self.pixelSize)
		foreColor = pygame.Surface(pointSize)
		backColor = pygame.Surface(pointSize)
		pygame.draw.rect(foreColor, self.color, (0, 0, pointSize[1], pointSize[0]))
		for i in range(16):
			s = struct.unpack('h', char[2*i+1]+char[2*i])[0]
			for j in range(15, -1, -1):
				if (s & (1 << j)) is not 0:
					self.image.blit(foreColor, ((15-j)*pointSize[1] + 0.5 * self.pixelSize * (16 - i), i*pointSize[0]))
					self.image.blit(foreColor, ((15-j)*pointSize[1] + 0.5 * self.pixelSize * (16 - i) + offset, i*pointSize[0]))
					self.image.blit(foreColor, ((15-j)*pointSize[1] + 0.5 * self.pixelSize * (16 - i), i*pointSize[0] + offset))

clock = pygame.time.Clock()
hanzi = Hanzi()
background = pygame.Surface(SCREEN_SIZE)
background.fill(Color('white'))

while True:
	timePassed = clock.tick()
	
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			exit()
		if event.type == KEYDOWN and event.key == K_SPACE:
			background.blit(hanzi.image, hanzi.rect)
			hanzi = Hanzi()
		hanzi.keySet(event);

	hanzi.update(timePassed)
	screen.blit(background, (0, 0))
	screen.blit(hanzi.image, hanzi.rect)
	pygame.display.update()
