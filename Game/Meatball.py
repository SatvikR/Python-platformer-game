import pygame
from math import sin, cos, atan, degrees, radians

class Meatball:
	meatballs = []
	speed = 5

	def __init__(self, player_pos, enemy_pos, img):
		enemy_x, enemy_y = enemy_pos
		player_x, player_y = player_pos
		try:
			self.angle = degrees(atan((enemy_y - player_y) / (enemy_x - player_x)))
		except ZeroDivisionError:
			self.angle = 0
		self.x, self.y = enemy_x, enemy_y
		self.img = img
		Meatball.meatballs.append(self)
	
	def update(self):
		self.x += int(self.speed * cos(radians(self.angle)))
		self.y += int(self.speed * sin(radians(self.angle)))
		

	def draw(self, screen, offset):
		screen.blit(self.img, (self.x, self.y + offset))
		# temporary
		if self.x >= 1200 or self.x <= 0:
			self.meatballs.remove(self)
	