import pygame

class Settings():

	def __init__(self):
		self.screen_width = 0
		self.screen_height = 0
		self.fullscreen = pygame.FULLSCREEN
		self.bg_color = (230, 230, 230)
		self.record_file = 'record.txt'

		self.ship_speed = 3.5
		self.ship_limit = 3

		# Настройки снарядов
		self.bullet_speed = 10.5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 10

		# Настройки пришельцев
		self.alien_speed = 3
		self.fleet_drop_speed = 15
		self.fleet_direction = 1

		# Темп ускорения игры
		self.speedup_scale = 1.1
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, изменяющиеся в ходе игры"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		"""Увеличивает настройки скорости"""
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.ship_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)