import pygame
from pygame.locals import *
import sys
import random
import json

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
title_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 70)

class Player():
	walk_speed = 10
	start_x = 100
	start_y = 500
	jump_velocity = 27.5 # Increase this value to jump higher
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.y_velocity = 0
		self.x_velocity = 0
		self.score = 0
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.death_bar = 0
		self.high = 0

	def draw(self, screen):
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		if self.x_velocity < 0:
			screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
		else:
			screen.blit(self.img, (self.x, self.y))

	def update_physics(self):
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
			Platform.add_plats(15)

		if self.y + self.img.get_height() >= height - self.death_bar: # increasing this number will increase the delay on falling off the map
			highscores = read_data('highscore.json')
			if highscores['high'] < self.high:
				highscores['high'] = self.high

			dump_data('highscore.json', highscores)
			self.x = self.start_x
			self.y = self.start_y
			self.x_velocity = 0
			self.score = 0
			self.y_velocity = 0
			self.high = 0
			main_menu() 

		if self.x_velocity > 0:
			if self.x + self.rect.width < width:
				self.x += self.x_velocity
		elif self.x_velocity < 0:
			if self.x > 0:
				self.x += self.x_velocity
		
		self.y += self.y_velocity
		
	def jump(self):
		if self.y_velocity == 0:
			self.y_velocity = -self.jump_velocity
			self.y += self.y_velocity
			self.y_velocity += 1.2
			self.rect = self.img.get_rect(topleft=(self.x, self.y))


class Camera():
	def draw_and_scroll(self, player, screen):
		offset = player.start_y - player.y
		player.rect = player.img.get_rect(topleft=(player.x, player.y))
		if player.x_velocity < 0:
			screen.blit(pygame.transform.flip(player.img, True, False), (player.x, player.y + offset))
		else:
			screen.blit(player.img, (player.x, player.y + offset))

		[plat.draw(screen, offset) for plat in Platform.platforms]

		for coin in Coin.coins:
			screen.blit(coin.img, (coin.x, coin.y + offset))


class Platform(): #Platform + former = platformer
	platforms = []

	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.platforms.append(self)
		self.moving = bool(random.randint(0, 1))
		self.x_vel = random.randint(2,6)

	def draw(self, screen, offset):
		self.update()
		screen.blit(self.img, (self.x, self.y + offset))

	def update(self):
		if self.moving:
			if self.x + self.rect.width > width or self.x < 0:
				self.x_vel *= -1
			self.x += self.x_vel
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

	@staticmethod
	def add_plats(amount):
		base_y = 700
		max_x = width - platform_two.get_width()
		for i in range(len(Platform.platforms), len(Platform.platforms) + amount):
			print(i, len(Platform.platforms) + 0 + amount)
			random.seed()
			Platform(random.randint(0, max_x), (base_y) - i * 275, platform_two)


	@staticmethod
	def create_plates(amount):
		Platform.platforms.clear()
		Platform(60, 700, ground_img)
		max_x = width - platform_two.get_width()
		base_y = 700
		for i in range(1, amount + 1):
			random.seed()
			Platform(random.randint(0, max_x), (base_y) - i * 275, platform_two)



class Coin():
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

def dump_data(file, data):
	with open(file, 'w') as out:
		json.dump(data, out, indent=4)

def read_data(file):
	with open(file, 'r') as f:
		return json.load(f)



def game_loop():
	player = Player(player_img, Player.start_x, Player.start_y)


	Platform.create_plates(15)

	#Coin(coin_img, 300, 325)
	#Coin(coin_img, 1000, 175)

	camera = Camera()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:	
				pygame.quit()
				exit()

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
		player.update_physics()

		# DRAW
		screen.fill((47, 47, 47))

		camera.draw_and_scroll(player, screen)

		x_vel = stat_font.render("PLAYER_X_VEL: " + str(player.x_velocity), True, (255, 255, 255))
		y_vel = stat_font.render("PLAYER_Y_VEL: " + str(int(player.y_velocity)), True, (255, 255, 255))
		score = score_font.render("SCORE: " + str(player.score), True, (255, 255, 255))

		screen.blit(x_vel, (800, 5))
		screen.blit(y_vel, (1010, 5))
		screen.blit(score, (10, 5))

		pygame.display.flip()
		fpsClock.tick(fps)

def main_menu():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			elif event.type == KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_loop()

		screen.fill((47, 47, 47))
		title = title_font.render("Spicy Meatballs!", True, (255, 255, 255))
		startinstructions = title_font.render("Press SPACE to play!", True, (255, 255, 255))

		screen.blit(title, (width / 2 - title.get_width() / 2, 100))
		screen.blit(startinstructions, (width / 2 - startinstructions.get_width() / 2, height - 75))
		screen.blit(pygame.transform.scale(
			player_img, 
			(player_img.get_width() * 3, player_img.get_height() * 3)), 
			(width / 1.5 + 100, 300))

		pygame.display.flip()
		fpsClock.tick(fps)
if __name__ == "__main__":
	main_menu()