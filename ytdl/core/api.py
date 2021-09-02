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

from core import downloader
from core import default_logger


class Download():
    """
    The class the uses the downloader module.
    """

    def __init__(self, url: list, download_path: str, temp_dl_path: str, logger = None, debug: bool = False, simulate: bool = False):
        """
        The initialization method of Download() class.

        :param list url: A list of URLs of the YouTube videos/playlists to download.
        :param class logger: The logger class.
        :param bool debug: Debug mode.
        :param bool simulate: Do not download the video files.
        """

        self.url = url
        self.debug = debug
        self.download_path = download_path
        if logger is None:
            self.logger = default_logger.Logger()

        else:
            self.logger = logger

        self.temp_dl_path = temp_dl_path
        self.simulate = simulate

    def video(self, embed_subs: bool = True, no_audio: bool = False, quality_override: bool = False, no_overwrites: bool = True):
        """
        Download video (with optional audio) from <self.url>.

        :param bool embed_subs: Embed the subtitles?
        :param bool no_audio: Download audio?
        :param bool quality_override: Override quality?
        :param bool no_overwrites: Avoid overwriting file if it already exists.

        :returns dict: A dictionary with 3 tuples (success, failed, and skipped) that contain tuples with two strings for urls and titles.
                       {"success": [(<url>, <title>)], "failed": [(<url>, <title>)], "skipped": [(<url>, <title>)]}
        """

        return downloader.Downloader(
            url=self.url,
            logger=self.logger,
            download_path=self.download_path,
            temp_dl_path=self.temp_dl_path,
            debug=self.debug,
            simulate=self.simulate
        ).video(
            embed_subs=embed_subs,
            no_audio=no_audio,
            quality_override=quality_override,
            no_overwrites=no_overwrites
        )

    def audio(self, no_lyrics: bool = False, quality_override: bool = False, no_overwrites: bool = True):
        """
        Download audio from <self.url>.

        :param bool no_lyrics: Download subtitles? (I assume they're lyrics)
        :param bool quality_override: Override quality?
        :param bool no_overwrites: Avoid overwriting file if it already exists.

        :returns dict: A dictionary with three tuples (success, failed, and skipped) that contain strings of urls.
        """

        return downloader.Downloader(
            url=self.url,
            logger=self.logger,
            download_path=self.download_path,
            temp_dl_path=self.temp_dl_path,
            debug=self.debug,
            simulate=self.simulate
        ).audio(
            no_lyrics=no_lyrics,
            quality_override=quality_override,
            no_overwrites=no_overwrites
        )
