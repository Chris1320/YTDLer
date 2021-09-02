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
import typer
import traceback

from core import api
from core import info
from core import ytdl

cmd_api = typer.Typer()

_debug = False
_simulate = False
_no_overwrites = False
url_list = {}  # Format: <url>: [<download_type>, [<options>]]


def main(logger):
    """
    The main function of cmd_handler.py

    :param class logger: The logger class.
    """

    logger.info("Setting up function and calling typer...")

    def parse_commands(
        url: str = typer.Argument(
            None,
            help="The YouTube URL or a file containing YouTube URLs separated by a comma.",
            show_default=False
        ),
        video: bool = typer.Option(
            False,
            "--video",
            "-v",
            help="Download video with audio. (Audio not downloaded when --no-audio is True.)",
            show_default=False
        ),
        audio: bool = typer.Option(
            False,
            "--audio",
            "-a",
            help="Download audio only.",
            show_default=False
        ),
        no_subs: bool = typer.Option(
            False,
            "--no-subs",
            help="Do not download video subtitles/audio lyrics.",
            show_default=False
        ),
        no_audio: bool = typer.Option(
            False,
            "--no-audio",
            help="Do not download audio (Only when `-v` is True.)",
            show_default=False
        ),
        quality_override: bool = typer.Option(
            False,
            "--quality",
            "-q",
            help="Show quality options list.",
            show_default=False
        ),
        debug: bool = typer.Option(
            False,
            "--debug",
            help="Show variable values when downloading.",
            show_default=False
        ),
        simulate: bool = typer.Option(
            False,
            "--simulate",
            help="Do not download the video files.",
            show_default=False
        )
    ):
        try:
            error_code = ytdl.Main(
                url=url,
                video=video,
                audio=audio,
                no_subs=no_subs,
                no_audio=no_audio,
                quality_override=quality_override,
                debug=debug,
                simulate=simulate,
                logger=logger
            ).main()

        except KeyboardInterrupt:
            print("[!] CTRL+C detected, forcing to quit...")
            logger.critical("CTRL+C detected, forcing to quit...")
            error_code = 6

        except Exception as e:
            print("[CRITICAL] An unknown error occured:\n", e)
            logger.critical("An unknown error occured:")
            logger.critical(e)
            logger.debug('\n' + str(traceback.format_exc()))
            error_code = 5

        logger.info(f"Returned with error code {error_code}.")
        typer.Exit(error_code)

    print()
    print(info.title)
    print()
    print("Session ID:", logger.session_id)
    print()
    typer.run(parse_commands)
