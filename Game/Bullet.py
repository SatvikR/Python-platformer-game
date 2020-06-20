import pygame
from math import sin, cos, atan, degrees, radians

class Bullet:
	bullets = []

	def __init__(self, player_pos, enemy_pos, img):
		enemy_x, enemy_y = enemy_pos
		player_x, player_y = player_pos
		self.angle = degrees(atan((enemy_y - player_y) / (enemy_x - player_x)))
		self.x, self.y = enemy_x, enemy_y
		self.img = img
	
	def update(self):
		self.x += int(cos(radians(self.angle)))
		self.y += int(sin(radians(self.angle)))
	
	def draw(self, screen, offset):
		screen.blit(self.img, (self.x, self.y + offset))