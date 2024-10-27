class Settings():
	""" Класс для хранения всех настроек игры Alien Settings"""

	def __init__(self):
		# Инициализирует настройки игры.
		
		# Параметры экрана
		self.screen_width = 1200
		self.screen_heignt = 800
		self.bg_color = (230, 230, 230)
		
		# Настройки коробля.
		self.ship_speed = 1.5
		self.ship_limit = 3

		# Параметы снарядаchange_fleet_direction
		self.bullet_speed = 2.5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3

		# Настройки пришельцев
		self.alien_speed = 0.2
		self.fleet_drop_speed = 10 
		# flet_direction = 1 обозночань движение вправо; а -1 влево.
		self.fleet_direction = 1


