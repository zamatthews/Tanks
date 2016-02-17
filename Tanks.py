#Tanks
#Zach Matthews
#CS 475
import os
import sys
import math
import pygame as pg
from enum import Enum

CAPTION = "Tanks"
SCREEN_SIZE = (700, 700)
BACKGROUND_COLOR = (33, 17, 255)
BORDER_SIZE = 500


class gun_type(Enum):
	basic = 1
	advanced = 2
	ultra = 3
class Tank(object):
	def __init__(self, location):
		self.turret_start = TURRET
		self.turret = TURRET;
		self.tank_start = TANK;
		self.tank = TANK
		self.turret_rect = self.turret.get_rect(center = location)
		self.tank_rect = self.tank.get_rect(center = location)
		self.tank_pos = location
		self.turret_angle = 0
		self.tank_angle = 0
		self.turret_direction = 0
		self.tank_spin_direction = 0
		self.tank_move_direction = 0
		self.rotate_speed = 1
		self.turn_speed = 1
		self.move_speed = 1
		self.bullet_timer = 0;
		
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
		return tank_pos
		
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
			bullets.add(bullet(self.turret_rect.center, self.turret_angle))
			self.bullet_timer = 60
		if self.bullet_timer > 0:
			self.bullet_timer -= 1
	def update(self, screen_rect):
	
		self.spin_turret();
		self.spin_tank();
		self.move_tank(screen_rect);
		self.turret_direction = 0
		self.tank_spin_direction = 0
		self.tank_move_direction = 0
		
	def draw(self, surface):
		surface.blit(self.tank, self.tank_rect);
		surface.blit(self.turret, self.turret_rect);

class bullet(pg.sprite.Sprite):
	def __init__(self, location, angle):
		pg.sprite.Sprite.__init__(self)
		self.angle = angle
		self.image = pg.transform.rotate(BULLET, angle - 90)
		self.speed = 2
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
		
class Driver(object):
	def __init__(self):
		self.screen = pg.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.done = False
		self.keys = pg.key.get_pressed()
		self.player = Tank((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
		self.bullets = pg.sprite.Group()
		self.island = ISLAND
		self.island_rect = self.island.get_rect(center =(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))

	def update_objects(self):
		self.player.update(self.island_rect)
		self.bullets.update(self.screen_rect)
		
	def draw_objects(self):
		self.screen.fill(BACKGROUND_COLOR)
		self.screen.blit(self.island, self.island_rect)
		self.bullets.draw(self.screen)
		self.player.draw(self.screen)
		
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
		
if __name__ == "__main__":
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pg.init()
	pg.display.set_caption(CAPTION)
	pg.display.set_mode(SCREEN_SIZE)
	TURRET = pg.transform.scale(pg.image.load("Textures/Tank_Turret.png").convert_alpha(),(75, 75))
	TANK = pg.transform.scale(pg.image.load("Textures/Tank_Base.png").convert_alpha(), (50, 50))
	BULLET = pg.transform.scale(pg.image.load("Textures/Bullet.png").convert_alpha(), (40, 40))
	ISLAND = pg.transform.scale(pg.image.load("Textures/Island.png").convert_alpha(), (BORDER_SIZE, BORDER_SIZE))
	run = Driver()
	run.game_loop()
	pg.quit()
	sys.exit()			