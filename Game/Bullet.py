from math import cos, sin, radians

class Bullet:
	speed = 20
	bullets = []

	def __init__(self, img, x, y, angle):
		self.img = img
		self.rect = self.img.get_rect(topleft=(x, y))
		self.x = x
		self.y = y
		self.angle = angle
		self.bullets.append(self)
	
	def update(self, screen):
		self.x += int(self.speed * cos(radians(self.angle)))
		self.y += int(self.speed * sin(radians(self.angle)))
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		if self.x < 0 or self.x > screen.get_width():
			self.bullets.remove(self)
	
	def draw(self, screen, offset):
		screen.blit(self.img, (self.x, self.y + offset))