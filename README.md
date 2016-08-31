# pygame-event-calendar-and-pianobar
A program I wrote in pygame for my Raspberry Pi 2 to display the kids' daily schedule on our living room television. 
It also acts as a Pandora jukebox by incorporating pianobar functionality.

In order to link the calendar, a Google Calendar API key and OAUTH authentication is required.  Instructions to obtain one can be found here:
  https://developers.google.com/google-apps/calendar/quickstart/python
  
My events_from_cal.py file is basically a modified version of this example to parse the data from the calendar that I wanted. 
One of the daily events in my google calendar is titled "Contributions" and the description contains everyone's contributions.

Another daily event is titled "Resting" and this will trigger changing the radio station to a relaxing pandora station of mine if the radio is running.

Fonts are included from the fonts.google.com library.

All (shoddy) artwork was created by me using Inkscape.

I've included the example scripts and config files I'm currently using for the pianobar installation on my pi in the misc folder.  
Username/Password and autostart stations will need to be adjusted accordingly

An openweathermap api key will be used for future integration
  
