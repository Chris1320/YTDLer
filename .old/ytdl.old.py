# NOTE: This is the old script I use.

import os
import sys
import subprocess

print("NOTE: DO NOT ENTER PLAYLIST LINKS!")

if "--no-subs" in sys.argv:
    no_subs = True

else:
    no_subs = False

print("--no-subs: {0}".format(no_subs))

url = str(input("Enter YouTube URL: ")).partition('&')[0]

code_list = subprocess.getstatusoutput(f"youtube-dl -F {url}")[1]

video_list = "{0}\n".format(code_list.split('\n')[0])
audio_list = "{0}\n".format(code_list.split('\n')[0])

for line in code_list.split('\n'):
    if "audio only" in line:
        audio_list += f"{line}\n"

    else:
        video_list += f"{line}\n"

print()
print(video_list)
print()
while True:
    video_code = str(input("Enter video code: "))
    for line in code_list.split('\n'):
        if line.startswith(video_code):
            if "mp4" in line:
                video_format = "mp4"

            elif "webm" in line:
                video_format = "webm"

            else:
                video_format = str(input("Enter video extension: "))

    try:
        int(video_code)

    except TypeError:
        continue

    else:
        break

print()
print(audio_list)
print()
while True:
    audio_code = str(input("Enter audio code: "))
    for line in code_list.split('\n'):
        if line.startswith(audio_code):
            if "m4a" in line:
                audio_format = "m4a"

            elif "webm" in line:
                audio_format = "webm"

            else:
                audio_format = str(input("Enter audio extension: "))

    try:
        int(audio_code)

    except TypeError:
        continue

    else:
        break

print()
print("Downloading...")
print()
while True:
    if subprocess.call(("youtube-dl", "-f", video_code, url)) == 0:
        break

    else:
        print("Retrying...")
        continue

while True:
    if subprocess.call(("youtube-dl", "-f", audio_code, url)) == 0:
        break

    else:
        print("Retrying...")
        continue

filename = subprocess.getstatusoutput(("youtube-dl", "--get-filename", url))[1][::-1].partition('.')[2][::-1]

if subprocess.call(
    (
        "ffmpeg",
        "-i",
        f"{filename}.{video_format}",
        "-i",
        f"{filename}.{audio_format}",
        "-c",
        "copy",
        f"{filename}.mkv"
    )
) == 0:
    print("Finished!")

else:
    print("Failed.")
    print(f"ffmpeg -i {filename}.{video_format} -i {filename}.{audio_format} -c copy {filename}.mkv")
    print()
    print('ffmpeg -i "<name>.<ext>" -i "<name>.<ext>" -c copy "<name>.mkv"')

if not no_subs:
    print("Downloading subtitles...")
    if subprocess.call(("youtube-dl", "--all-subs", "--skip-download", url)) == 0:
        print("Subtitle downloaded.")

    else:
        print("Failed to download subtitles.")

else:
    print("Subtitles not downloaded due to --no-subs switch.")

os.remove(f"{filename}.{video_format}")
os.remove(f"{filename}.{audio_format}")
