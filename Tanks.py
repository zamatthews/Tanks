#Tanks
#Zach Matthews
#CS 475
import os
import sys
import math
import pygame as pg
from enum import Enum
from random import randint

CAPTION = "Tanks"
SCREEN_SIZE = (700, 700)
BACKGROUND_COLOR = (33, 17, 255)
BORDER_SIZE = 500
FPS_LOCK = 60
GAME_OVER = False

class gun_type(Enum):
	basic = 1
	advanced = 2
	ultra = 3
class Tank(object):
	def __init__(self, location):
		self.turret_start = TURRET
		self.turret = TURRET
		self.tank_start = TANK
		self.tank = TANK
		self.turret_rect = self.turret.get_rect(center = location)
		self.tank_rect = self.tank.get_rect(center = location)
		self.tank_pos = location
		self.turret_angle = 0
		self.tank_angle = 0
		self.turret_direction = 0
		self.tank_spin_direction = 0
		self.tank_move_direction = 0
		self.rotate_speed = 5
		self.turn_speed = 2.5
		self.move_speed = 2.5
		self.bullet_timer = 0
		self.gun_cooldown = 50
		self.gun = gun_type.basic
		
	def spin_turret(self):
		self.turret_angle += self.rotate_speed*self.turret_direction
		self.turret_angle += self.turn_speed*self.tank_spin_direction
		self.turret = pg.transform.rotate(self.turret_start, self.turret_angle)
		self.turret_rect = self.turret.get_rect(center = self.turret_rect.center)
		
	def spin_tank(self):
		self.tank_angle += self.turn_speed*self.tank_spin_direction
		self.tank = pg.transform.rotate(self.tank_start, self.tank_angle)
		self.tank_rect = self.tank.get_rect(center = self.tank_rect.center)
		
	def get_pos(self):
		return self.tank_pos
	def get_rect(self):
		return self.tank_rect
		
	def move_tank(self, island_rect):
		new_x = self.tank_pos[0] + self.move_speed*math.sin(math.radians(self.tank_angle - 90))*self.tank_move_direction
		new_y = self.tank_pos[1] + self.move_speed*math.cos(math.radians(self.tank_angle - 90))*self.tank_move_direction
		
		if new_x > (SCREEN_SIZE[0] + BORDER_SIZE) / 2 or new_x < (SCREEN_SIZE[0] - BORDER_SIZE) / 2:
			new_x = self.tank_pos[0]
		if new_y > (SCREEN_SIZE[1] + BORDER_SIZE) / 2 or new_y < (SCREEN_SIZE[1] - BORDER_SIZE) / 2:
			new_y = self.tank_pos[1]
		self.tank_pos = (new_x, new_y)
		self.turret_rect = self.turret.get_rect(center = self.tank_pos)
		self.tank_rect = self.tank.get_rect(center = self.tank_pos)
		
		
	def key_press(self, keys, bullets):
		if keys[pg.K_a]:
			self.tank_spin_direction = 1
		if keys[pg.K_d]:
			self.tank_spin_direction = -1
		if keys[pg.K_w]:
			self.tank_move_direction = -1
		if keys[pg.K_s]:
			self.tank_move_direction = 1
		if keys[pg.K_LEFT]:
			self.turret_direction = 1
		if keys[pg.K_RIGHT]:
			self.turret_direction = -1
		if keys[pg.K_SPACE] and self.bullet_timer == 0:
			self.add_bullet(bullets)
			bullets.add(bullet(self.turret_rect.center, self.turret_angle))
			self.bullet_timer = self.gun_cooldown
		if self.bullet_timer > 0:
			self.bullet_timer -= 1
			
	def add_bullet(self, bullets):
		if self.gun == gun_type.basic:
			bullets.add(bullet(self.turret_rect.center, self.turret_angle))
		if self.gun == gun_type.advanced:
			bullets.add(bullet(self.turret_rect.center, self.turret_angle))
			bullets.add(bullet(self.turret_rect.center, self.turret_angle - 15))
			bullets.add(bullet(self.turret_rect.center, self.turret_angle + 15))
		if self.gun == gun_type.ultra:
			bullets.add(bullet(self.turret_rect.center, self.turret_angle))
			bullets.add(bullet(self.turret_rect.center, self.turret_angle - 15))
			bullets.add(bullet(self.turret_rect.center, self.turret_angle + 15))
			bullets.add(bullet(self.turret_rect.center, self.turret_angle - 25))
			bullets.add(bullet(self.turret_rect.center, self.turret_angle + 25))
			
	def update(self, screen_rect):
		self.spin_turret();
		self.spin_tank();
		self.move_tank(screen_rect);
		self.turret_direction = 0
		self.tank_spin_direction = 0
		self.tank_move_direction = 0
		
	def upgrade(self):
		if self.gun == gun_type.basic:
			self.gun = gun_type.advanced
		elif self.gun == gun_type.advanced:
			self.gun = gun_type.ultra
		else:
			self.gun_cooldown -= 5
			
	def downgrade(self):
		self.gun_cooldown = 50
		if self.gun == gun_type.advanced:
			self.gun = gun_type.basic
		elif self.gun == gun_type.ultra:
			self.gun = gun_type.advanced
		else:
			GAME_OVER = True
		
	def draw(self, surface):
		surface.blit(self.tank, self.tank_rect);
		surface.blit(self.turret, self.turret_rect);
		if not self.gun == gun_type.basic:
			extra_turret = pg.transform.rotate(self.turret_start, self.turret_angle + 15)
			extra_rect = extra_turret.get_rect(center = self.turret_rect.center)
			surface.blit(extra_turret, extra_rect);
			extra_turret = pg.transform.rotate(self.turret_start, self.turret_angle - 15)
			extra_rect = extra_turret.get_rect(center = self.turret_rect.center)
			surface.blit(extra_turret, extra_rect);
		if self.gun == gun_type.ultra:
			extra_turret = pg.transform.rotate(self.turret_start, self.turret_angle + 25)
			extra_rect = extra_turret.get_rect(center = self.turret_rect.center)
			surface.blit(extra_turret, extra_rect);
			extra_turret = pg.transform.rotate(self.turret_start, self.turret_angle - 25)
			extra_rect = extra_turret.get_rect(center = self.turret_rect.center)
			surface.blit(extra_turret, extra_rect);

