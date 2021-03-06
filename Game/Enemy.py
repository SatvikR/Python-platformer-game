import pygame
from .Meatball import Meatball
from .Bullet import Bullet
from .Highscores.read_write import read_data
class Enemy:
	enemies = []
	base_spawn_rate = 10 # We will use this later ... Maybe for making them spawn more at higher scores
	multiplier = 0.1
	enemy_img = pygame.image.load("./assets/images/enemy.png")
	target_player = None
	enemiesspawned = 0

	def __init__(self, img, x, y, platform):
		self.img = img
		self.x = x
		self.y = y
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		Enemy.enemies.append(self)
		self.cor_platform = platform # Platform underneath
		self.frame = 0
		self.health_multiplier = 1 * Enemy.enemiesspawned
		self.health = 4 * self.health_multiplier
		Enemy.enemiesspawned += 1
		print(self.health)
	def update(self):
		self.check_bullet_collision()
		if self.cor_platform.moving: # Move if platform underneath is moving
			self.x += self.cor_platform.x_vel
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

		if self.timer % 240 == 0: # Once per 4 seconds
			Meatball((self.target_player.x, self.target_player.y), (self.x, self.y), pygame.image.load("./assets/images/meatball.png"))
			print(self.target_player.multiplier)

		self.timer += 1

	def check_bullet_collision(self):
		for bullet in Bullet.bullets:
			if bullet.rect.colliderect(self.rect):
				self.health = self.health - 1
				if self.health <= 0:
					self.enemies.remove(self)
					data = read_data('data.json')
					self.target_player.coins += data['coin_multiplier'] * 10
					return # Leave loop if hit by bullet

	def draw(self, screen, offset):
		screen.blit(self.img, (self.x, self.y + offset))
