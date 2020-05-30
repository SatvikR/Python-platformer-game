import pygame
from pygame.locals import *
import sys

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
player_img = pygame.image.load("./assets/player.png")
ground_img = pygame.image.load("./assets/ground.png")

class Player():
	x_vel = 5
	def __init__(self, img, x, y):
		self.img = img
		self.x = x
		self.y = y
		self.move_y = 0
		self.rect = self.img.get_rect()
		print(self.y, self.rect.y)

	def draw(self, screen):
		self.rect = self.img.get_rect() 
		screen.blit(self.img, (self.x, self.y))

	def update_grav(self, platform_list):
		self.move_y += 1.2

		for platform in platform_list:
			if self.rect.colliderect(platform.rect):
				if self.move_y > 0:
					self.y = platform.y - self.img.get_height()
					self.move_y = 0
		if self.y + self.img.get_height() >= height:
			self.y = height / 2
			self.move_y = 0 
		self.y += self.move_y

class Platform(): #Platform + former = platformer
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.rect = self.img.get_rect()

	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))

	@staticmethod
	def draw_all(platform_list, screen):
		for platform in platform_list:
			platform.draw(screen)


def game_loop():
	player = Player(player_img, 100, height / 2)
	platforms = []
	platforms.append(Platform(50, 700, ground_img))


	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			if player.x >= 0:
				player.x -= player.x_vel
		if key[pygame.K_d]:
			if player.x <= width:
				player.x += player.x_vel

		# UPDATE
		player.update_grav(platforms)

		# DRAW
		screen.fill((47, 47, 47))

		player.draw(screen)

		Platform.draw_all(platforms, screen)


		pygame.display.flip()
		fpsClock.tick(fps)

if __name__ == "__main__":
	game_loop()