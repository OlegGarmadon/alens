import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
	"""Класс для управления ресурсами и поведением игры"""

	def __init__(self):
		"""Инициирует игру и создает игровые ресурсы"""
		pygame.init()

		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_heignt))
		pygame.display.set_caption("Alien Invasion")
		
		# Создание экземпляляра для хранение игровой статистики.
		self.stats = GameStats
		
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		
		self._create_fleet()
		
		#Назначение цвета фона а
		self.bg_color = (230, 230, 230)

	def run_game(self):
		"""Запуск основного цикла игры"""
		while True:
			self._check_events()			
			self.ship.update()
			self._update_bullets()
			self._update_aliens()
			self._update_screen()
			# При каждом проходе цикла перерисовываеться экран.
 
	def _check_events(self):			
		"""обрабатывает событий клавиатуры и мыши"""
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		""" Реагирует на нажатие клавиш"""

		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		# Выход из игры с помощью клавиши "Q"
		elif event.key == pygame.K_q:
			sys.exet()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		""" Реагирует на нажатие клавиш"""
		
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
			#Переместить корабль в право.
			self.ship.rect.x += 1

	def _fire_bullet(self):
		"""Создание нового снаряда и включение его в группу bullets"""
		
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
			""" Обновляеться позиция и уничтожаються старые снаряды"""			
			
			# Обновление позиции снаряда.
			self.bullets.update()			
			# Удаление снарядов, вышедших за край экрана.
			for bullet in self.bullets.copy():
				if bullet.rect.bottom <= 0:
					self.bullets.remove(bullet)
			self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
			"""Обработка коллизии снарядов"""
			# Удаление снарядов и пришелбцев, учавствующих в коллизии
			collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
			if not self.aliens:
				# Уничтожение существующих снарядов и зоздание нового флота
				self.bullets.empty()
				self._create_fleet()



	def _update_aliens(self):
		"""Обновляет все позиции пришельцеф во флоте"""
		self._check_fleet_edges()
		self.aliens.update()
		
		# Проверка коллизии пришелец коsрабль
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		def _ship_hit(self):
				"""Обрабатывает столкновение коробля с пришельцем."""
				# Уменьшение ship_left.
				self.stats.ships_left -= 1

				# Очистка списков пришельцев и снарядов.
				self.aliens.empty()
				self.bullets.empty()

				# Создание нового флота и размещение коробля в центре.
				self.create_fleet()
				self.ship.centr_ship()

				# Пауза
				sleep(0.5)
			

	def _create_fleet(self):
		"""Создание флота пришельцев"""
		
		# Создание пришельца и вычисление колличества пришельцев в ряду.
		# Интервал между соседними пришельцами равен ширине пришельца.		
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien_width = alien.rect.width
		available_spase_x = self.settings.screen_width - (2 * alien_width)
		number_alins_x = available_spase_x // (2 * alien_width)

		""" Определяет колличество рядов, помещающихся на экране"""
		ship_height = self.ship.rect.height
		available_spase_y = (self.settings.screen_heignt - (3 * alien_height) - ship_height)
		namber_rows = available_spase_y // (2 * alien_height)


		# Создание флота вторжения
		for row_number in range(namber_rows):
			for alien_number in range(number_alins_x):
				self._creat_alien(alien_number, row_number)

	def _creat_alien(self, alien_number, row_number):
		"""Создает пришельца и размещает его в ряду."""

		alien = Alien(self)
		alien_width = alien.rect.width
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width *alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Реагирует на достижение пришельцем края экрана."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Опускаем весь флот и меняем направление флота."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		"""Обновляет изображения на экране и отображает новый экран"""
		
		self.screen.fill(self.settings.bg_color)
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()		
		self.ship.blitme()
		self.aliens.draw(self.screen)			

		pygame.display.flip()

if __name__ == '__main__':
	#Создание экземпляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()
