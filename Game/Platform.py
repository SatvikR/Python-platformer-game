import random
import pygame

class Platform: #Platform + former = platformer
	platforms = []
	platform_img = pygame.image.load("./assets/images/platform_2.png")
	ground_img = pygame.image.load("./assets/images/ground.png")

	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		self.platforms.append(self)
		self.moving = bool(random.randint(0, 1))
		self.x_vel = random.randint(2,6)

	def draw(self, screen, offset): # Offset is the players offset (this is called in the draw_and_scroll function)
		self.update(screen)
		screen.blit(self.img, (self.x, self.y + offset))

	def update(self, screen):
		if self.moving:
			if self.x + self.rect.width > screen.get_width() or self.x < 0: # Reverse direction if hitting the edge
				self.x_vel *= -1
			self.x += self.x_vel
			self.rect = self.img.get_rect(topleft=(self.x, self.y))

	@staticmethod
	def add_plats(amount, screen): # Adds 15 new platforms at random x positions
		base_y = 700
		max_x = screen.get_width() - Platform.platform_img.get_width()
		for i in range(len(Platform.platforms), len(Platform.platforms) + amount):
			print(i, len(Platform.platforms) + 0 + amount)
			random.seed()
			Platform(random.randint(0, max_x), (base_y) - i * 275, Platform.platform_img)


	@staticmethod
	def create_plates(amount, screen): # Initial creation of platforms incuding ground platform
		Platform.platforms.clear()
		Platform(60, 700, Platform.ground_img)
		max_x = screen.get_width() - Platform.platform_img.get_width()
		base_y = 700
		for i in range(1, amount + 1):
			random.seed()
			Platform(random.randint(0, max_x), (base_y) - i * 275, Platform.platform_img)