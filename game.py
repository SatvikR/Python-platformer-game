import pygame
from pygame.locals import *
import sys

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("./assets/images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("The holy rectangle")
player_img = pygame.image.load("./assets/images/player.png")
ground_img = pygame.image.load("./assets/images/ground.png")
platform_one = pygame.image.load("./assets/images/platform_1.png")
platform_two = pygame.image.load("./assets/images/platform_2.png")
platform_three = pygame.image.load("./assets/images/platform_3.png")
coin_img = pygame.image.load("./assets/images/coin.png")
stat_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 24)
score_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 40)

class Player():
	walk_speed = 8
	start_x = 100
	start_y = 200
	jump_velocity = 27.5 # Increase this value to jump higher
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.y_velocity = 0
		self.x_velocity = 0
		self.score = 0
		self.rect = self.img.get_rect(topleft=(self.x, self.y))

	def draw(self, screen):
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		if self.x_velocity < 0:
			screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
		else:
			screen.blit(self.img, (self.x, self.y))

	def update_physics(self, platform_list, coin_list):
		self.y_velocity += 1.2

		for platform in platform_list:
			if self.rect.colliderect(platform.rect):
				if self.y_velocity > 0 and platform.y + platform.rect.height * 0.2 > self.y + self.rect.height * 0.8:
					self.y = platform.y - self.rect.height
					self.y_velocity = 0
				elif self.y_velocity < 0:
					self.y_velocity = 1.2
				elif self.x_velocity > 0 and platform.rect.x > self.x:
					self.x_velocity = 0
				elif self.x_velocity < 0 and platform.rect.x < self.x:
					self.x_velocity = 0

		for coin in coin_list:
			if self.rect.colliderect(coin.rect):
				self.score += 1
				coin_list.remove(coin) 

		if self.y + self.img.get_height() >= height + 1000: # increasing this number will increase the delay on falling off the map
			self.x = self.start_x
			self.y = self.start_y
			self.y_velocity = 0 

		if self.y_velocity < 0 and self.y <= 0:
			self.y_velocity = 1.2

		if self.x_velocity > 0:
			if self.x < width:
				self.x += self.x_velocity
		elif self.x_velocity < 0:
			if self.x > 0:
				self.x += self.x_velocity
		
		self.y += self.y_velocity
		
	def jump(self):
		if self.y_velocity == 0:
			self.y_velocity = -self.jump_velocity

class Platform(): #Platform + former = platformer
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.rect = self.img.get_rect(topleft=(self.x, self.y))

	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))

	@staticmethod
	def draw_all(platform_list, screen):
		for platform in platform_list:
			platform.draw(screen)


class Coin():
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.y_velocity = -10
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		
	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))

	@staticmethod
	def draw_all(coin_list, screen):
		for coin in coin_list:
			coin.draw(screen)


def game_loop():
	player = Player(player_img, Player.start_x, Player.start_y)
	platforms = []
	coins = []

	platforms.append(Platform(60, 700, ground_img))
	platforms.append(Platform(800, 600, platform_one))
	platforms.append(Platform(200, 400, platform_two))
	platforms.append(Platform(900, 250, platform_three))
	
	coins.append(Coin(coin_img, 300, 325))
	coins.append(Coin(coin_img, 1000, 175))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:	
				pygame.quit()
				sys.exit()

		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			player.x_velocity = -player.walk_speed
		if key[pygame.K_d]:
			player.x_velocity = player.walk_speed
		if not key[pygame.K_d] and not key[pygame.K_a]:
			player.x_velocity = 0
		if key[pygame.K_F4] and key[pygame.K_LALT]:
			pygame.quit()
			sys.exit()
			
		if key[pygame.K_SPACE]:
			player.jump()
		# UPDATE
		player.update_physics(platforms, coins)

		# DRAW
		screen.fill((47, 47, 47))

		player.draw(screen)
		Coin.draw_all(coins, screen)

		Platform.draw_all(platforms, screen)

		x_vel = stat_font.render("PLAYER_X_VEL: " + str(player.x_velocity), True, (255, 255, 255))
		y_vel = stat_font.render("PLAYER_Y_VEL: " + str(int(player.y_velocity)), True, (255, 255, 255))
		score = score_font.render("SCORE: " + str(player.score), True, (255, 255, 255))

		screen.blit(x_vel, (800, 5))
		screen.blit(y_vel, (1010, 5))
		screen.blit(score, (10, 5))

		pygame.display.flip()
		fpsClock.tick(fps)

if __name__ == "__main__":
	game_loop()
