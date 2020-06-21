import pygame
from .Coin import Coin
from .Platform import Platform
from .Enemy import Enemy
from .Meatball import Meatball
from .Bullet import Bullet

class Camera:
	def draw_and_scroll(self, player, screen):
		"""
		Calcultes difference between current and initial positon
		and draws everything accordingly
		"""
		offset = player.start_y - player.y
		player.rect = player.img.get_rect(topleft=(player.x, player.y))
		if player.direction == 'l':
			screen.blit(pygame.transform.flip(player.img, True, False), (player.x, player.y + offset))
			screen.blit(
				pygame.transform.flip(player.gun_img, True, False), 
				(player.x - player.gun_img.get_width(), player.y + player.img.get_height() / 2 + offset)
			)
		else:
			screen.blit(player.img, (player.x, player.y + offset))
			screen.blit(player.gun_img, (player.x + player.img.get_width(), player.y + player.img.get_height() / 2 + offset))

		[plat.draw(screen, offset) for plat in Platform.platforms]
		
		for enemy in Enemy.enemies:
			enemy.update()
			enemy.draw(screen, offset)

		for meatball in Meatball.meatballs:
			meatball.update()
			meatball.draw(screen, offset)

		for bullet in Bullet.bullets:
			bullet.update(screen)
			bullet.draw(screen, offset)

		for coin in Coin.coins:
			screen.blit(coin.img, (coin.x, coin.y + offset))