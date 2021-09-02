"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

# Program name
name = "YTDLer"

# Program version
version = {
    tuple: (0, 2, 6),  # Version in tuple datatype.
    str: None  # Will be populated after this dictionary declaration.
}
version[str] = '.'.join(map(lambda x: str(x), version[tuple]))  # Version in string datatype.

# Program title
title = f"{name} v{version[str]}"

# NOTE: Will be removed as it is unused.
help_menu = """
-u|--url <URL>        The YouTube URL or a file containing YouTube URLs.
-v|--video            Download video and audio.
-a|--audio            Download audio only.
--no-subs             Do not download video subtitles/audio lyrics.
--no-audio            Do not download audio (Only when `-v` is True.)
-q|--quality          Show quality options list.
--debug               Show variable values when downloading.
-s|--simulate         Do not download the video files.

NOTE: You can use multiple `--url` switches to download multiple videos/audio/playlists.
"""
