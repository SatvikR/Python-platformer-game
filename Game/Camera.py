import pygame
from .Coin import Coin
from .Platform import Platform
from .Enemy import Enemy
from .Meatball import Meatball
from .Bullet import Bullet

class Camera:
	offset = 500

	def draw_and_scroll(self, player, screen):
		"""
		Calcultes difference between current and initial positon
		and draws everything accordingly
		"""
		self.offset += (player.rect.y - self.offset - (screen.get_height() / 2 + player.rect.height / 2)) / 15
		reversed_offset = -1 * self.offset
		
		player.rect = player.img.get_rect(topleft=(player.x, player.y))
		if player.direction == 'l':
			screen.blit(pygame.transform.flip(player.img, True, False), (player.x, player.y + reversed_offset))
			screen.blit(
				pygame.transform.flip(player.gun_img, True, False), 
				(player.x - player.gun_img.get_width(), player.y + player.img.get_height() / 2 + reversed_offset)
			)
		else:
			screen.blit(player.img, (player.x, player.y + reversed_offset))
			screen.blit(player.gun_img, (player.x + player.img.get_width(), player.y + player.img.get_height() / 2 + reversed_offset))

		[plat.draw(screen, reversed_offset) for plat in Platform.platforms]

		[coin.draw(screen, reversed_offset) for coin in Coin.coins]
		
		for enemy in Enemy.enemies:
			enemy.update()
			enemy.draw(screen, reversed_offset)

		for meatball in Meatball.meatballs:
			meatball.update()
			meatball.draw(screen, reversed_offset)

		for bullet in Bullet.bullets:
			bullet.update(screen)
			bullet.draw(screen, reversed_offset)
