import sys
import pygame

from settings import Settings
from ship import Ship, Pers
from bullet import Bullet

class AlienInvasion():
	"""Класс для управления ресурсами и поведением игры"""

	def __init__(self):
		"""Init game and game's resources"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), self.settings.fullscreen)
		self.bg_color = self.settings.bg_color
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		# self.test_pers = Pers(self)

	def _check_events(self):
		"""Обрабатывает нажатия клавиатуры и события мыши"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
				
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)				

	def _check_keydown_events(self, event):
		"""Реагирует на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		if event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		if event.key == pygame.K_q:
			sys.exit()
		if event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Реагирует на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		if event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Создание нового снаряда"""

		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Обновление позиции снарядов и удаление старых"""
		self.bullets.update()

		#Удаление снарядов
		for bullet in self.bullets:
			if bullet.rect.y <= 0:
				self.bullets.remove(bullet)

	def _update_screen(self):
		"""Перерисовывает экран"""
		self.screen.fill(self.bg_color)
		self.ship.blitme()
		# self.test_pers.blitme()

		for bullet in self.bullets:
			bullet.draw_bullet()

		pygame.display.flip()


	def run_game(self):
		"""Запуск основного цикла игры"""
		while True:
			
			self._check_events()
			self.ship.update()
			self._update_bullets()

			self._update_screen()


			

if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()