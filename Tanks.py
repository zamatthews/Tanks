#Tanks
#Zach Matthews
#CS 475
import os
import sys
import math
import pygame as pg

CAPTION = "Tanks"
SCREEN_SIZE = (1000, 1000)
BACKGROUND_COLOR = (50, 50, 50)
COLOR_KEY = (255, 0, 255)

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
		
	def spin_turret(self):
		self.turret_angle += self.rotate_speed*self.turret_direction
		self.turret_angle += self.turn_speed*self.tank_spin_direction
		self.turret = pg.transform.rotate(self.turret_start, self.turret_angle)
		self.turret_rect = self.turret.get_rect(center = self.turret_rect.center)
		
	def spin_tank(self):
		self.tank_angle += self.turn_speed*self.tank_spin_direction
		self.tank = pg.transform.rotate(self.tank_start, self.tank_angle)
		self.tank_rect = self.tank.get_rect(center = self.tank_rect.center)
		
	def move_tank(self):
		
		self.tank_pos = (self.tank_pos[0] + self.move_speed*math.sin(math.radians(self.tank_angle - 90))*self.tank_move_direction, self.tank_pos[1] + self.move_speed*math.cos(math.radians(self.tank_angle - 90))*self.tank_move_direction)
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
		if keys[pg.K_q]:
			self.turret_direction = 1
		if keys[pg.K_e]:
			self.turret_direction = -1
#		if keys[pg.K_SPACE]:
#			bullets.add(bullet(self.turret_rect.center, self.turret_angle))	
		
	def update(self):
		self.spin_turret();
		self.spin_tank();
		self.move_tank();
		self.turret_direction = 0
		self.tank_spin_direction = 0
		self.tank_move_direction = 0
		
	def draw(self, surface):
		surface.blit(self.tank, self.tank_rect);
		surface.blit(self.turret, self.turret_rect);
		
class bullet(object):
	def __init__(self):
		self.it = 0
		

class Driver(object):
	def __init__(self):
		self.screen = pg.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.done = False
		self.keys = pg.key.get_pressed()
		self.player = Tank((250, 250))
		self.bullets = pg.sprite.Group()

	def update_objects(self):
		self.player.update()
#		self.bullets.update(self.screen_rect)
		
	def draw_objects(self):
		self.screen.fill(BACKGROUND_COLOR)
		self.player.draw(self.screen)
#		self.bullets.draw(self.screen_rect)
		
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
	TURRET = pg.transform.scale(pg.image.load("Textures/Tank_Turret.png").convert_alpha(),(150, 150))
	TANK = pg.transform.scale(pg.image.load("Textures/Tank_Base.png").convert_alpha(), (100, 100))
#	TURRET.set_colorkey(COLOR_KEY)
#	TANK.set_colorKey(COLOR_KEY)
	run = Driver()
	run.game_loop()
	pg.quit()
	sys.exit()			