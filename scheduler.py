
import pygame as pg
import time, random, sys, dateutil.parser, os 
from datetime import datetime

# import functions from my files
from run_pianobar import start_pianobar, process_input, get_song_data
from setup_fonts import create_text, font_preferences, header_font
from file_parser import readfile, parse_line, return_list, update_cal
from cloud import Cloud
from weather import Weather

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Game(object):
	def __init__(self, screen):
		self.done = False
		self.screen = screen
		self.clock = pg.time.Clock()
		self.fps = 60
		self.RADIO_STATION = '39' # or 1591330390268116913
		self.BACKGROUND_IMG = 'img/bg/day_tree.png'
		self.SCREEN_WIDTH = SCREEN_WIDTH
		self.SCREEN_HEIGHT = SCREEN_HEIGHT
		self.RADIO_RUNNING = False
		self.RESTING = False
		self.SHOWGOALS = False
		self.grass = 'img/bg/day_grass.png'
		self.day_clouds = pg.sprite.RenderUpdates()
		self.night_clouds = pg.sprite.RenderUpdates()
		self.all_sprites_list = pg.sprite.RenderUpdates()
		self.quote_list = return_list('quotes.txt')
		self.contributions = return_list('contributions.txt')
		self.goals = return_list('goals.txt')
		self.weather = Weather()
		self.weather_observation = {}
		self.phrase = random.choice(self.quote_list)
		self.cwd = os.getcwd() #windows
		#self.cwd = '/home/pi/.config/pianobar' # linux
		## DAIYE COLORS ###
		self.HEADER_COLOR = pg.Color('black')
		self.CONTENT_COLOR = pg.Color('indianred4')
		self.BG_COLOR = pg.Color('skyblue')
		self.current_events = []
		self.upcoming_events = []
		
		# User events:
		self.UPDATECALENDAR = pg.USEREVENT + 1
		self.UPDATEQUOTE = pg.USEREVENT + 2
		self.NIGHTRADIO = pg.USEREVENT + 3
		self.CHANGESTATE = pg.USEREVENT + 4
		self.UPDATEWEATHER = pg.USEREVENT + 5
		#self.SHOWGOALS = pg.USEREVENT + 6
		pg.time.set_timer(self.UPDATECALENDAR, 60000) #update calendar every 60 seconds     
		pg.time.set_timer(self.UPDATEQUOTE, 20000) #update quote every 20 seconds
		pg.time.set_timer(self.NIGHTRADIO,300000) # check for relaxation radio time
		pg.time.set_timer(self.UPDATEWEATHER, 600000)
		pg.time.set_timer(self.CHANGESTATE, 300000)
		#pg.time.set_timer(self.SHOWGOALS, 6000)
		
		self.DAYGFX = load_gfx(os.path.join("img", "clouds", "day"))
		self.NTGFX = load_gfx(os.path.join("img", "clouds", "night"))
		self.BGIMG  = load_gfx(os.path.join('img', 'bg'))
		self.keymap_dict = {pg.K_n: 'n', pg.K_PLUS: '+', pg.K_KP_PLUS: '+', pg.K_EQUALS: '+', pg.K_MINUS: '-', pg.K_KP_MINUS: '-', 
							pg.K_p: 'p', pg.K_SPACE: 'p', pg.K_q: 'q', pg.K_r: 'r', pg.K_s: 's', pg.K_1: 's6\n', pg.K_2: 's4\n', 
							pg.K_3: 's15\n', pg.K_4: 's25\n', pg.K_5: 's48\n', pg.K_6: 's37\n', pg.K_7: 's52\n', pg.K_8: 's58\n'}

	
	def update_calendar(self):
		update_cal()
		self.goals = return_list('goals.txt')
		self.contributions = return_list('contributions.txt')
		self.current_events,self.upcoming_events = update_event_lists('calevents.txt')
		if not any('Resting' in s for s in self.current_events):
			self.RESTING = False
			print('not resting. setting to False and restarting timer')
			pg.time.set_timer(self.NIGHTRADIO,30000)
		else:
			self.RESTING = True
			print('resting is:',self.RESTING)	


	def update_quote(self):
		self.phrase = random.choice(self.quote_list)
		self.SHOWGOALS = not self.SHOWGOALS

	def update_weather(self):
		self.weather_observation = self.weather.get_weather_observation()

	def event_loop(self):
		for event in pg.event.get():
			self.get_event(event)

	def get_event(self, event):
		if event.type == pg.QUIT:
			self.done = True
		elif event.type == self.CHANGESTATE:
			self.change_state()
		elif event.type == self.UPDATECALENDAR:
			self.update_calendar()
		elif event.type == self.UPDATEQUOTE:
			self.update_quote()
		elif event.type == self.UPDATEWEATHER:
			self.update_weather()
		elif event.type == self.NIGHTRADIO:
			if self.RESTING and self.RADIO_RUNNING:
				process_input('s41\n')
				pg.time.set_timer(self.NIGHTRADIO,0)
				print('Station Changed to Relaxation Radio, disabling timer')
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				if self.RADIO_RUNNING:
					process_input('q')
				print('You pressed ESC... Quitting')
				self.done = True
				return
			if not self.RADIO_RUNNING:
				if event.key == pg.K_m and pg.key.get_mods() & pg.KMOD_CTRL:
					print('Attempting to start the music')
					self.RADIO_RUNNING = True
					start_pianobar(sys.platform)
			else:
				if event.key in self.keymap_dict:
					if event.key == pg.K_q:
						self.RADIO_RUNNING = False
						process_input('q')
					elif event.key == pg.K_r:
						print('choosing a random radio station')
						sl = readfile(self.cwd+'/scripts/stationlist')
						random_station = 's'+str(random.randint(0,(len(sl)-1)))+'\n'
						process_input(random_station)
					else:
						process_input(self.keymap_dict[event.key])
				elif event.key == pg.K_9 and pg.key.get_mods() & pg.KMOD_SHIFT:
					process_input('(')
				elif event.key == pg.K_0 and pg.key.get_mods() & pg.KMOD_SHIFT:
					process_input(')')

	def change_state(self):
		#global self.HEADER_COLOR, self.CONTENT_COLOR, self.BG_COLOR
		#hour = int(time.strftime('%H'))
		#if self.BG_COLOR == pg.Color('black'):
		curtime = datetime.now().strftime('%H:%M')
		settime = self.weather.sunset.strftime('%H:%M')
		risetime = self.weather.sunrise.strftime('%H:%M')

		if (curtime > risetime) and (curtime < settime): # Day Time
		#if hour > 7 and hour < 20: # Day Time
		#if self.BG_COLOR == pg.Color('black'):
			self.HEADER_COLOR = pg.Color('black')
			self.CONTENT_COLOR = pg.Color('indianred4')
			self.BG_COLOR = pg.Color('skyblue')
			self.background = self.BGIMG['day_tree']
			self.grass = self.BGIMG['day_grass']
			self.all_sprites_list.remove(self.night_clouds)
			self.all_sprites_list.add(self.day_clouds)
		else: # Night Time
			self.HEADER_COLOR = pg.Color('white')
			self.CONTENT_COLOR = pg.Color('red')
			self.BG_COLOR = pg.Color('black')
			self.background = self.BGIMG['night_tree']
			self.grass = self.BGIMG['night_grass']
			self.all_sprites_list.remove(self.day_clouds)
			self.all_sprites_list.add(self.night_clouds)
		#print(self.all_sprites_list)


	def draw_text(self, mylist):
		for item in mylist:
			self.screen.blit(item[0], item[1])

	def update_text(self):
		drawing_list = []
		drawing_list.append((self.background, (900,165)))
		drawing_list.append((self.grass, (0, 1030)))
		
		# print the weather
		description =  ['current: ', 'temperature: ', 'sunrise: ', 'sunset: ', 'wind: ']
		wx_list = [self.weather_observation['status'].capitalize(), '%0.0f'%self.weather_observation['temperature']+u'\xb0F', self.weather_observation['sunrise'].strftime('%H:%M'),
					self.weather_observation['sunset'].strftime('%H:%M'), str(self.weather_observation['wind']['deg'])+u'\xb0'+' at '+str(self.weather_observation['wind']['speed'])+'mph']
		for index, item in enumerate(wx_list):
					text = create_text((description[index]+item), font_preferences, 24, self.HEADER_COLOR)
					drawing_list.append((text, (1600, 800+25*index)))

		# print current events
		text = create_text('Happening Now:', header_font, 36, self.HEADER_COLOR)			
		drawing_list.append((text, (5,0)))
		if not self.current_events:
			text = create_text('No Active Events', font_preferences, 48, self.CONTENT_COLOR)
			drawing_list.append((text, (35,60)))

			# print the time until next event
			text = create_text('Next Event Starts in: '+display_time_until(self.upcoming_events[0]), font_preferences, 36, self.HEADER_COLOR) # display time remaining until next event ends
			drawing_list.append((text, (1500,0)))

		else:
			for index, item in enumerate(self.current_events):
				text = create_text(item[2]+' ('+item[0][11:16]+' - '+item[1][11:16]+')',font_preferences,48,self.CONTENT_COLOR)
				drawing_list.append((text, (35, 60+50*index)))

			# print the time remaining
			text = create_text('Time Remaining: '+display_time_remaining(self.current_events[0]), font_preferences, 36, self.HEADER_COLOR) # display time remaining until next event ends
			drawing_list.append((text, (1500,0)))	

		# print upcoming events 
		text = create_text('Coming Up: ',header_font, 28, self.HEADER_COLOR)
		drawing_list.append((text, (5,70+50*(len(self.current_events)+1))))
		for index, item in enumerate(self.upcoming_events[0:3]):
			text = create_text(item[2]+' ('+item[0][11:16]+' - '+item[1][11:16]+')',font_preferences,28, pg.Color('steelblue4'))
			drawing_list.append((text,(25,110+50*(len(self.current_events)+1)+40*index)))		

		# print contributions or goals
		silly_list = []
		if self.SHOWGOALS:
			text = create_text('Personal Goals:', header_font, 36, self.HEADER_COLOR)
			silly_list = self.goals
		else:
			text = create_text('Weekly Contributions:', header_font, 36, self.HEADER_COLOR)
			silly_list = self.contributions
		drawing_list.append((text, (5,500)))
		for index, item in enumerate(silly_list):
			text = create_text(item,font_preferences,48,self.CONTENT_COLOR)
			drawing_list.append((text, (35, 540+50*index)))
		
		# display current system time
		text = create_text(time.strftime('%x  %H:%M'),font_preferences,36, self.HEADER_COLOR) 
		drawing_list.append((text, (1615, 1000)))

		#print the random quote
		text = create_text(self.phrase, font_preferences, 28, self.HEADER_COLOR)
		drawing_list.append((text, (5,1000)))

		# Show Now Playing
		if self.RADIO_RUNNING:
			text = create_text('Now Playing:', font_preferences, 24, self.HEADER_COLOR)
			drawing_list.append((text, (1500,60)))
			description = ['Artist:   ','Song:    ','Album:   ','Station:  ']
			now_playing_list = get_song_data()
			if len(now_playing_list) == 4:
				for index, item in enumerate(now_playing_list):
					text = create_text(description[index]+item, header_font, 24, self.CONTENT_COLOR)
					drawing_list.append((text, (1520, 90+28*index)))
			else:
				print ('now playing list did not update properly.  We\'ll get \'em next time')
		else: 
		#print a message
			text = create_text('To start radio, type CTRL-M', font_preferences, 24, self.HEADER_COLOR)
			drawing_list.append((text, (1600, 100)))
		return drawing_list

	def run(self):
		while not self.done:
			self.screen.fill(self.BG_COLOR)
			self.event_loop()	# check for outside input
			drawing_list = self.update_text()
			self.all_sprites_list.update() # move all the clouds
			self.all_sprites_list.draw(self.screen)
			self.draw_text(drawing_list) # draw text
			pg.display.update()
			self.clock.tick(self.fps)
			#print ("fps: ", self.clock.get_fps())
			

	def create_sprites(self):
		self.day_clouds = Cloud.create_clouds(10, self.DAYGFX)
		self.night_clouds = Cloud.create_clouds(10, self.NTGFX)
		self.all_sprites_list.add(self.day_clouds, self.night_clouds)
		#print(self.all_sprites_list)

