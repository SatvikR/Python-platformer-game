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
heart_img = pygame.image.load("./assets/images/heart.png")
stat_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 24)
score_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 40)
title_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 70)
highscore_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 50)
message_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 35)

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
		self.hearts = 5

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

		if self.score < self.high - 4: # increasing this number will increase the delay on falling off the map
			highscores = read_data('highscore.json')
			if highscores['high'] < self.high:
				highscores['high'] = self.high
				dump_data('highscore.json', highscores)
				enter_score()

			
			main_menu() 

		if self.x_velocity > 0:
			if self.x + self.rect.width < width:
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
		heart_width = heart_img.get_width() + 3
		for i in range(0, self.hearts):
			screen.blit(heart_img, (
				width - (5 * heart_width) + i * heart_width,
				5
			))

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

	camera = Camera()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:	
				running = False				
			elif event.type == KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause()
			
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			player.x_velocity = -player.walk_speed
		if key[pygame.K_d]:
			player.x_velocity = player.walk_speed
		if not key[pygame.K_d] and not key[pygame.K_a]:
			player.x_velocity = 0
		if key[pygame.K_F4] and key[pygame.K_LALT]:
			running = False

		if key[pygame.K_SPACE]:
			player.jump()
		# UPDATE
		player.update_physics()

		# DRAW
		screen.fill((47, 47, 47))

		camera.draw_and_scroll(player, screen)

		x_vel = stat_font.render("PLAYER_X_VEL: " + str(player.x_velocity), True, (255, 255, 255))
		y_vel = stat_font.render("PLAYER_Y_VEL: " + str(int(player.y_velocity)), True, (255, 255, 255))
		score = score_font.render("SCORE: " + str(player.high), True, (255, 255, 255))
		#print(score.get_height())

		#screen.blit(x_vel, (800, 5))
		#screen.blit(y_vel, (1010, 5))
		player.draw_hearts(screen)
		screen.blit(score, (10, 5))

		pygame.display.flip()
		fpsClock.tick(fps)
	pygame.quit()
	sys.exit(0)

def main_menu():
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				
			elif event.type == KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_loop()

		screen.fill((47, 47, 47))

		highscore = read_data('highscore.json')['high']
		high_player = read_data('highscore.json')['name']

		title = title_font.render("Spicy Meatballs!", True, (255, 255, 255))
		startinstructions = title_font.render("Press SPACE to play!", True, (255, 255, 255))
		highscore_title = highscore_font.render("Highscore: ", True, (255, 255, 255))
		highscore = highscore_font.render(str(int(highscore)), True, (255, 255, 255))
		name = highscore_font.render(high_player, True, (255, 255, 255))

		screen.blit(title, (width / 2 - title.get_width() / 2, 100))
		screen.blit(startinstructions, (width / 2 - startinstructions.get_width() / 2, height - 75))
		screen.blit(pygame.transform.scale(
			player_img, 
			(player_img.get_width() * 3, player_img.get_height() * 3)), 
			(width / 1.5 + 100, 300))

		pygame.draw.rect(screen, (25, 25, 25), pygame.Rect((75, 275), (400, 100)))
		pygame.draw.line(screen, (255, 255, 255), (225, 300), (225, 340), 5)
		screen.blit(highscore, (100, 300))
		screen.blit(highscore_title,  (100, 225))
		screen.blit(name, (300, 300))

		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)

def enter_score():
	running = True
	text = ''
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					text = text[:-1]
				elif event.key == pygame.K_RETURN:
					data = read_data('highscore.json')
					data['name'] = text.upper()
					dump_data('highscore.json', data)
					main_menu()
				else:
					if len(text) < 3:
						text += event.unicode


		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((width * 0.3, height * 0.3), (width * 0.4, height * 0.4)))
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((width * 0.3 + 15, height * 0.3 + 80), (width * 0.4 - 30, height * 0.4 - 170)))
		pygame.draw.rect(screen, (47, 47, 47), pygame.Rect((width - 200, 0), (200, 35)))

		message = message_font.render("Congrats, you got a highscore!", True, (255, 255, 255))
		prompt = message_font.render("Enter Your Initials:", True, (255, 255, 255))
		current = highscore_font.render(text.upper(), True, (0, 0, 0))
		enter = message_font.render("Press enter/return to submit", True, (255, 255, 255))

		screen.blit(message, ((width / 2) - (message.get_width() / 2) , height * 0.3 + 10))
		screen.blit(prompt, ((width / 2) - (message.get_width() / 2), height * 0.3 + 40))
		screen.blit(current, (width * 0.3 + 25, height * 0.3 + 95))
		screen.blit(enter, (width * 0.3 + 20, height * 0.7 + - 50))
		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)

def pause():
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN:
				if event.key == pygame.K_RETURN:
					return
			elif event.type == MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				if width * 0.3 + 75 < x < width * 0.7 - 75 and height * 0.3 + 150 < y < height * 0.3 + 200:
					main_menu()

		menu_button = pygame.Rect((width * 0.3 + 75, height * 0.3 + 150), ((width * 0.4 - 150, 50)))
		x, y = pygame.mouse.get_pos()
		if width * 0.3 + 75 < x < width * 0.7 - 75 and height * 0.3 + 150 < y < height * 0.3 + 200:
			button_color = (168, 226, 255)
		else:
			button_color = (255, 255, 255)

		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((width * 0.3, height * 0.3), (width * 0.4, height * 0.4)))
		pygame.draw.rect(screen, button_color, menu_button)

		message = message_font.render("Press Enter/Return to resume...", True, (255, 255, 255))
		prompt = message_font.render("Main Menu", True, (0, 0, 0))

		screen.blit(message, (width / 2 - message.get_width() / 2,  height * 0.3 + 25))
		screen.blit(prompt, (width / 2 - prompt.get_width() / 2, height * 0.3 + 150 + ((50 - prompt.get_height()) / 2)))

		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)


if __name__ == "__main__":
	main_menu()
