import pygame
from .Coin import Coin
from .Platform import Platform
from .Highscores.read_write import read_data, dump_data
from .Meatball import Meatball
from .Bullet import Bullet

class Player:
	walk_speed = 10
	start_x = 100
	start_y = 500
	current_pos = 0, 0
	jump_velocity = read_data('data.json')['jump_vel'] # Increase this value to jump higher
	heart_img = pygame.image.load("./assets/images/heart.png")
	gun_img = pygame.image.load("./assets/images/gun.png")
	bullet_img = pygame.image.load("./assets/images/bullet.png")
	
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		Player.current_pos = self.x, self.y
		self.y_velocity = 0
		self.x_velocity = 0
		self.score = 0
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.high = 0
		self.hearts = 5
		self.damage = 0
		self.direction = 'r'
		self.multiplier = 4
		self.coins = read_data('data.json')['coins']
		self.coin_multiplier = read_data('data.json')["coin_multiplier"] # Can be upgraded
		Player.jump_velocity = read_data('data.json')['jump_vel'] # Reloaded because can be upgraded

	def draw(self, screen):
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		if self.x_velocity < 0: # Draw a reversed image if facing to the left
			screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
			screen.blit(self.gun_img, (self.x - self.gun_img.get_width(), self.y - self.img.get_height() / 2))
		else:
			screen.blit(self.img, (self.x, self.y))
			screen.blit(self.gun_img, (self.x + self.img.get_width(), self.y - self.img.get_height() / 2))

	def update_physics(self, screen):

		self.y += self.y_velocity
		self.y_velocity += 1.2
		self.rect = self.img.get_rect(topleft=(self.x, self.y))

		for platform in Platform.platforms: # Checks collisions in all direction and changes velocity accordingly
			if self.rect.colliderect(platform.rect):
				if self.y_velocity > 0 and platform.y + platform.rect.height * 0.2 > self.y + self.rect.height * 0.8:
					self.y = platform.y - self.rect.height + 1.2
					self.y_velocity = 0
				elif self.y_velocity < 0:
					self.y_velocity = 1.2
				elif self.x_velocity > 0 and platform.rect.x > self.x:
					self.x_velocity = 0
				elif self.x_velocity < 0 and platform.rect.x < self.x:
					self.x_velocity = 0

		
		if self.x_velocity > 0: # Check within screen bounds
			if self.x + self.rect.width < screen.get_width():
				self.x += self.x_velocity
		elif self.x_velocity < 0:
			if self.x > 0:
				self.x += self.x_velocity
		
		self.score = (700 - self.y) // 275 # Calculate current score based on y_pos
		if self.score > self.high:
			self.high = self.score

		# self.multiplier = (self.score / 10) + 1

		self.check_bullet_collisions(Meatball.meatballs)
		self.hearts = 5 - int(self.high - self.score) - self.damage

		for coin in Coin.coins:
			if self.rect.colliderect(coin.rect):
				self.coins += 1 * self.coin_multiplier
				Coin.coins.remove(coin)

		data = read_data('data.json')
		data['coins'] = self.coins
		dump_data('data.json', data)

		if self.x_velocity > 0:
			self.direction = 'r'
		elif self.x_velocity < 0:
			self.direction = 'l'

		if self.score == len(Platform.platforms) - 2: # Add more platforms when close to top of current platforms
			Platform.add_plats(15, screen)
		
		

	def spawn_bullet(self):
		if self.direction == 'r':
			Bullet(
				self.bullet_img,
				self.x + self.gun_img.get_width() + self.rect.width,
				self.y + self.img.get_height() / 2,
				0
			)
		else:
			Bullet(
				self.bullet_img,
				self.x - self.gun_img.get_width(),
				self.y + self.img.get_height() / 2,
				180
			)

	def jump(self): # Jump if touching grounds
		if self.y_velocity == 0:
			self.y_velocity = -self.jump_velocity
			self.y += self.y_velocity
			self.y_velocity += 1.2
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

	def check_bullet_collisions(self, meatballs):
		for meatball in meatballs:
			if self.rect.colliderect(meatball.rect):
				self.damage += 1
				meatballs.remove(meatball)

	def draw_hearts(self, screen):
		heart_width = Player.heart_img.get_width() + 3
		for i in range(0, self.hearts):
			screen.blit(Player.heart_img, (
				screen.get_width() - (5 * heart_width) + i * heart_width,
				5
			))