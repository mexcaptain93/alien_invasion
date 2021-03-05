import pygame

class Ship():
	"""Класс для управления кораблём"""

	def __init__(self, ai_game):
		"""Инициализирует корабль и задает его начальную позицию"""

		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		# Загружает изображение корабля и получает прямоугольник
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		self.rect.midbottom = self.screen_rect.midbottom

		self.x = float(self.rect.x)

		# Флаги
		self.moving_right = False
		self.moving_left = False


	def update(self):
		"""Обновляет позицию корабля с учетом флага"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed

		if self.moving_left and self.rect.left > 1:
			self.x -= self.settings.ship_speed


		self.rect.x = self.x

	def blitme(self):
		"""Рисует корабль в текущей позиции"""
		self.screen.blit(self.image, self.rect)


class Pers():
	"""Тестовый класс"""

	def __init__(self, ai_game):
		"""Инициализирует тестового перса"""

		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		self.rect = pygame.Rect(150, 150, 150, 150)
		self.color = (52, 152, 219)


		self.rect.center= self.screen_rect.center

	def blitme(self):
		pygame.draw.rect(self.screen, self.color, self.rect)






















