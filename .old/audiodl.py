# NOTE: This is the old script I use.

import os
import sys
import subprocess

audiodl_temp = ".audiodl.temp"


def check4urls(song: str):
    """
    Checks if <song> has <checks.items> in it.

    :param str song: The URL of the song.

    :returns bool:  True if there is atleast one item present in <song> from <checks>;
                    Otherwise, it returns False.
    """

    checks = (
        "youtube.com",
        "youtu.be",
        "soundcloud.com"
    )

    for check in checks:
        if check in song:
            return True

    return False


songs = []
success = []
failed = []

print("Paste YouTube URLs here or absolute/relative path to a file with URLs. When done, type `done`.")
while True:
    with open(audiodl_temp, 'w') as tempfile:
        song2add = str(input("URL/Filepath: "))
        if song2add.lower().startswith("done"):
            break

        if os.path.exists(song2add) and os.path.isfile(song2add):
            try:
                with open(song2add, 'r') as urlfile:
                    songs = urlfile.read().split('\n')

            except(FileNotFoundError):
                print("[ERROR] File doesn't exist.")
                sys.exit(1)

            except(IOError, PermissionError):
                print("[ERROR] Cannot read file; do we have permission?")
                sys.exit(1)

            else:
                print("File with URLs found!")
                print("Verifying URLs...")
                verified_urls_from_file = 0
                for _ in songs:
                    if check4urls(_):
                        verified_urls_from_file += 1

                print("Verified files from file: {0}".format(verified_urls_from_file))
                break

        songs.append(song2add)
        tempfile.write("{0}\n".format(song2add))

for song in songs:
    if check4urls(song):
        # youtube-dl -x --audio-format mp3 --audio-quality 320k --add-metadata <song>
        if subprocess.call(("youtube-dl", "-x", "--audio-format", "mp3", "--audio-quality", "320k", "--add-metadata", song)) == 0:
            success.append(song)

        else:
            failed.append(song)

        print()

    else:
        continue

print("FINISHED")
print()
print("Success:")
for song in success:
    print(song)
print()
print("Failed:")
for song in failed:
    print(song)

os.remove(audiodl_temp)
sys.exit(0)
