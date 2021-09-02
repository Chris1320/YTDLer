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

from core import api


class Main():
    def __init__(
        self,
        url: str,
        video: bool,
        audio: bool,
        no_subs: bool,
        no_audio: bool,
        quality_override: bool,
        debug: bool,
        simulate: bool,
        logger
    ):
        self.url = url
        self.video = video
        self.audio = audio
        self.no_subs = no_subs
        self.no_audio = no_audio
        self.quality_override = quality_override
        self.debug = debug
        self.simulate = simulate
        self.logger.logger

    def main(self):
        if ',' in self.url:
            url = self.url.split(',')

        else:
            url = [self.url]

        url_list = []
        self.logger.info("Checking if argument is a file...")
        for i in url:
            if os.path.exists(i):
                self.logger.info("argument is a file, getting its contents.")
                with open(i, 'r') as f:
                    for url in f.readlines():
                        if url == '':
                            continue

                        elif url.startswith(('\n', '\r')):
                            continue

                        self.logger.info("Adding a URL to url list.")
                        url_list.append(url.replace('\n', ''))

        else:
            url_list.append(i)
            self.logger.info("argument is not a file, added to url list.")

        if self.debug:
            print("[i] Debug mode is on.")
            print()
            print("url:", url_list)
            print("video:", self.video)
            print("audio:", self.audio)
            print("no_subs:", self.no_subs)
            print("no_audio:", self.no_audio)
            print("quality:", self.quality)
            print("debug:", self.debug)
            print("simulate:", self.simulate)
            print()
            self.logger.debug(
                {
                    "url": url_list,
                    "video": self.video,
                    "audio": self.audio,
                    "no_subs": self.no_subs,
                    "no_audio": self.no_audio,
                    "quality": self.quality,
                    "debug": self.debug,
                    "simulate": self.simulate
                }
            )

        if self.video:
            self.logger.info("Video download mode. Calling api.Download().video() method.")
            downloads = api.Download(
                url=url_list,
                logger=self.logger,
                debug=self.debug,
                simulate=self.simulate
            ).video(
                not self.no_subs,
                self.no_audio,
                self.quality_override
            )
            self.logger.info("Downloads finished, printing results.")

            print()
            print("==================== Results ====================")
            if len(downloads["success"]) > 0:
                print()
                print("Completed downloads:")
                for url in downloads["success"]:
                    print("    +", url[0], f"({url[1]})")

            if len(downloads["failed"]) > 0:
                print()
                print("Failed downloads:")
                for url in downloads["failed"]:
                    print("    -", url[0], f"({url[1]})")

            if len(downloads["skipped"]) > 0:
                print()
                print("Skipped downloads:")
                for url in downloads["skipped"]:
                    print("    *", url[0], f"({url[1]})")

            print()
            print("=================================================")
            if len(downloads["failed"]) == 0:
                return 0

            else:
                return 4

        if self.audio:
            self.logger.info("Audio download mode. Calling api.Download().audio() method.")
            downloads = api.Download(
                url=url_list,
                logger=self.logger,
                debug=self.debug,
                simulate=self.simulate
            ).audio(
                self.no_subs,
                self.quality_override
            )

            self.logger.info("Downloads finished, printing results.")

            print()
            print("==================== Results ====================")
            if len(downloads["success"]) > 0:
                print()
                print("Completed downloads:")
                for url in downloads["success"]:
                    print("    +", url[0], f"({url[1]})")

            if len(downloads["failed"]) > 0:
                print()
                print("Failed downloads:")
                for url in downloads["failed"]:
                    print("    -", url[0], f"({url[1]})")

            if len(downloads["skipped"]) > 0:
                print()
                print("Skipped downloads:")
                for url in downloads["skipped"]:
                    print("    *", url[0], f"({url[1]})")

            print()
            print("=================================================")
            if len(downloads["failed"]) == 0:
                return 0

            else:
                return 4
