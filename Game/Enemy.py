import pygame

class Enemy:
	enemies = []
	base_spawn_rate = 10 # We will use this later ... Maybe for making them spawn more at higher scores
	multiplier = 0.1
	enemy_img = pygame.image.load("./assets/images/enemy.png")

	def __init__(self, img, x, y, platform):
		self.img = img
		self.x = x
		self.y = y
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		Enemy.enemies.append(self)
		self.cor_platform = platform # Platform underneath
		print("Entered Enemy intializer")
		print(Enemy.enemies)
	
	def update(self):
		if self.cor_platform.moving: # Move if platform underneath is moving
			self.x += self.cor_platform.x_vel
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

	def draw(self, screen, offset):
		screen.blit(self.img, (self.x, self.y + offset))