class bullet(pg.sprite.Sprite):
	def __init__(self, location, angle):
		pg.sprite.Sprite.__init__(self)
		self.angle = angle
		self.image = pg.transform.rotate(BULLET, angle - 90)
		self.speed = 10
		self.pos = location
		self.rect = self.image.get_rect(center=location)
		self.done = False;
		
	def update(self, screen_rect):
		self.pos = (self.pos[0] + self.speed*math.sin(math.radians(self.angle + 90)), self.pos[1] + self.speed*math.cos(math.radians(self.angle + 90)))
		self.rect = self.image.get_rect(center = self.pos)
		self.remove(screen_rect)
	def remove(self, screen_rect):
		if not self.rect.colliderect(screen_rect):
			self.kill()
	def get_pos(self):
		return self.pos
			
class missile_type(Enum):
	easy = 1
	normal = 2
	hard = 3
	
class missile(pg.sprite.Sprite):
	def __init__(self, location, angle, type, player_pos):
	
		pg.sprite.Sprite.__init__(self)
		self.angle = angle
		self.type = type
		
		if type == missile_type.easy:
			self.image = pg.transform.rotate(MISSILE_1, angle)
			self.speed = 4
		else:
			self.speed = 6
			self.angle = ( math.atan((player_pos[0] - location[0])/ (player_pos[1] - location[1]))) * 180/math.pi - 90;
			if player_pos[1] < location[1]:
				self.angle += 180
			
		if type == missile_type.normal:
			self.image = pg.transform.rotate(MISSILE_2, self.angle)
		if type == missile_type.hard:
			self.speed = 4.5
			self.image = pg.transform.rotate(MISSILE_3, self.angle)
		self.pos = location
		self.rect = self.image.get_rect(center=location)
		self.done = False;
		
	def update(self, screen_rect, player_pos):
		if self.type == missile_type.hard:
			self.angle = ( math.atan((player_pos[0] - self.pos[0])/ (player_pos[1] - self.pos[1]))) * 180/math.pi - 90;
			if player_pos[1] < self.pos[1]:
				self.angle += 180
			self.image = pg.transform.rotate(MISSILE_3, self.angle)
			
		self.pos = (self.pos[0] + self.speed*math.sin(math.radians(self.angle + 90)), self.pos[1] + self.speed*math.cos(math.radians(self.angle + 90)))
		self.rect = self.image.get_rect(center = self.pos)
		self.remove(screen_rect)
	def check_shot(self, bullet):
		if self.rect.collidepoint(bullet.get_pos()):
			self.kill()
			return True
			
	def check_hit(self, tank_rect):
		if self.rect.colliderect(tank_rect):
			self.kill()
			return True
		return False
	
	
	def remove(self, screen_rect):
		if not self.rect.colliderect(screen_rect):
			self.kill()
		
		
