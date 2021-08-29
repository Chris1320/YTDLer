# This is not needed anymore.

foreach ($wsong in Get-ChildItem -Include @("*.webm") -Recurse) {
ffmpeg -i "$wsong" -ab 320k "$wsong.mp3"}