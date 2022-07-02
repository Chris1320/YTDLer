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

import os
import traceback

import youtube_dl

from core import info
from core.hook import YTDLHook


class Downloader:
    """
    The class that handles youtube_dl calls.
    """

    def __init__(self, url: list, logger, download_path: str, temp_dl_path: str, debug: bool = False, simulate: bool = False, cookie_filepath: str | None = None):
        """
        The initialization method of Downloader() class.

        :param url: A list of URLs of the YouTube videos/playlists to download.
        :param logger: The logger class.
        :param debug: Debug mode.
        :param simulate: Do not download the video files.
        :param cookie_filepath: The filepath of the cookie file to use.
        """

        self.url = url
        self.debug = debug
        # Old method: self.download_path = SettingsHandler().get("downloads_path")
        self.download_path = download_path
        self.logger = logger
        self.temp_dl_path = temp_dl_path
        self.simulate = simulate
        self.cookie_filepath = cookie_filepath

    def video(self, embed_subs: bool = True, no_audio: bool = False, quality_override: bool = False, no_overwrites: bool = True):
        """
        Download video (with optional audio) from <self.url>.

        :param embed_subs: Embed the subtitles?
        :param no_audio: Download audio?
        :param quality_override: Override quality?
        :param no_overwrites: Avoid overwriting file if it already exists.

        :returns: A dictionary with 3 tuples (success, failed, and skipped) that contain tuples with two strings for urls and titles.
                       {"success": [(<url>, <title>)], "failed": [(<url>, <title>)], "skipped": [(<url>, <title>)]}
        """

        self.logger.info("Preparing to call youtube_dl...")
        result = {"success": [], "failed": [], "skipped": []}
        if quality_override:
            self.logger.error("quality_override is not yet supported.")
            print("[!] Not supported yet!")
            result["failed"] = map(lambda x: (x, "N/A"), self.url)
            return result

        else:
            self.logger.info(f"Downloading from {len(self.url)} URLs...")
            for url in self.url:
                self.logger.info("Setting YouTube-DL options.")
                ydl_opts = {
                    "logger": self.logger,
                    "postprocessors": [
                        {
                            "key": "FFmpegEmbedSubtitle"
                        },
                        {
                            "key": "FFmpegMetadata"
                        }
                    ],
                    "progress_hooks": [YTDLHook(self.logger).main],
                    "verbose": self.debug,
                    "nooverwrites": no_overwrites,
                    "simulate": self.simulate,
                    "debug_printtraffic": self.debug,
                    "outtmpl": os.path.join(self.temp_dl_path, "%(title)s - %(id)s.%(ext)s")
                }

                if embed_subs:
                    ydl_opts["writesubtitles"] = True
                    ydl_opts["allsubtitles"] = True

                if no_audio:
                    ydl_opts["format"] = "bestvideo"

                else:
                    ydl_opts["format"] = "bestvideo+bestaudio/best"

                if self.cookie_filepath is not None:
                    ydl_opts["cookiefile"] = self.cookie_filepath

                self.logger.info("Extracting URL info...")
                url_info = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download=False)

                print()
                print(f"[*] Downloading video `{url_info.get('title', 'N/A')}` (ID: {url_info.get('id', 'N/A')})")
                self.logger.info("Checking if file is already downloaded using its ID.")
                skip_url = False
                for f in os.listdir(self.download_path):
                    if url_info["id"] in f:
                        self.logger.warning("File is already downloaded. (ID detected on filename)")
                        print("[!] File is already downloaded.")
                        skip_url = True
                        break

                if skip_url:
                    self.logger.warning("Skipping URL since it is already downloaded.")
                    result["skipped"].append((url, url_info.get("title", "N/A")))
                    continue

                self.logger.info("Starting youtube_dl.")
                try:
                    if youtube_dl.YoutubeDL(ydl_opts).download([url]) == 0:
                        self.logger.info("Download success.")
                        result["success"].append((url, url_info.get("title", "N/A")))
                        # Get all files with the same name
                        matched_files = []
                        if not self.simulate:
                            self.logger.info("Checking files to move.")
                            for f in os.listdir(self.temp_dl_path):
                                if f"- {url_info['id']}" in f:
                                    matched_files.append(f)

                            self.logger.info(f"{len(matched_files)} files to move.")
                            for f in matched_files:
                                os.rename(os.path.join(self.temp_dl_path, f), os.path.join(self.download_path, f))

                        else:
                            self.logger.info("Simulation only, skipping file movement process.")

                    else:
                        self.logger.error("Download failed.")
                        result["failed"].append((url, url_info.get("title", "N/A")))

                except Exception as e:
                    print("[E] A YouTube-DL error occured:", e)
                    self.logger.error("A YouTube-DL error occured: {0}".format(e))
                    self.logger.debug('\n' + traceback.format_exc())
                    result["failed"].append((url, url_info.get("title", "N/A")))

            self.logger.info("Returning result...")
            return result

    def audio(self, no_lyrics: bool = False, quality_override: bool = False, no_overwrites: bool = True):
        """
        Download audio from <self.url>.

        :param no_lyrics: Download subtitles? (I assume they're lyrics)
        :param quality_override: Override quality?
        :param no_overwrites: Avoid overwriting file if it already exists.

        :returns: A dictionary with three tuples (success, failed, and skipped) that contain strings of urls.
        """

        self.logger.info("Preparing to call youtube_dl...")
        result = {"success": [], "failed": [], "skipped": []}
        if quality_override:
            self.logger.error("quality_override is not yet supported.")
            print("[!] Not supported yet!")
            result["failed"] = map(lambda x: (x, "N/A"), self.url)
            return result

        else:
            self.logger.info(f"Downloading from {len(self.url)} URLs...")
            for url in self.url:
                self.logger.info("Setting up YouTube-DL options.")
                ydl_opts = {
                    "format": "bestaudio",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3"
                        },
                        {
                            "key": "FFmpegSubtitlesConvertor",
                            "format": "lrc"
                        },
                        {
                            "key": "FFmpegMetadata"
                        }
                    ],
                    "logger": self.logger,
                    "verbose": self.debug,
                    "progress_hooks": [YTDLHook(self.logger).main],
                    "nooverwrites": no_overwrites,
                    "simulate": self.simulate,
                    "debug_printtraffic": self.debug,
                    "outtmpl": os.path.join(self.temp_dl_path, "%(title)s - %(id)s.%(ext)s")
                }

                if not no_lyrics:
                    ydl_opts["writesubtitles"] = True
                    ydl_opts["allsubtitles"] = True

                if self.cookie_filepath is not None:
                    ydl_opts["cookiefile"] = self.cookie_filepath

                self.logger.info("Fetching url information.")
                url_info = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download=False)

                print()
                print(f"[*] Downloading audio `{url_info.get('title', 'N/A')}` (ID: {url_info.get('id', 'N/A')})...")
                self.logger.info("Checking if file is already downloaded using its ID.")
                skip_url = False
                for f in os.listdir(self.download_path):
                    if url_info["id"] in f:
                        self.logger.warning("File is already downloaded. (ID detected on filename)")
                        print("[!] File is already downloaded.")
                        skip_url = True
                        break

                if skip_url:
                    self.logger.warning("Skipping URL since it is already downloaded.")
                    result["skipped"].append((url, url_info.get("title", "N/A")))
                    continue

                self.logger.info("Calling youtube_dl.")
                try:
                    if youtube_dl.YoutubeDL(ydl_opts).download([url]) == 0:
                        self.logger.info("Download success.")
                        result["success"].append((url, url_info.get("title", "N/A")))
                        # Get all files with the same name
                        matched_files = []
                        if not self.simulate:
                            self.logger.info("Checking files to move.")
                            for f in os.listdir(self.temp_dl_path):
                                if f"- {url_info['id']}" in f:
                                    matched_files.append(f)

                            self.logger.info(f"{len(matched_files)} files to move.")
                            for f in matched_files:
                                os.rename(os.path.join(self.temp_dl_path, f), os.path.join(self.download_path, f))

                            self.logger.info("Files moved.")

                        else:
                            self.logger.info("Simulation only, skipping file movement process.")

                    else:
                        result["failed"].append((url, url_info.get("title", "N/A")))

                except Exception as e:
                    print("[E] A YouTube-DL error occured:", e)
                    self.logger.error("A YouTube-DL error occured: {0}".format(e))
                    self.logger.debug('\n' + traceback.format_exc())
                    result["failed"].append((url, url_info.get("title", "N/A")))

            return result
