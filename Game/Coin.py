import pygame

class Coin:
	coins = []
	coin_img = pygame.image.load('./assets/images/coin.png')


	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.coins.append(self)
		
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))

	@staticmethod
	def draw_all(screen):
		for coin in Coin.coins:
			coin.draw(screen)