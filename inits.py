import pygame									#精灵小组、逻辑更新，绘制图像
import random
from os import path

global score

WIDTH,HIGHT = 600,750   						#全部大写，通常是常量
NEW_ENEMY_GENERATE_INTERVAL = 500				#每个多少毫秒生成一个敌人

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

MISSILE_LIFETIME = 10000
MISIILE_INTERVAL = 500

class Player(pygame.sprite.Sprite):									#产生一个精灵
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.flip(player_img,False,True)	#第一个参数是左右反转，第二个是上下翻转
		self.image = pygame.transform.scale(self.image,(53,40))		#缩放
		self.image.set_colorkey(BLACK)							#用color_key方法除去方框周边的黑色部分
		self.rect = self.image.get_rect()
		self.radius = 20
		#pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)

		self.rect.centerx = WIDTH/2
		self.rect.bottom = HIGHT

		self.hp = 100
		self.lives = 3
		self.score = 0
		self.hidden = False
		self.hide_time = 0

		self.is_firing_missile = False
		self.start_missile_time = 0
		self.last_missile_time = 0

	def update(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.rect.x -= 8
		if keystate[pygame.K_RIGHT]:
			self.rect.x += 8
		if keystate[pygame.K_UP]:
			self.rect.y -= 8
		if keystate[pygame.K_DOWN]:
			self.rect.y += 8

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom >HIGHT:
			self.rect.bottom = HIGHT

		now = pygame.time.get_ticks()
		if self.hidden and now - self.hide_time>1000:			
			self.hidden = False
			self.rect.bottom = HIGHT
			self.rect.centerx = WIDTH/2

		if self.is_firing_missile:
			if now - self.start_missile_time <= MISSILE_LIFETIME:
				if now - self.last_missile_time >= MISIILE_INTERVAL:
					missile = Missile(self.rect.center)
					missiles.add(missile)
					self.last_missile_time = now
			else:
				self.is_firing_missile = False

	def shoot(self):
		bullet = Bullet(self.rect.centerx,self.rect.centery)
		bullets.add(bullet)
		shoot_sound.play()

	def hide(self):										#出生后无敌时间
		self.hidden = True
		self.rect.y = -200
		self.hide_time = pygame.time.get_ticks()

	def fire_missile(self):
		self.is_firing_missile = True
		self.start_missile_time = pygame.time.get_ticks()




class Enemy(pygame.sprite.Sprite):
	"""docstring for Enemy"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		img_width = random.randint(20,120)
		img_height = int(img_width*70/72)
		self.image = pygame.transform.scale(enemy_img,(img_width,img_height))
		self.image.set_colorkey(BLACK)
		self.image_origin = self.image.copy()
		self.rect = self.image.get_rect()
		self.radius = int(img_width/2)
		#pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)

		self.rect.x = random.randint(0,WIDTH-self.rect.w)
		self.rect.bottom = 0


		self.vx = random.randint(-2,2)
		self.vy = random.randint(2,10)

		self.last_time = 0
		self.rotate_speed = random.randint(-5,5)
		self.rotate_angle = 0


	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy
		self.rotate()

		# if self.rect.left>WIDTH:
		# 	self.kill()
		# if self.rect.right<0:
		# 	self.kill()


	def rotate(self):														#制作岩石的旋转
		now = pygame.time.get_ticks()
		if now - self.last_time>30:
			self.rotate_angle = (self.rotate_angle + self.rotate_speed) % 360
			self.image = pygame.transform.rotate(self.image_origin,self.rotate_angle)
			old_center = self.rect.center
			self.rect = self.image.get_rect()
			self.rect.center = old_center



class Enemy1(pygame.sprite.Sprite):
	"""docstring for Enemy"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.score = 1000
		self.image = pygame.transform.flip(enemy1_img,False,True)	#第一个参数是左右反转，第二个是上下翻转
		self.image = pygame.transform.scale(self.image,(40,80))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		#pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)

		self.rect.x = random.randint(0,WIDTH-self.rect.w)
		self.rect.bottom = 0


		self.vx = random.randint(-2,2)
		self.vy = random.randint(2,10)



	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy



class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image.set_colorkey()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

	def update(self):
		self.rect.y -= 10



class Explosion(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image = explosion_animation[0]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0								#表示现在是爆炸效果的第几张图像
		self.last_time = 0
		explosion_sound.play()


	def update(self):
		now = pygame.time.get_ticks()				#在update中判断更新时间
		if now - self.last_time>40:
			if self.frame<len(explosion_animation):
				self.image = explosion_animation[self.frame]
				self.image.set_colorkey(BLACK)
				self.frame += 1
				self.last_time = now
			else:
				self.kill()		
class Powerup(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		random_num = random.random()
		if random_num >= 0 and random_num < 0.5:
			self.type = 'add_hp'
		elif random_num >= 0.5 and random_num < 0.8:
			self.type = 'add_missile'
		else:
			self.type = 'add_lives'


		self.image = powerup_imgs[self.type]
		self.image = pygame.transform.scale(self.image,(40,40))	
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.vx = random.randint(-2,2)
		self.vy = random.randint(2,10)

		self.rotate_speed = random.randint(-5,5)
		self.rotate_angle = 0

	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy


class Missile(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image = missile_img
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		self.rect.center = center

	def update(self):
		self.rect.y -= 5




def draw_text(text,surface,color,x,y,size):
	font_name = pygame.font.match_font('arial')
	font = pygame.font.Font(font_name ,size)
	text_surface = font.render(text,True,color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surface.blit(text_surface,text_rect)



def draw_ui():
	pygame.draw.rect(screen,GREEN,(10,10,player.hp,15))
	pygame.draw.rect(screen,WHITE,(10,10,100,15),2)

	draw_text(str(player.score),screen,WHITE,WIDTH/2,10,20)
	img_rect = player_img_small.get_rect()
	img_rect.right = WIDTH - 10
	img_rect.y = 10
	for i in range(player.lives):
		screen.blit(player_img_small,img_rect)
		img_rect.right = img_rect.x - 10


def show_menu():
	global game_state, screen
	screen.blit(background1, background1_rect)

	draw_text('SPACE SHOOTER!',screen,WHITE,WIDTH/2,100,40)
	draw_text('Press Space To Start',screen,WHITE,WIDTH/2,300,20)
	draw_text('Press Esc key to quit',screen,WHITE,WIDTH/2,350,20)

	event_list = pygame.event.get()
	for event in event_list:
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
			if event.key == pygame.K_SPACE:
				game_state = 1

	pygame.display.flip()


pygame.mixer.pre_init(44100,-16,2,2048)			#初始化,减少延时
pygame.mixer.init()
pygame.init()                               	#初始化

screen = pygame.display.set_mode((WIDTH,HIGHT))	
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()						#游戏的时钟


img_dir = path.join(path.dirname(__file__),'img')			#绝对路径
background_dir = path.join(img_dir,'background.png')		#导入背景图
background = pygame.image.load(background_dir).convert()	#将图片导入到pygame
background_rect = background.get_rect()						#获取background的尺寸信息

background1_dir = path.join(img_dir,'background1.png')		#导入背景图
background1 = pygame.image.load(background1_dir).convert()	#将图片导入到pygame
background1_rect = background1.get_rect()					#获取background的尺寸信息

background_1_dir = path.join(img_dir,'background_1.png')		#导入背景图
background_1 = pygame.image.load(background_1_dir).convert()	#将图片导入到pygame
background_1_rect = background1.get_rect()						#获取background的尺寸信息


player_dir = path.join(img_dir,'spaceShips_007.png')			#导入图片
player_img = pygame.image.load(player_dir).convert()
player_img_small = pygame.transform.scale(player_img,(26,20))	#表示生命数
player_img_small.set_colorkey(BLACK)
enemy_dir = path.join(img_dir,'spaceMeteors_001.png')
enemy_img = pygame.image.load(enemy_dir).convert()
enemy1_dir = path.join(img_dir,'spaceRockets_001.png')
enemy1_img = pygame.image.load(enemy1_dir).convert()
bullet_dir = path.join(img_dir,'spaceMissiles_016.png')
bullet_img = pygame.image.load(bullet_dir).convert()
missile_dir = path.join(img_dir,'spaceMissiles_003.png')
missile_img = pygame.image.load(missile_dir).convert()




explosion_animation = []									#动画效果
for i in range(9):
	explosion_dir = path.join(img_dir,'regularExplosion0{}.png'.format(i))
	img = pygame.image.load(explosion_dir).convert()
	img.set_colorkey(BLACK)
	img = pygame.transform.scale(img,(76,75))
	explosion_animation.append(img)

powerup_imgs = {}											#创建一个字典存放补给品
powerup_add_hp_dir = path.join(img_dir,'gem1.png')
powerup_imgs['add_hp'] = pygame.image.load(powerup_add_hp_dir).convert()
powerup_add_lives_dir = path.join(img_dir,'gem5.png')
powerup_imgs['add_lives'] = pygame.image.load(powerup_add_lives_dir).convert()
powerup_add_missile_dir = path.join(img_dir,'gem3.png')
powerup_imgs['add_missile'] = pygame.image.load(powerup_add_missile_dir).convert()


sound_dir = path.join(path.dirname(__file__),'sound')
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot4.wav'))
explosion_sound = pygame.mixer.Sound(path.join(sound_dir,'Explosion11.wav'))
pygame.mixer.music.load(path.join(sound_dir,'Soliloquy.wav'))

player = Player()							#实例化
enemy = Enemy()
enemy1 = Enemy1()
enemys = pygame.sprite.Group()				#生成精灵小组
enemy1s = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
powerups = pygame.sprite.Group()
missiles = pygame.sprite.Group()

for i in range(10):							#增加敌人数量
	enemy = Enemy()
	enemys.add(enemy)

for i in range(1):
	enemy1 = Enemy1()
	enemy1s.add(enemy1)


last_enemy_generate_time = 0


game_over = False
game_state = 0
#pygame.mixer.music.set_volume(0.8)			#调节声音大小
pygame.mixer.music.play(loops=-1)   		#loops=-1表示无限循环
while not game_over:
	clock.tick(60)


	if game_state == 0:
		show_menu()
	elif game_state == 1:
		now = pygame.time.get_ticks()
		if now - last_enemy_generate_time > NEW_ENEMY_GENERATE_INTERVAL:
			enemy = Enemy()
			enemys.add(enemy)
			last_enemy_generate_time = now
		if int(now) % 500 == 0:
			enemy1 = Enemy1()
			enemy1s.add(enemy1)


		event_list = pygame.event.get()
		if len(event_list)>0:
			print(event_list)

		for event in event_list:
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_over = True
				if event.key == pygame.K_SPACE:
					player.shoot()


		screen.fill(WHITE)
		screen.blit(background,background_rect)


		enemys.update()
		enemy1s.update()
		player.update()
		bullets.update()
		explosions.update()
		missiles.update()
		powerups.update()


		#hits = pygame.sprite.spritecollide(player,enemys,False,pygame.sprite.collide_rect_ratio(0.8))	#缩放hitbox比例
		hits = pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)

		for hit in hits:
			player.hp -= hit.radius
			if player.hp<0:
				player.lives -= 1
				player.hp = 100
				player.hide()
				if player.lives == 0:
					game_over = True

		hits = pygame.sprite.groupcollide(enemys,bullets,True,True)	#碰撞检测

		for hit in hits:										#实例化
			explosion = Explosion(hit.rect.center)
			explosions.add(explosion)
			player.score += hit.radius
			enemy = Enemy()
			enemys.add(enemy)
			if random.random() >0.9:									#random.random得到0到1之间的数
				powerup = Powerup(hit.rect.center)
				powerups.add(powerup)


		hits = pygame.sprite.groupcollide(enemy1s,bullets,True,True)	#碰撞检测

		for hit in hits:												#实例化
			explosion = Explosion(hit.rect.center)
			explosions.add(explosion)
			player.score += hit.score
			enemy1 = Enemy1()
			enemy1s.add(enemy1)
			if random.random() >0.9:									#random.random得到0到1之间的数
				powerup = Powerup(hit.rect.center)
				powerups.add(powerup)


		hits = pygame.sprite.groupcollide(enemys,missiles,True,True)	#碰撞检测

		for hit in hits:												#实例化
			explosion = Explosion(hit.rect.center)
			explosions.add(explosion)
			player.score += hit.radius
			enemy = Enemy()
			enemys.add(enemy)
			if random.random() >0.9:									#random.random得到0到1之间的数
				powerup = Powerup(hit.rect.center)
				powerups.add(powerup)



		hits = pygame.sprite.spritecollide(player,powerups,True)

		for hit in hits:
			if hit.type == 'add_hp':
				player.hp += 25
				if player.hp > 100:
					player.hp = 100
			elif hit.type == 'add_lives':
				player.lives += 1
				if player.lives > 3:
					player.lives = 3
			else:
				player.fire_missile()


		screen.blit(player.image,(player.rect.x,player.rect.y))
		enemys.draw(screen)										#一定要记得话draw
		enemy1s.draw(screen)
		bullets.draw(screen)
		missiles.draw(screen)
		explosions.draw(screen)
		powerups.draw(screen)



		draw_ui()


		pygame.display.flip()          			#翻转;渲染



# 游戏 Game Over 后显示最终得分
font_name = pygame.font.match_font('arial')
font = pygame.font.Font(font_name, 80)
font_1 = pygame.font.Font(font_name, 40)
text = font.render('Score: '+ str(player.score), True, WHITE)
text_1 = font_1.render('YOUR LAST RESULT ', True, WHITE)
text_rect = text.get_rect()
text_1_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
text_1_rect.centerx = screen.get_rect().centerx -40
text_1_rect.centery = screen.get_rect().centery - 100
screen.blit(background_1, (0, 0))
screen.blit(text, text_rect)
screen.blit(text_1, text_1_rect)
 
 
# 显示得分并处理游戏退出
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()