def load_gfx(directory,colorkey=(0,0,0),accept=(".png",".jpg",".bmp")):
    """Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def display_time_until(event):
	et = dateutil.parser.parse(event[0])
	ct = dateutil.parser.parse(datetime.now().isoformat()).replace(microsecond=0)
	return str((et-ct))

def display_time_remaining(event):
	et = dateutil.parser.parse(event[1])
	ct = dateutil.parser.parse(datetime.now().isoformat()).replace(microsecond=0)
	return str((et-ct))
			
def update_event_lists(filename):
	''' the function takes a file as an argument 
	and returns the current and upcoming event lists '''
	content = readfile(filename)
	curr_evts = []
	future_evts = []
	curr_time = datetime.now().isoformat()
	for line in content:
		text = parse_line(line)
		start_time,end_time,event = text[0],text[1],text[2]
		the_event = (start_time,end_time,event)
		if curr_time > start_time and curr_time < end_time:
			curr_evts.append(the_event)
		if curr_time < start_time:
			future_evts.append(the_event)
	return curr_evts,future_evts


	

def main():
	pg.init()
	pg.mouse.set_visible(False) # hide the pointer
	screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN) # windows
	#screen = pg.display.set_mode((1920, 1080), pg.NOFRAME) # linux
	game = Game(screen)
	game.create_sprites()
	game.update_calendar()
	game.update_weather()
	game.change_state()
	game.run()
	exit(0)

if __name__ == '__main__':
	main()
