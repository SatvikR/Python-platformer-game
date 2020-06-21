from math import sin, cos, atan, degrees, radians, tan

class Meatball:
	meatballs = []
	speed = 7.5

	def __init__(self, player_pos, enemy_pos, img):
		enemy_x, enemy_y = enemy_pos
		player_x, player_y = player_pos
		try:
			self.angle = degrees(atan((enemy_y - player_y) / (enemy_x - player_x)))
			print(f"Slope: {tan(radians(self.angle))}")
		except ZeroDivisionError:
			self.angle = 90 if player_y > enemy_y else 180
		print(f"Spawned meatball with: x_vel: {int(self.speed * cos(radians(self.angle)))}, y_vel: {int(self.speed * sin(radians(self.angle)))}")
		print(f"Angle = {self.angle}")
		self.x, self.y = enemy_x, enemy_y
		self.img = img
		self.rect = img.get_rect(topleft=(self.x, self.y))
		Meatball.meatballs.append(self)
	
	def update(self):
		self.x += int(self.speed * cos(radians(self.angle)))
		self.y += int(self.speed * sin(radians(self.angle)))
		self.rect = self.img.get_rect(topleft=(self.x, self.y))
		

	def draw(self, screen, offset):
		screen.blit(self.img, (self.x, self.y + offset))
		# temporary
		if self.x >= 1200 or self.x <= 0:
			self.meatballs.remove(self)
	