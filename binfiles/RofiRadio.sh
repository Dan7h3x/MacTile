#!/usr/bin/env bash
#
#
STATIONS_FILE="/home/mehdi/.config/rofi/stations.json"
THEME="$HOME/.config/rofi/launcher.rasi"
notify() {
	dunstify -u low -t 3000 "$1" "$2"
}

play() {
	station_url=$(jq -r ".[] | select(.name==\"$1\") | .url" "$STATIONS_FILE")

	if [ -z "$station_url" ]; then
		notify "Error" "Station '$1' not found"
		exit 1
	fi

	mpv "$station_url"
}

add() {
	rofi -dmenu -p "Enter station name and URL (e.g., Radio XYZ;http://example.com/radio-xyz)" -theme "$THEME" | while read -ra station_info; do
		echo "{\"name\":\"${station_info[0]}\",\"url\":\"${station_info[1]}\"}" | jq -r '.' >>"$STATIONS_FILE"
		notify "Success" "Station '${station_info[0]}' added"
	done
}

show() {
	jq -r '.[].name' "$STATIONS_FILE" | rofi -dmenu -p "Select station" -theme "$THEME" | while read -r station; do
		play "$station"
	done
}

opts=("Play Radio" "Add Station" "Exit")

while true; do
	option=$(printf "%s\n" "${opts[@]}" | rofi -dmenu -p "Radios" -theme "$THEME")
	case $option in
	"Play Radio")
		show
		;;
	"Add Station")
		add
		;;
	"Exit")
		exit 0
		;;
	*)
		notify "Error" "Invalid option"
		exit 1
		;;
	esac
done
