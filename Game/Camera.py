import pygame
from .Coin import Coin
from .Player import Player
from .Platform import Platform

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