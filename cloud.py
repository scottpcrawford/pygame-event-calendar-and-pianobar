import pygame as pg, random


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
_image_library = {}


class Cloud(pg.sprite.Sprite):
	def __init__(self, color, width, height, speed):
		super().__init__()
		self.image = pg.Surface([width, height])
		self.image.fill(pg.Color('black'))
		
		pg.draw.rect(self.image, color, [0,0, width, height])
		#self.image = pg.image.load('img/clouds/day/path3336.png')
		self.image.set_colorkey(pg.Color('black'))
		self.image = self.image.convert()
		self.image.set_alpha(255)
		self.rect = self.image.get_rect()
		move_direction = 1

		self.speed = speed

	def update(self):
		self.rect.x += self.speed*self.move_direction
		if self.rect.right < 0:
			self.rect.x = SCREEN_WIDTH
			self.rect.y = random.randint(0, 400)
			self.speed = random.randint(1,5)
		elif self.rect.left >= SCREEN_WIDTH:
			self.rect.x = -150
			self.rect.y = random.randint(0, 400)
			self.speed = random.randint(1,5)


	def move(self, pixels):
		self.rect.x += pixels*self.move_direction

	def moveRight(self, pixels):
		self.rect.x += pixels
 
	def moveLeft(self, pixels):
		self.rect.x -= pixels
 
	def moveUp(self, pixels):
		self.rect.y -= pixels
 
	def moveDown(self, pixels):
		self.rect.y += pixels

	def create_clouds(num, img):
		sprite_list = pg.sprite.Group()
		for x in range(0, num):
			cloud = Cloud(pg.Color('black'), 200, 200, random.randint(1,3))
			cloud.image = img[random.choice(list(img.keys()))]
			cloud.rect.x = random.randint(0,SCREEN_WIDTH)
			cloud.rect.y = random.randint(0,200)
			cloud.move_direction = random.choice([-1,1])
			sprite_list.add(cloud)
		return sprite_list


class World(pg.sprite.Sprite):
	def __init__(self, screen, background, sprites):
		super().__init__()
		self.background = background
		self.screen = screen
		self.sprites = sprites
'''
	def get_image(path):
		global _image_library
		image = _image_library.get(path)
		if image == None:
			canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
			image = pg.image.load(canonicalized_path)
			_image_library[path] = image
		return image

	#load images in a dict
	from os import listdir
	from os.path import isfile, join
	IMAGE_PATH = "/images"
	images_dict = dict()
	images = [ f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH,f)) and f.endswith('png') ]
	for filename in images:
    	images_dict[os.path.splitext(filename)[0]] = pg.image.load(join(IMAGE_PATH,filename))
    
    image = images_dict['fox']
'''