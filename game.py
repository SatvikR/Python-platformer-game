import pygame
from pygame.locals import *
import sys
import random
import json
from Game import (
	Coin,
	Player, 
	Platform, 
	Camera, 
	Button,
	dump_data, 
	read_data
)

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


def main_menu(): #  Starting Menu
	shop_button = Button(
		pygame.Rect((100, 500), (200, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Shop",
		(0, 0, 0),
		message_font
	)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_loop()
			elif event.type == MOUSEBUTTONDOWN:
				if shop_button.check_pos():
					shop()

		screen.fill((47, 47, 47))

		highscore = read_data('data.json')['high']
		high_player = read_data('data.json')['name']
		coin_count = read_data('data.json')['coins']

		title = title_font.render("Spicy Meatballs!", True, (255, 255, 255))
		startinstructions = title_font.render("Press SPACE to play!", True, (255, 255, 255))
		highscore_title = highscore_font.render("Highscore: ", True, (255, 255, 255))
		coins = highscore_font.render(f"Coins: {coin_count}", True, (255, 255, 255))
		highscore = highscore_font.render(f"{int(highscore)}", True, (255, 255, 255))
		name = highscore_font.render(high_player, True, (255, 255, 255))

		screen.blit(title, (width / 2 - title.get_width() / 2, 100))
		screen.blit(startinstructions, (width / 2 - startinstructions.get_width() / 2, height - 75))
		screen.blit(pygame.transform.scale(
			player_img, 
			(player_img.get_width() * 3, player_img.get_height() * 3)), 
			(width / 1.5 + 100, 300))

		shop_button.change_color()

		pygame.draw.rect(screen, (25, 25, 25), pygame.Rect((75, 275), (400, 100)))
		pygame.draw.line(screen, (255, 255, 255), (225, 300), (225, 340), 5)
		screen.blit(highscore, (100, 300))
		screen.blit(highscore_title,  (100, 225))
		screen.blit(name, (300, 300))
		screen.blit(coins, (100, 425))
		shop_button.draw(screen)
		shop_button.draw_text(screen)

		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)

def enter_score(): # Prompt that appears when a player gets a highscore
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
					data = read_data('data.json')
					data['name'] = text.upper()
					dump_data('data.json', data)
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

def game_loop(): # Main game loop
	player = Player(player_img, Player.start_x, Player.start_y)

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

		if player.hearts <= 0:
			highscores = read_data('data.json')
			if highscores['high'] < player.high:
				highscores['high'] = player.high
				dump_data('data.json', highscores)
				enter_score()

			main_menu()

		coins = read_data('data.json')['coins']

		# DRAW
		screen.fill((47, 47, 47))

		Coin.draw_all(screen)

		camera.draw_and_scroll(player, screen)

		# x_vel = stat_font.render("PLAYER_X_VEL: " + str(player.x_velocity), True, (255, 255, 255))
		# y_vel = stat_font.render("PLAYER_Y_VEL: " + str(int(player.y_velocity)), True, (255, 255, 255))
		score = score_font.render(f"SCORE: {str(player.high)}", True, (255, 255, 255))
		coins = score_font.render(f"COINS: {coins}", True, (255,255, 255))

		player.draw_hearts(screen)
		screen.blit(score, (10, 5))
		screen.blit(coins, (width - coins.get_width() - 155, 5))

		pygame.display.flip()
		fpsClock.tick(fps)
	pygame.quit()
	sys.exit(0)

def pause(): # Pause Menu
	menu_button = Button(pygame.Rect((width * 0.3 + 75, height * 0.3 + 100), ((width * 0.4 - 150, 50))), 
		(255, 255, 255), 
		(168, 226, 255), 
		"Main Menu",
		(0, 0, 0),
		message_font
	)

	resume_button = Button(pygame.Rect((width * 0.3 + 75, height * 0.3 + 200), (width * 0.4 - 150, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Resume",
		(0, 0, 0),
		message_font
	)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == MOUSEBUTTONDOWN:
				if menu_button.check_pos():
					main_menu()
				elif resume_button.check_pos():
					return

		menu_button.change_color()
		resume_button.change_color()

		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((width * 0.3, height * 0.3), (width * 0.4, height * 0.4)))
		menu_button.draw(screen)
		resume_button.draw(screen)

		message = message_font.render("Paused...", True, (255, 255, 255))

		screen.blit(message, (width / 2 - message.get_width() / 2,  height * 0.3 + 25))
		menu_button.draw_text(screen)
		resume_button.draw_text(screen)

		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)

def shop():
	menu_button = Button(
		pygame.Rect((width / 2 - 100, 600), (200, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Main Menu",
		(0, 0, 0),
		message_font
	)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == MOUSEBUTTONDOWN:
				if menu_button.check_pos():
					main_menu()

		screen.fill((47, 47, 47))

		menu_button.change_color()
		message = title_font.render("Coming Soon...", True, (255, 255, 255))

		screen.blit(message, (width / 2 - message.get_width() / 2, height / 2 - message.get_height() / 2))
		menu_button.draw(screen)
		menu_button.draw_text(screen)

		pygame.display.flip()
		fpsClock.tick(fps)
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main_menu()
