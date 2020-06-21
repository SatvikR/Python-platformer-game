import pygame

class Coin:
	coins = []
	coin_img = pygame.image.load('./assets/images/coin.png')


	def __init__(self, img, x, y, platform):
		self.img = img
		self.x = x
		self.y = y
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.coins.append(self)
		self.cor_platform = platform # Platform underneath
		print(f"Spawned a Coin at {x}, {y} and moving is {platform.moving}")
		
	def draw(self, screen):
		if self.cor_platform.moving: # Move if platform underneath is moving
			self.x += self.cor_platform.x_vel
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

		screen.blit(self.img, (self.x, self.y))

	@staticmethod
	def draw_all(screen):
		for coin in Coin.coins:
			coin.draw(screen)