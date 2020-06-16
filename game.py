import pygame
from pygame.locals import *
import sys
import random
import json
from Game.Highscores.read_write import dump_data, read_data
from Game.Coin import Coin
from Game.Platform import Platform
from Game.Camera import Camera
from Game.Player import Player

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("./assets/images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("The holy rectangle")
player_img = pygame.image.load("./assets/images/player.png")
platform_one = pygame.image.load("./assets/images/platform_1.png")
platform_three = pygame.image.load("./assets/images/platform_3.png")
coin_img = pygame.image.load("./assets/images/coin.png")
stat_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 24)
score_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 40)
title_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 70)
highscore_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 50)
message_font = pygame.font.Font("./assets/fonts/bitfont.ttf", 35)


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

def game_loop():
	player = Player(player_img, Player.start_x, Player.start_y, main_menu, enter_score)

	Platform.create_plates(15, screen)

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
		player.update_physics(screen)

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
