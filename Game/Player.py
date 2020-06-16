import pygame
from .Coin import Coin
from .Platform import Platform
from .Highscores.read_write import read_data, dump_data

class Player:
	walk_speed = 10
	start_x = 100
	start_y = 500
	jump_velocity = 27.5 # Increase this value to jump higher
	heart_img = pygame.image.load("./assets/images/heart.png")
	
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.y_velocity = 0
		self.x_velocity = 0
		self.score = 0
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.high = 0
		self.hearts = 5
		self.coins = read_data('data.json')['coins']

	def draw(self, screen):
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		if self.x_velocity < 0: # Draw a reversed image if facing to the left
			screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
		else:
			screen.blit(self.img, (self.x, self.y))

	def update_physics(self, screen):
		self.y_velocity += 1.2

		self.score = (700 - self.y) // 275 # Calculate current score based on y_pos
		if self.score > self.high:
			self.high = self.score

		self.hearts = 5 - int(self.high - self.score)

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

		for coin in Coin.coins:
			if self.rect.colliderect(coin.rect):
				self.coins += 1
				Coin.coins.remove(coin)

		data = read_data('data.json')
		data['coins'] = self.coins
		dump_data('data.json', data)

		if self.score == len(Platform.platforms) - 2: # Add more platforms when close to top of current platforms
			Platform.add_plats(15, screen)

		if self.x_velocity > 0: # Check within screen bounds
			if self.x + self.rect.width < screen.get_width():
				self.x += self.x_velocity
		elif self.x_velocity < 0:
			if self.x > 0:
				self.x += self.x_velocity
		
		self.y += self.y_velocity
		
	def jump(self): # Jump if touching grounds
		if self.y_velocity == 0:
			self.y_velocity = -self.jump_velocity
			self.y += self.y_velocity
			self.y_velocity += 1.2
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

	def draw_hearts(self, screen):
		heart_width = Player.heart_img.get_width() + 3
		for i in range(0, self.hearts):
			screen.blit(Player.heart_img, (
				screen.get_width() - (5 * heart_width) + i * heart_width,
				5
			))