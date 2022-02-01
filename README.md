# YTDLer

A wrapper for YoutubeDL.

```plaintext
$ python ytdl.py --help
YTDLer v0.2.5

-u|--url \<URL\>        The YouTube URL or a file containing YouTube URLs.
-v|--video            Download video and audio.
-a|--audio            Download audio only.
--no-subs             Do not download video subtitles/audio lyrics.
--no-audio            Do not download audio (Only when `-v` is True.)
-q|--quality          Show quality options list.
--debug               Show variable values when downloading.
-s|--simulate         Do not download the video files.

NOTE: You can use multiple `--url` switches to download multiple videos/audio/playlists.
```

## Using Cookies

YTDLer checks if `cookies.txt` exists in the current directory. If it does, it will supply the file to youtube-dl.
