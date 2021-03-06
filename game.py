import pygame
import sys
from Game import (
	Player, 
	Platform,
	Coin,
	Meatball, 
	Camera, 
	Button,
	Upgrades,
	Enemy,
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
coin_img = pygame.image.load("./assets/images/coin.png")
jump_upgrade_img = pygame.image.load("./assets/images/jump_upgrade.png")
coin_upgrade_img = pygame.image.load("./assets/images/coin_upgrade.png")
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
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_loop()
			elif event.type == pygame.MOUSEBUTTONDOWN:
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
		screen.blit(pygame.transform.scale( # Player Model
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
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					text = text[:-1] # Slices off last letter
				elif event.key == pygame.K_RETURN:
					data = read_data('data.json')
					data['name'] = text.upper()
					dump_data('data.json', data)
					main_menu()
				else:
					if len(text) < 6:
						text += event.unicode


		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((width * 0.3, height * 0.3), (width * 0.4, height * 0.4)))
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((width * 0.3 + 15, height * 0.3 + 80), (width * 0.4 - 30, height * 0.4 - 170)))
		pygame.draw.rect(screen, (47, 47, 47), pygame.Rect((width - 170, 0), (200, 35)))

		message = message_font.render("Congrats, you got a highscore!", True, (255, 255, 255))
		prompt = message_font.render("Enter Your Name:", True, (255, 255, 255))
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
	Enemy.target_player = player

	# Clear all existing entities
	Platform.platforms.clear()
	Meatball.meatballs.clear()
	Coin.coins.clear()
	Enemy.enemies.clear()

	Upgrades.update_upgrades('data.json')

	Platform.create_plates(15, screen)

	camera = Camera()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	
				running = False				
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					player.spawn_bullet()
			
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

		camera.draw_and_scroll(player, screen)

		score = score_font.render(f"SCORE: {str(player.high)}", True, (255, 255, 255))
		coins = score_font.render(f"COINS: {coins}", True, (255,255, 255))

		player.draw_hearts(screen)
		screen.blit(score, (10, 5))
		screen.blit(coins, (width - coins.get_width() - 200, 5))

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
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

def shop(): # Menu from which player can buy upgrades

	# Shop Button Width Margins: 100px on either side, 200 px between buttons, button_width=200px

	menu_button = Button(
		pygame.Rect((width / 2 - 100, 700), (200, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Main Menu",
		(0, 0, 0),
		message_font
	)

	jump_button = Button(
		pygame.Rect((100, 300), (200, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Higher Jump",
		(0, 0, 0),
		message_font
	)

	coin_button = Button(
		pygame.Rect((500, 300), (200, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Multi-Coin",
		(0, 0, 0),
		message_font
	)


	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Check each upgrade button and do the according action
				if menu_button.check_pos():
					main_menu()
				elif jump_button.check_pos():
					data = read_data('data.json')
					if not data["jump_upgrade"]["active"]: # Add ten to jump_vel
						if data["coins"] >= data["jump_upgrade"]["price"]:
							data['coins'] -= data["jump_upgrade"]["price"]
							data['jump_vel'] += 10
							data["jump_upgrade"]["active"] = True
							dump_data('data.json', data)
							upgrade_prompt("jump_upgrade")
						else:
							empty_prompt("Not Enough Money!")
					else:
						empty_prompt("Upgrade in Use")
				elif coin_button.check_pos():
					data = read_data('data.json')
					if not data["coin_upgrade"]["active"]: # Doubles coin multiplier
						if data["coins"] >= data["coin_upgrade"]["price"]:
							data["coins"] -= data["coin_upgrade"]["price"]
							data["coin_multiplier"] = 2
							data["coin_upgrade"]["active"] = True
							dump_data('data.json', data)
							upgrade_prompt("coin_upgrade")
						else:
							empty_prompt("Not Enough Money!")
					else:
						empty_prompt("Upgrade in Use")

		screen.fill((47, 47, 47))

		coins = score_font.render(f"COINS: {read_data('data.json')['coins']}", True, (255,255, 255))
		screen.blit(coins, (width - 250, 15))

		menu_button.change_color()
		jump_button.change_color()
		coin_button.change_color()

		menu_button.draw(screen)
		menu_button.draw_text(screen)

		jump_button.draw(screen)
		jump_button.draw_text(screen)

		coin_button.draw(screen)
		coin_button.draw_text(screen)

		screen.blit(jump_upgrade_img, (jump_button.rect.x - 25, jump_button.rect.y - 15 - jump_upgrade_img.get_height()))
		screen.blit(coin_upgrade_img, (coin_button.rect.x - 25, coin_button.rect.y - 15 - coin_upgrade_img.get_height()))

		pygame.display.flip()
		fpsClock.tick(fps)
	pygame.quit()
	sys.exit(0)

def upgrade_prompt(upgrade_name): # Prompt when upgrade is purchased
	back_button = Button(pygame.Rect((width * 0.3 + 75, height * 0.3 + 225), (width * 0.4 - 150, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Back",
		(0, 0, 0),
		message_font
	)
	
	upgrade_duration = read_data('data.json')[upgrade_name]["duration"]

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if back_button.check_pos():
					return

		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((width * 0.3, height * 0.3), (width * 0.4, height * 0.4)))


		prompt_one = score_font.render("You Purchased: ", True, (255, 255, 255))
		prompt_two = score_font.render(upgrade_name, True, (255, 255, 255))
		prompt_three = score_font.render("Your upgrade lasts for ", True, (255, 255, 255))
		prompt_four = score_font.render(f"{upgrade_duration} Games", True, (255, 255, 255))

		screen.blit(prompt_one, (width / 2 - prompt_one.get_width() / 2, height * 0.3 + 5))
		screen.blit(prompt_two, (width / 2 - prompt_two.get_width() / 2, height * 0.3 + 45))
		screen.blit(prompt_three, (width / 2 - prompt_three.get_width() / 2, height * 0.3 + 85))
		screen.blit(prompt_four, (width / 2 - prompt_four.get_width() / 2, height * 0.3 + 125))

		back_button.change_color()
		back_button.draw(screen)
		back_button.draw_text(screen)

		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)

def empty_prompt(text): # Generic prompt with text and back button
	back_button = Button(pygame.Rect((width * 0.3 + 75, height * 0.3 + 225), (width * 0.4 - 150, 50)),
		(255, 255, 255),
		(168, 226, 255),
		"Back",
		(0, 0, 0),
		message_font
	)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if back_button.check_pos():
					return

		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((width * 0.3, height * 0.3), (width * 0.4, height * 0.4)))

		prompt = score_font.render(text, True, (255, 255, 255))

		screen.blit(prompt, (width / 2 - prompt.get_width() / 2, height / 2 - prompt.get_height() / 2 - 75))

		back_button.change_color()
		back_button.draw(screen)
		back_button.draw_text(screen)

		pygame.display.flip()
		fpsClock.tick(fps)

	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main_menu()
