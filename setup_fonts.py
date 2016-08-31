import pygame, os
'''
def get_my_fonts():
	my_font_list = []
	for root, dirs, files in os.walk('font'):
		for file in files:
			if file.endswith(".ttf"):
				my_font_list.append(os.path.join(root, file))
	return my_font_list           
'''
def get_my_fonts():
	my_font_list = []
	for fontfile in os.listdir('font'):
		if fontfile.endswith(".ttf"):
			my_font_list.append('font/'+fontfile)
			print(fontfile)
	return my_font_list

def make_font(fonts, size):
	available = pygame.font.get_fonts()
	print(available)
	print('=======================================================================================================================')
	print(font_preferences)
	choices = map(lambda x:x.lower().replace(' ', ''), fonts)
	for choice in choices:
		if choice in available:
			return pygame.font.SysFont(choice, size)
	return pygame.font.Font(None, size)

def scott_make_font(fonts, size):
	available = font_preferences

	#choices = map(lambda x:x.lower().replace(' ', ''), fonts)
	for choice in fonts:
		if choice in available:
			return pygame.font.Font(choice, size)
	return pygame.font.Font(None, size)

_cached_fonts = {}
def get_font(font_preferences, size):
	global _cached_fonts
	key = str(font_preferences) + '|' + str(size)
	font = _cached_fonts.get(key, None)
	if font == None:
		font = scott_make_font(font_preferences, size)
		_cached_fonts[key] = font
	return font

_cached_text = {}
def create_text(text, fonts, size, color):
	global _cached_text
	key = '|'.join(map(str, (fonts, size, color, text)))
	image = _cached_text.get(key, None)
	if image == None:
		font = get_font(fonts, size)
		image = font.render(text, True, color)
		_cached_text[key] = image
	return image

font_preferences = [
	'font/IndieFlower.ttf', # fun Gamey font
	'font/OpenSans-Light.ttf', # clean
	'font/PoiretOne-Regular.ttf', # good Space font
	]

header_font = [
	'font/OpenSans-Light.ttf', # clean
	'font/PoiretOne-Regular.ttf', # good Space font
	]



def main():
    """Testing out fonts
    """
    pygame.init()
    print(font_preferences)
    a = create_text('Hello World', font_preferences, 24, (255,255,255))

    

if __name__ == '__main__':
    main()