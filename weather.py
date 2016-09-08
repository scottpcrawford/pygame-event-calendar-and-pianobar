import pyowm 
from dateutil import tz
from datetime import datetime
from api_keys import open_weather_map_api_key
from file_parser import readfile, return_list
import json


owm = pyowm.OWM(open_weather_map_api_key)  # You MUST provide a valid API key

# Search current weather observations in the surroundings of 

class Weather(object):
	def __init__(self):
		self.station_name = 'Norfolk, VA'
		self.station_id = 4776222
		self.temperature = '60'
		self.cloud_cover = '0'
		self.wind = {}
		#self.wind_direction = '0'
		#self.wind_speed = '0'
		self.status = 'sunny'
		self.sunrise = ''
		self.sunset = ''
		self.humidity = ''
		self.observation = {}

	def get_weather_observation(self):
		weather_dict = {}
		observation = owm.weather_at_id(self.station_id)
		w = observation.get_weather()
		self.temperature = w.get_temperature('fahrenheit')['temp']
		self.status = w.get_detailed_status()
		self.wind = w.get_wind()
		#self.wind_direction = w.get_wind('deg')
		self.cloud_cover = w.get_clouds()
		#self.sunrise = w.get_sunrise_time()
		#datetime.fromtimestamp(my_unix_time).strftime('%Y-%m-%d %H:%M:%S')
		self.sunrise_time = w.get_sunrise_time()
		self.sunset_time = w.get_sunset_time()
		self.sunrise = self.convert_time(w.get_sunrise_time())
		self.sunset = self.convert_time(w.get_sunset_time())
		#self.sunset.convert_time(self.sunset)
		self.humidity = w.get_humidity()
		weather_dict = {'temperature': self.temperature, 'status': self.status, 'wind': self.wind, 'clouds': self.cloud_cover, 'sunrise': self.sunrise, 'sunset': self.sunset, 'humidity': self.humidity}
		return weather_dict

	def convert_time(self, my_time):
		return datetime.fromtimestamp(my_time) #.strftime('%H:%M') # format it in scheduler.py

	def write_file(self, my_dict):
		with open('weather.txt','w') as f:
			for k,v in my_dict.items():
				f.write(k+' : '+str(v)+'\n')

	def after_sunset(self, current_time):
		return current_time > datetime.fromtimestamp(self.sunset_time)

	def before_sunrise(self, current_time):
		return current_time < datetime.fromtimestamp(self.sunrise_time)




def main():
	
	weather = Weather()
	obs = weather.get_weather_observation()
	print('Norfolk, VA Weather:','\n','sunrise: ', obs['sunrise'],'\n','sunset: ', obs['sunset'],'\n','temp: ', obs['temperature'],u'\xb0F','\n', 'current: ', obs['status'].capitalize(), '\n', 'wind: ', obs['wind']['deg'],u'\xb0', 'at',obs['wind']['speed'], 'mph' )
	#observation = owm.weather_at_id(weather.station_id)
	#w = observation.get_weather()
	weather.write_file(obs)
	exit(0)

if __name__ == '__main__':
	main()

