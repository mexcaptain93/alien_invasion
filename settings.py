import pygame

class Settings():

	def __init__(self):
		self.screen_width = 0
		self.screen_height = 0
		self.fullscreen = pygame.FULLSCREEN
		self.bg_color = (230, 230, 230) 

		self.ship_speed = 1.5

		self.bullet_speed = 1
		self.bullet_width = 3 
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 4