class Driver(object):
	def __init__(self):
		self.screen = pg.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.done = False
		self.keys = pg.key.get_pressed()
		self.player = Tank((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
		self.bullets = pg.sprite.Group()
		self.missiles = pg.sprite.Group()
		self.island = ISLAND
		self.island_rect = self.island.get_rect(center =(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
		self.frequency = 256
		self.goal_amount = 5
		self.missile_chance = (100, 0, 0)
		self.missile_tick = 0;
		self.score = 0;
		self.clock = pg.time.Clock()
		self.fps = FPS_LOCK

	def update_objects(self):
		self.check_collisions()
		self.player.update(self.island_rect)
		self.bullets.update(self.screen_rect)
		self.missiles.update(self.screen_rect, self.player.get_pos())
		
	def draw_objects(self):
		self.screen.fill(BACKGROUND_COLOR)
		self.screen.blit(self.island, self.island_rect)
		self.bullets.draw(self.screen)
		self.player.draw(self.screen)
		self.missiles.draw(self.screen)
		
	def check_collisions(self):
		for bullet in self.bullets:
			for missile in self.missiles:
				if missile.check_shot(bullet):
					self.score += 1
					print(self.score)
		for missile in self.missiles:		
			if(missile.check_hit(self.player.get_rect())):
				self.player.downgrade()
	
	def game_loop(self):
		while not self.done:
			for event in pg.event.get():
				self.keys = pg.key.get_pressed()
				if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
					self.done = True
			self.player.key_press(self.keys, self.bullets)
			self.update_objects()
			self.draw_objects()
			pg.display.flip()
			if self.missile_tick > self.frequency:
				self.add_missile()
				self.missile_tick = 0
			self.missile_tick += 1
			if(self.score >= self.goal_amount):
				self.new_wave()
			self.clock.tick(self.fps)
			pg.display.set_caption("{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps()))
			
	def add_missile(self):
		side = randint(1, 4)
		side_pos = randint(100, SCREEN_SIZE[0] - 100);
		if side == 1:
			location = (0, side_pos)
			angle = 0
		if side == 2:
			location = (SCREEN_SIZE[0], side_pos)
			angle = 180
		if side == 3:
			location = (side_pos, 0)
			angle = 270
		if side == 4:
			location = (side_pos, SCREEN_SIZE[1])
			angle = 90
		rand = randint(1, 100)
		
		if rand < self.missile_chance[0]:
			type = missile_type.easy
		elif rand < self.missile_chance[0] + self.missile_chance[1]:
			type = missile_type.normal
		else:
			type = missile_type.hard
		self.missiles.add(missile(location, angle, type, self.player.get_pos()))
			
	
	def new_wave(self):
		self.frequency /= 1.5
		self.goal_amount += 1.5 * self.goal_amount
		self.player.upgrade()
		missile_3_chance = self.missile_chance[2] + self.missile_chance[1] / 3
		missile_2_chance  = self.missile_chance[1] * 2 / 3
		missile_2_chance += self.missile_chance[0] / 3
		missile_1_chance = self.missile_chance[0] * 2 / 3
		self.missile_chance = (missile_1_chance, missile_2_chance, missile_3_chance);

			
if __name__ == "__main__":
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pg.init()
	pg.display.set_caption("TANKS")
	pg.display.set_mode(SCREEN_SIZE)
	TURRET = pg.transform.scale(pg.image.load("Textures/Tank_Turret.png").convert_alpha(),(75, 75))
	TANK = pg.transform.scale(pg.image.load("Textures/Tank_Base.png").convert_alpha(), (50, 50))
	BULLET = pg.transform.scale(pg.image.load("Textures/Bullet.png").convert_alpha(), (40, 40))
	ISLAND = pg.transform.scale(pg.image.load("Textures/Island.png").convert_alpha(), (BORDER_SIZE, BORDER_SIZE))
	MISSILE_1 = pg.transform.scale(pg.image.load("Textures/Missile_1.png").convert_alpha(),(100, 100)).subsurface((10, 35, 90, 30))
	MISSILE_2 = pg.transform.scale(pg.image.load("Textures/Missile_2.png").convert_alpha(),(100, 100)).subsurface((10, 35, 90, 30))
	MISSILE_3 = pg.transform.scale(pg.image.load("Textures/Missile_3.png").convert_alpha(),(100, 100)).subsurface((10, 35, 90, 30))
	run = Driver()
	run.game_loop()
	pg.quit()
	sys.exit()			