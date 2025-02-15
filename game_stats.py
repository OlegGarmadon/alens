class GameStats():
	""" Отслеживание статистики игры Alien Invasion"""

	def __init__(self, ai_game):
		""" Инициализируем статистику"""
		self.settings = ai_game.settings
		self.reset_stats()

	def reset_stats():
		"""Инициализирует статистику, изменяющуюся в ходе игры"""
		self.ships_left = self.settings.ship_limit
