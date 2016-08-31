#!/bin/bash

# create variables
while read L; do
	k="`echo "$L" | cut -d '=' -f 1`"
	v="`echo "$L" | cut -d '=' -f 2`"
	export "$k=$v"
done < <(grep -e '^\(title\|artist\|album\|stationName\|songStationName\|pRet\|pRetStr\|wRet\|wRetStr\|songDuration\|songPlayed\|rating\|coverArt\|stationCount\|station[0-9]*\)=' /dev/stdin) # don't overwrite $1...

case "$1" in 
	songstart)
		rm ~/.config/pianobar/scripts/out
		rm ~/.config/pianobar/scripts/coverart
		#rm ~/.config/pianobar/scripts/stations
		echo -e "$title\n$artist\n$album\n$stationName" >> ~/.config/pianobar/scripts/out
				echo "$artist / $title / $album / $stationName" >> ~/.config/pianobar/nowplaying
				echo -e "$coverArt" >> ~/.config/pianobar/scripts/coverart
				rm ~/.config/pianobar/scripts/stationlist
				for stnum in $(seq 0 $(($stationCount-1))); do
						#echo "$stnum) "$(eval "echo \$station$stnum") >> ~/.config/pianobar/scripts/stationlist
						echo $(eval "echo \$station$stnum") >> ~/.config/pianobar/scripts/stationlist
						done

esac

