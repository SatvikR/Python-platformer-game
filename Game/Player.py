import pygame
from .Coin import Coin
from .Platform import Platform
from .Highscores.read_write import read_data, dump_data

class Player():
	walk_speed = 10
	start_x = 100
	start_y = 500
	jump_velocity = 27.5 # Increase this value to jump higher
	heart_img = pygame.image.load("./assets/images/heart.png")
	
	def __init__(self, img, x, y, main_menu, enter_score):
		self.img = img
		self.x = x
		self.y = y
		self.y_velocity = 0
		self.x_velocity = 0
		self.score = 0
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.death_bar = 0
		self.high = 0
		self.hearts = 5
		self.main_menu = main_menu
		self.enter_score = enter_score

	def draw(self, screen):
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		if self.x_velocity < 0:
			screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
		else:
			screen.blit(self.img, (self.x, self.y))

	def reset(self):
		self.x = self.start_x
		self.y = self.start_y
		self.x_velocity = 0
		self.score = 0
		self.y_velocity = 0
		self.high = 0
		self.hearts = 5

	def update_physics(self, screen):
		self.y_velocity += 1.2
		self.score = (700 - self.y) // 275
		if self.score > self.high:
			self.high = self.score
		self.death_bar = (self.high - 1) * 250 if self.score < 5 else (self.high - 5) * 250
		for platform in Platform.platforms:
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

		if self.score == len(Platform.platforms) - 2:
			Platform.add_plats(15, screen)

		if self.score < self.high - 4: # increasing this number will increase the delay on falling off the map
			highscores = read_data('highscore.json')
			if highscores['high'] < self.high:
				highscores['high'] = self.high
				dump_data('highscore.json', highscores)
				self.enter_score()

			
			self.main_menu() 

		if self.x_velocity > 0:
			if self.x + self.rect.width < screen.get_width():
				self.x += self.x_velocity
		elif self.x_velocity < 0:
			if self.x > 0:
				self.x += self.x_velocity
		
		self.hearts = 5 - int(self.high - self.score)
		self.y += self.y_velocity
		
	def jump(self):
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