import pygame
from math import sin, cos, atan, degrees

class Bullet:
	Projectiles

	def __init__(self, player_pos, enemy_pos, img):
		enemy_x, enemy_y = enemy_pos
		player_x, player_y = player_pos
		angle = degrees(atan((enemy_y - player_y) / (enemy_x - player_x)))
		self.x, self.y = enemy_x, enemy_y
		self.img = img
	
	de