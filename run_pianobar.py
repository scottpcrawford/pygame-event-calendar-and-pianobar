import os, sys
from subprocess import Popen, PIPE
from file_parser import readfile

def start_pianobar(os_type):
	print('Pianobar starting')
	if os_type == 'linux':
		Popen('/usr/bin/pianobar', stdout=PIPE)
		#Popen(['lxterminal', '-e', '/usr/bin/pianobar'], stdout=PIPE)
	elif os_type == 'win32':
		print('sorry, Pianobar Music Player is not intalled on Windows')
	else:
		print('unrecognized OS')
	# start pianobar

def get_os():
	 os_type = sys.platform
	 return os_type

def quit_pianobar():
	print('Quitting Pianobar')
	#sys.exit()
	# quit pianobar

def process_input(key):
	os_type = get_os()
	if os_type == 'linux':
		try:
			with open('/home/pi/.config/pianobar/ctl', 'w') as fifo:
				fifo.write(key)
		except:
			print('failed to pass key on to fifo, my bad')
		if key == 'q':
			quit_pianobar()
	elif os_type == 'win32':
		print('key '+key+' pressed, but not passed on')
	else:
		print(os_type+' is unsupported by this application today.  I should fix that')   
	# send message to ~/.config/pianobar/ctl

def display_music_player():
	print('display pianobar player')
	# pygame data

def get_song_data():
	# get song details to display
	try:
		#path = '/home/pi/.config/pianobar/nowplaying' # linux
		path = os.getcwd()+'\\nowplaying' # windows
		np = readfile(path)
		now_playing = (np[len(np)-1])
		now_playing_list = now_playing.split(' / ')
		return now_playing_list
	except:
		print('couldn\'t get the now playing list. Returning a blank one instead')
		return ['Error','Couldn\'t', 'Get', 'Song Info']

def main():
	print('main loop')# do stuff
	print('getting environment...')
	os_type = get_os()
	print('Operating system is: '+os_type)
	start_pianobar(os_type)
	
	

if __name__ == '__main__':
	main()



