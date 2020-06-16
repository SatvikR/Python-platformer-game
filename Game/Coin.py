import pygame

class Coin:
	coins = []

	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.y_velocity = -10
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.coins.append(self)
		
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))

	@staticmethod
	def draw_all(coin_list, screen):
		for coin in coin_list:
			coin.draw(screen)