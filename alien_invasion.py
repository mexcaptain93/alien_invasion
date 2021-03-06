import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion():
	"""Класс для управления ресурсами и поведением игры"""

	def __init__(self):
		"""Init game and game's resources"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), self.settings.fullscreen)
		self.bg_color = self.settings.bg_color
		pygame.display.set_caption("Alien Invasion")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)


		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()
		self.play_button = Button(self, "Play")

	def _check_events(self):
		"""Обрабатывает нажатия клавиатуры и события мыши"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.stats.set_record_to_file(self.stats.high_score)
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_keydown_events(self, event):
		"""Реагирует на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		if event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		if event.key == pygame.K_q:
			self.stats.set_record_to_file(self.stats.high_score)
			sys.exit()
		if event.key == pygame.K_SPACE:
			self._fire_bullet()
		if event.key == pygame.K_p:
			self.start_game()

	def _check_keyup_events(self, event):
		"""Реагирует на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		if event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _check_play_button(self, mouse_pos):
		"""Запускает игру при нажатии на Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)

		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			self.start_game()
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

	def start_game(self):
		self.stats.reset_stats()
		self.stats.game_active = True

		self.aliens.empty()
		self.bullets.empty()

		self._create_fleet()
		self.ship.center_ship()

		pygame.mouse.set_visible(False)

	def _fire_bullet(self):
		"""Создание нового снаряда"""
		if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Обновление позиции снарядов и удаление старых"""
		self.bullets.update()

		#Удаление снарядов
		for bullet in self.bullets:
			if bullet.rect.y <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		# Проверка попадания в пришельцев
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.stats.score += self.settings.alien_points
			self.sb.prep_score()
			self.sb.check_high_score()
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level += 1
			self.sb.prep_level()

	def _create_fleet(self):
		"""Создание флота"""
		alien = Alien(self)
		self.aliens.add(alien)
		alien_width, alien_height = alien.rect.size

		ship_height = self.ship.rect.height
		available_space_x = pygame.display.Info().current_w - (alien_width * 2)
		available_space_y = pygame.display.Info().current_h - ship_height - (alien_height * 3)
		number_aliens_x = available_space_x // (alien_width * 2)
		number_aliens_y = available_space_y // (alien_height * 2)

		for row_number in range(number_aliens_y):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _update_aliens(self):
		"""Обновляет позиции всех пришельцев"""
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		self._check_aliens_bottom()

	def _create_alien(self, alien_number, row_number):
		"""Создание пришельца"""
		alien = Alien(self)
		# alien_width, alien_height = alien.rect.size

		alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
		alien.rect.x = alien.x
		alien.y = alien.rect.height + 2 * alien.rect.height * row_number
		alien.rect.y = alien.y
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Реагирует на достижение пришельцем края"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _check_aliens_bottom(self):
		"""Проверяет, достигли ли пришельцы нижнего края экрана"""
		screen_rect = self.screen.get_rect()

		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

	def _change_fleet_direction(self):
		"""Опускает весь флот и меняет его направление"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Обрабатывает столкновение с кораблём"""
		if self.stats.ship_left > 0:
			self.stats.ship_left -= 1
			self.sb.prep_ships()

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()

			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _update_screen(self):
		"""Перерисовывает экран"""
		self.screen.fill(self.bg_color)
		self.ship.blitme()

		for bullet in self.bullets:
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		self.sb.show_score()

		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()

	def run_game(self):
		"""Запуск основного цикла игры"""
		while True:
			
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._check_fleet_edges()
				self._update_aliens()

			self._update_screen()


if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()