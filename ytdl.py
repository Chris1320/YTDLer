import os
import sys
import time
import random
import logging
import traceback

from datetime import timedelta

import youtube_dl


class Settings():
    """
    This class contains the variables that you can change.
    """

    config = {
        "downloads_path": "downloads",  # The path where completed files are moved.
        "temp_dl_path": ".temp",  # The temporary directory where files will be downloaded.
        "logfile": "ytdl.log",  # Where to write the logs.
        "ffmpeg_path": "ffmpeg"  # The path of the ffmpeg executable.
    }


# ? From Chris1320's ASCIIGraphs project.
class ASCIIGraphs():
    """
    The class for creating graphs, splashes,
    animations, and progress bars.
    """

    def __init__(self):
        """
        Initialization method of ASCIIGraphs() class.
        """

        self.VERSION = "0.0.1.0"

    def progress_bar(self, length, description='Loading...', progress_bar_length=20):
        """
        Print progress bar while waiting for a specified time.

        :param float length: How long the progress bar will show up.
        :param str description: The description of the loading screen.
        :param int progress_bar_length: The length of the progress bar.

        :returns None:
        """

        length = float(length)
        start = time.time()
        end = start + length
        iteration_counter = 0
        while True:
            iteration_counter = end - time.time()
            total_items = length
            percent = float(iteration_counter) / total_items
            spaces = ' ' * int(round(percent * progress_bar_length))
            hashes = '#' * (progress_bar_length - len(spaces))
            per = int(100 - round(percent * 100))
            if per > 100:
                per = 100

            sys.stdout.write("\r{0} [{1}] {2}%".format(description, hashes + spaces, per))
            sys.stdout.flush()
            if int(100 - round(percent * 100)) >= 100:
                print('\r')
                if length > 1:
                    time.sleep(1)

                else:
                    time.sleep(length)

                break

            else:
                if length > 1:
                    time.sleep(1)

                else:
                    time.sleep(length)

                continue

    def progress_bar_manual(self, description='Loading...', iteration_counter=0, total_items=100, progress_bar_length=20):
        """
        Print progress bar manually.

        :param str description: Description of the loading screen.
        :param int iteration_counter: Incremental counter
        :param int total_items: total number items
        :param int progress_bar_length: Progress bar length

        :returns None:
        """

        percent = float(iteration_counter) / total_items
        hashes = '#' * int(round(percent * progress_bar_length))
        spaces = ' ' * (progress_bar_length - len(hashes))
        sys.stdout.write("\r{0} [{1}] {2}%".format(description, hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()
        if total_items == iteration_counter:
            print("\r")

    def animated_loading_screen(self, length, description='Loading...', animation='loading', delay=0.15):
        """
        Print an animated loading screen while waiting for a specified time.

        :param float length: How long the loading screen will show up.
        :param str description: Message in the loading screen.
        :param str animation: Animation to use. (Can either be `loading` or `swapcase`)
        :param float delay: Delay on each frame.

        :returns None:
        """

        if animation.lower() == 'loading':
            length = float(time.time()) + float(length)
            splashes = ['-', '\\', '|', '/']
            iterator = 0
            while time.time() < length:
                sys.stdout.write("\r{0} {1}".format(description, splashes[iterator]))
                sys.stdout.flush()
                iterator += 1
                if iterator > 3 or iterator < 0:
                    iterator = 0

                time.sleep(delay)

            sys.stdout.write('\r{0}{1}'.format(description, '  '))
            sys.stdout.flush()
            print('\r')

            return None

        elif animation.lower() == 'swapcase':
            length = float(time.time()) + float(length)
            characters = list(description)
            iterator = 0
            while time.time() < length:
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                desc = ''
                for character in characters:
                    desc += character

                sys.stdout.write("\r{0}".format(desc))
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                iterator += 1
                if iterator > (len(characters) - 1):
                    iterator = 0

                time.sleep(delay)

            sys.stdout.write('\r{0}{1}'.format(description, '  '))
            sys.stdout.flush()
            print('\r')

            return None

        else:
            print("[i] Unknown animation `{0}`!".format(animation))
            return None

    def animated_loading_screen_manual(self, last_load=False, description='Loading...', animation='loading', delay=0.15):
        r"""
        Print an animated loading screen.

        :param bool last_load: If True, print a \r in the screen, which means the end of the loading.
        :param str description: Message in the loading screen.
        :param str animation: Animation to use. (Either `loading` or `swapcase`)
        :param float delay: Length of each animation to play.

        :returns None:
        """

        if animation.lower() == 'loading':
            splashes = ['-', '\\', '|', '/']
            iterator = 0
            while not iterator >= (len(splashes) - 1):
                sys.stdout.write("\r{0} {1}".format(description, splashes[iterator]))
                sys.stdout.flush()
                iterator += 1
                if iterator > 3 or iterator < 0:
                    iterator = 0

                time.sleep(delay)

            if last_load is True:
                sys.stdout.write('\r{0}{1}'.format(description, '  '))
                sys.stdout.flush()
                print('\r')
                return None

            else:
                return None

        elif animation.lower() == 'swapcase':
            characters = list(description)
            iterator = 0
            while True:
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                desc = ''
                for character in characters:
                    desc += character

                sys.stdout.write("\r{0}".format(desc))
                if characters[iterator].isupper():
                    characters[iterator] = characters[iterator].lower()

                elif characters[iterator].islower():
                    characters[iterator] = characters[iterator].upper()

                else:
                    pass

                iterator += 1
                if iterator > (len(characters) - 1):
                    break

                time.sleep(delay / (len(characters) - 1))

            if last_load is True:
                sys.stdout.write('\r{0}{1}'.format(description, '  '))
                sys.stdout.flush()
                print('\r')

            return None

        else:
            print("[i] Unknown animation `{0}`!".format(animation))
            return None


# ? From Chris1320's SimpleLogger-python project.
class LoggingObject(object):
    """
    The main class of Logger.
    """

    def __init__(self, **kwargs):
        """
        Initialization method of the logging object.

        :**kwargs str name: Name of the logging object.
        :**kwargs int session_id: Session ID of the logging object.
        :**kwargs str logfile: Path of logfile to write data into.
        :**kwargs tuple funcs: A list/tuple of function objects that
                               accepts the following kwargs:
            - name
            - session_id
            - logfile
            - message
            - mtype
                               The functions in the list are called
                               after logging the messages.
        """

        self.VERSION = [0, 0, 1, 2]

        # Set the name of the logger.
        self.name = kwargs.get('name', __name__)

        # Set the session ID of the logger.
        rand_id = random.randint(100000, 999999)
        self.session_id = kwargs.get('session_id', rand_id)
        del rand_id

        # Set the path of the logfile to write data into.
        self.logfile = kwargs.get('logfile', None)

        # Initialize the main logging object.
        self.logger = logging.getLogger(self.name)

        # Set the logging level.
        self.level = None

        # Set the value of print_logs
        self.print_logs = False

        # Set the time when the logger has started.
        self.start_time = time.asctime()

        # Set the current data
        self.log_datas = []  # All logs inf dict form {log_type:  message}
        self.log_data = ""  # Current/Latest log

        # Set the tuple of functions to call after
        self.afterlog_funcs = kwargs.get('funcs', ())

    def _write(self, message):
        """
        Write data into a logfile.

        :param str message: The message to write.

        :returns void:
        """

        # I didn't put a try/except block to let
        # the user to customize it.

        if self.logfile is None:
            return None

        else:
            with open(self.logfile, 'a', encoding="utf-8") as fopen:
                fopen.write(message)
                fopen.write('\n')

    def _format(self, message, logtype, caller):
        """
        Format the message into a more informative one.

        :param str message: Log message
        :param str logtype: The log message type.
        :param str caller: The name of the function that called the logger.

        :returns str: The newer version of the message.
        """

        if str(caller) == "<module>":
            pass

        else:
            caller = str(caller) + "()"

        result = ":{}: [{}] ({}) | {} | {}".format(
            logtype.upper(),
            str(self.session_id),
            time.strftime("%H:%M:%S %b %d %Y"),
            caller,
            message
        )

        # I put this here because I'm lazy doing another method.
        if self.print_logs is True:
            print(result)

        return result

    def get_all_log_datas(self):
        """
        Return the log data in a form of tuple in a list.

        :returns tuple: The log data in tuple in a list form.
        """

        return self.log_datas

    def get_log_data(self, log_number):
        """
        Get a specific log data.

        :param int log_number: The index number to get the data of log number.

        :returns str: Return the content of the specified log number.
        """

        return self.log_datas[log_number]

    def get_latest_log_data(self):
        """
        Return the last message recieved by logger.

        :returns str: The last message recieved by the logger.
        """

        return self.log_data

    def set_logging_level(self, level):
        """
        Set logging level.

        :returns void:
        """

        if level.upper() == "NOTSET":
            self.level = "NOTSET"

        elif level.upper() == "INFO":
            self.level = "INFO"

        elif level.upper() == "WARNING":
            self.level = "WARNING"

        elif level.upper() == "ERROR":
            self.level = "ERROR"

        elif level.upper() == "DEBUG":
            self.level = "DEBUG"

        elif level.upper() == "CRITICAL":
            self.level = "CRITICAL"

        else:
            raise ValueError("argument `level` must be `NOTSET`, `INFO`, `WARNING`, `ERROR`, `DEBUG`, or `CRITICAL`!")

    def enable_logging(self):
        """
        Show logging information.

        :returns void:
        """

        if self.level is None:
            raise self.LevelNotSetError("Logging level is not yet defined! Run `logger.LoggingObject().set_logging_level([LEVEL])` to set the level.")

        else:
            # logging.basicConfig(level=self.level)
            self.print_logs = True

    def _call_funcs(self, message, mtype):
        """
        Call the functions passed by the user.

        :param str message: The message to log.
        :param str mtype: The log message type.

        :returns void:
        """

        for function in self.afterlog_funcs:
            try:
                function(
                    name=self.name,
                    session_id=self.session_id,
                    logfile=self.logfile,
                    message=message,
                    mtype=mtype
                )

            except Exception:
                pass

    def info(self, message):
        """
        Log information.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'info', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'info'))
        self.log_data = (message, 'info')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'info')

    def warning(self, message):
        """
        Log warnings.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'warning', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'warning'))
        self.log_data = (message, 'warning')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'warning')

    def error(self, message):
        """
        Log errors.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'error', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'error'))
        self.log_data = (message, 'error')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'error')

    def debug(self, message):
        """
        Log debugging information.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'debug', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'debug'))
        self.log_data = (message, 'debug')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'debug')

    def critical(self, message):
        """
        Log critical errors.

        :param message: Log message.

        :returns void:
        """

        message = self._format(message, 'critical', sys._getframe(1).f_code.co_name)
        self.log_datas.append((message, 'critical'))
        self.log_data = (message, 'critical')
        self.logger.info(message)
        self._write(message)
        self._call_funcs(message, 'critical')

    class LevelNotSetError(Exception):
        """
        An exception class.
        """

        pass


class SettingsHandler():
    """
    This class helps other classes access values from Settings() class.
    """

    def get(self, key: str):
        """
        Get <key> from Settings().config.

        :param str key: The key to get.

        :returns obj: The value of the key.
        """

        return Settings().config.get(key)


class YTDLHook():
    """
    YouTuble-DL Hook.
    """

    def __init__(self, logger):
        """
        The initialization method of YTDLHook() class.

        :param class logger: The logger object.
        """

        self.logger = logger
        self.desc_length = 75   # Hardcoded TODO: Find a way to fix it without hardcoding anything (characters are not cleared in stdout when flushing)

    def size_converter(self, bytes_to_convert: int, divisor: int = 1024):
        """
        Automatically convert bytes into kilobytes/megabytes/etc.

        :param int bytes_to_convert: This is the float to be converted.
        :param int divisor: As far as I know, there are people who use 1000 instead of 1024 so I won't hardcode it.

        :returns tuple: The value and the unit. (B, KB, MB, GB, TB, PB)
        """

        try:
            result = bytes_to_convert / divisor

            # Check if need to convert KB to MB.
            if result > divisor:
                result = result / divisor
                # Check if need to convert MB to GB.
                if result > divisor:
                    result = result / divisor
                    # Check if need to convert GB to TB.
                    if result > divisor:
                        result = result / divisor
                        # Check if need to convert TB to PB.
                        if result > divisor:
                            # self.logger.info("Returning in `petabytes` form.")
                            return (round(result / divisor, 2), "PB")  # Let's make PB the largest unit we'll use.

                        else:
                            # self.logger.info("Returning in `terabytes` form.")
                            return (round(result, 2), "TB")

                    else:
                        # self.logger.info("Returning in `gigabytes` form.")
                        return (round(result, 2), "GB")

                else:
                    # self.logger.info("Returning in `megabytes` form.")
                    return (round(result, 2), "MB")

            else:
                # self.logger.info("Returning in `kilobytes` form.")
                return (round(result, 2), "KB")

        except ZeroDivisionError:
            # self.logger.info("Returning in `bytes` form.")
            return (0, "B")

    def downloading(self, d):
        """
        :param str d: The argument youtube_dl sends.
        """

        # self.logger.info("Hook called.")
        # self.logger.info("Setting t_size.")
        if d.get("total_bytes", None) is not None:
            # self.logger.info("t_size is d[\"total_bytes\"]")
            t_size = self.size_converter(d.get("total_bytes", None))
            percent_divisor = d.get("total_bytes", None)

        elif d.get("total_bytes_estimate", None) is not None:
            # self.logger.info("t_size is d[\"total_bytes_estimate\"]")
            t_size = self.size_converter(d.get("total_bytes_estimate", None))
            percent_divisor = d.get("total_bytes_estimate", None)

        else:
            # self.logger.info("t_size is NULL.")
            t_size = "---.--"
            percent_divisor = 0

        # self.logger.info("Setting dl_size.")
        dl_size = self.size_converter(d.get("downloaded_bytes", 0))
        percent_dividend = d.get("downloaded_bytes", 0)

        if d.get("eta", None) is not None:
            # self.logger.info("Setting ETA.")
            eta = str(timedelta(seconds=d.get("eta", 0)))

        else:
            # self.logger.info("Setting ETA. (ETA is N/A)")
            eta = "N/A"

        if d.get("speed", None) is not None:
            # self.logger.info("Setting speed.")
            speed_tmp = self.size_converter(d.get("speed", 0), 1000)  # Set it to 1000 because the unit is `bits` not `bytes`.
            speed = " | {0}{1}".format(speed_tmp[0], (speed_tmp[1].lower() + "ps"))

        else:
            # self.logger.info("speed is None.")
            speed = ""

        # self.logger.info("Setting percentage.")
        percentage = round((percent_dividend / percent_divisor) * 100, 1)

        # self.logger.info("Assembling description.")
        desc = f"[i] Downloaded: {dl_size[0]}{dl_size[1]}/{t_size[0]}{t_size[1]} ({percentage}%) [ETA: {eta}{speed}]"
        if len(desc) < self.desc_length:
            desc = desc + (' ' * (self.desc_length - len(desc)))

        # self.logger.debug(desc)

        self.logger.info("Calling ASCIIGraphs.")
        ASCIIGraphs().progress_bar_manual(desc, percentage, 100)

    def main(self, d):
        """
        The main method of YTDLHook() class.

        :param str d: The argument youtube_dl sends.
        """

        self.logger.info(f"Status is `{d['status']}`...")
        if d["status"] == "downloading":
            self.downloading(d)

        elif d["status"] == "error":
            pass

        elif d["status"] == "finished":
            print("[i] Post-processing...")

        else:
            self.logger.error("Unknown status recieved.")
            print("[!] Unkown status recieved: `{0}`".format(d["status"]))


class Downloader():
    """
    The class that handles youtube_dl calls.
    """

    def __init__(self, url: list, logger, debug: bool = False, simulate: bool = False):
        """
        The initialization method of Downloader() class.

        :param list url: A list of URLs of the YouTube videos/playlists to download.
        :param class logger: The logger class.
        :param bool debug: Debug mode.
        :param bool simulate: Do not download the video files.
        """

        self.url = url
        self.debug = debug
        self.download_path = SettingsHandler().get("downloads_path")
        self.logger = logger
        self.temp_dl_path = SettingsHandler().get("temp_dl_path")
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
                        }
                    ],
                    "progress_hooks": [YTDLHook(self.logger).main],
                    "verbose": self.debug,
                    "nooverwrites": no_overwrites,
                    "simulate": self.simulate,
                    "outtmpl": os.path.join(self.temp_dl_path, "%(title)s - %(id)s.%(ext)s")
                }

                if embed_subs:
                    ydl_opts["writesubtitles"] = True
                    ydl_opts["allsubtitles"] = True

                if no_audio:
                    ydl_opts["format"] = "bestvideo"

                else:
                    ydl_opts["format"] = "bestvideo+bestaudio"

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

        :param bool no_lyrics: Download subtitles? (I assume they're lyrics)
        :param bool quality_override: Override quality?
        :param bool no_overwrites: Avoid overwriting file if it already exists.

        :returns dict: A dictionary with three tuples (success, failed, and skipped) that contain strings of urls.
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
                            "preferredcodec": "mp3",
                            "preferredquality": "320"
                        },
                        {
                            "key": "FFmpegSubtitlesConvertor",
                            "format": "lrc"
                        }
                    ],
                    "logger": self.logger,
                    "verbose": self.debug,
                    "progress_hooks": [YTDLHook(self.logger).main],
                    "nooverwrites": no_overwrites,
                    "simulate": self.simulate,
                    "outtmpl": os.path.join(self.temp_dl_path, "%(title)s - %(id)s.%(ext)s")
                }

                if not no_lyrics:
                    ydl_opts["writesubtitles"] = True
                    ydl_opts["allsubtitles"] = True

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


class Main():
    """
    The main class of the module.
    """

    def __init__(self, args: list):
        """
        The initialization method of Main() class.
        """

        self.name = "YTDLer"
        self.versiont = (0, 2, 5)  # Version in tuple datatype.
        self.versions = '.'.join(map(lambda x: str(x), self.versiont))  # Version in string datatype.
        self.title = f"{self.name} v{self.versions}"

        self.args = args
        self.debug = False

        # Start the logger.

        self.logger = LoggingObject(
            name=self.name,
            logfile=SettingsHandler().get("logfile")
        )

        self.logger.info(f"{self.title} started on {time.asctime()}.")

    def parse_commands(self):
        """
        Parse self.args commands, if there are any.
        """

        i = 0  # iterator

        commands = {
            "download_mode": None,  # Possible values: "video, audio"
            "url": [],  # A list of YouTube URLs.
            "no_subs": False,  # Download subtitles? False to download.
            "quality_override": False,  # Show quality override settings?
            "no_audio": False,  # Do not download audio.
            "simulate": False
        }

        while i < len(self.args):
            arg = self.args[i]

            if arg in ("-h", "--help"):
                print("""
-u|--url <URL>        The YouTube URL or a file containing YouTube URLs.
-v|--video            Download video and audio.
-a|--audio            Download audio only.
--no-subs             Do not download video subtitles/audio lyrics.
--no-audio            Do not download audio (Only when `-v` is True.)
-q|--quality          Show quality options list.
--debug               Show variable values when downloading.
-s|--simulate         Do not download the video files.

NOTE: You can use multiple `--url` switches to download multiple videos/audio/playlists.
""")
                self.logger.info("Showing help menu.")
                return 0

            elif arg in ("-u", "--url"):
                self.logger.info("-u/--url detected.")
                try:
                    self.logger.info("Checking if argument is a file...")
                    if os.path.exists(self.args[i + 1]):
                        self.logger.info("argument is a file, getting its contents.")
                        with open(self.args[i + 1], 'r') as f:
                            for url in f.readlines():
                                if url == '':
                                    continue

                                elif url.startswith(('\n', '\r')):
                                    continue

                                self.logger.info("Adding a URL to url list.")
                                commands["url"].append(url.replace('\n', ''))

                    else:
                        commands["url"].append(self.args[i + 1])
                        self.logger.info("argument is not a file, added to url list.")

                except IndexError as e:
                    print(f"[ERROR] Usage: {self.args[0]} --url <URL>")
                    self.logger.error(f"IndexError: {e}")
                    return 3

                else:
                    self.logger.info(f"Incrementing `i` variable. ({i} += 1)")
                    i += 1  # Skip the switch argument.

            elif arg in ("-v", "--video"):
                self.logger.info("-v/--v detected.")
                if commands["download_mode"] is None:
                    self.logger.info("Setting download mode to `video`.")
                    commands["download_mode"] = "video"

                else:
                    self.logger.warning("download_mode is already set to `{0}`; Skipping --video switch.".format(commands["download_mode"]))
                    print("[i] download_mode is already set to `{0}`; Skipping --video switch.".format(commands["download_mode"]))

            elif arg in ("-a", "--audio"):
                self.logger.info("-a/--audio detected.")
                if commands["download_mode"] is None:
                    self.logger.info("Setting download mode to `audio`.")
                    commands["download_mode"] = "audio"

                else:
                    self.logger.warning("download_mode is already set to `{0}`; Skipping --audio switch.".format(commands["download_mode"]))
                    print("[i] download_mode is already set to `{0}`; Skipping --audio switch.".format(commands["download_mode"]))

            elif arg in ("--no-subs",):
                self.logger.info("--no-subs detected, Setting no_subs to True.")
                commands["no_subs"] = True

            elif arg in ("-q", "--quality"):
                self.logger.info("-q/--quality detected, setting quality override to True.")
                commands["quality_override"] = True

            elif arg in ("--no-audio",):
                self.logger.info("--no-audio detected, setting no_audio to True.")
                commands["no_audio"] = True

            elif arg in ("--debug",):
                self.debug = True
                self.logger.info("--debug detected, enabling debug mode.")

            elif arg in ("-s", "--simulate"):
                self.logger.info("-s/--simulate detected, Setting simulate to True.")
                commands["simulate"] = True

            elif arg == sys.argv[0]:
                pass

            else:
                print("[ERROR] Unknown argument `{0}`.".format(arg))
                return 2

            i += 1  # Iterate i

        self.logger.debug(commands)

        if commands["download_mode"] is None:
            self.logger.warning("No command recieved, exiting...")
            print("[i] No command recieved, exiting...")
            return 0

        elif commands["download_mode"] == "video":
            self.logger.info("Video download mode. Calling Downloader().video() method.")
            downloads = Downloader(
                commands["url"],
                logger=self.logger,
                debug=self.debug,
                simulate=commands["simulate"]
            ).video(
                not commands["no_subs"],
                commands["no_audio"],
                commands["quality_override"]
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

        elif commands["download_mode"] == "audio":
            self.logger.info("Audio download mode. Calling Downloader().audio() method.")
            downloads = Downloader(
                commands["url"],
                logger=self.logger,
                debug=self.debug
            ).audio(
                commands["no_subs"],
                commands["quality_override"]
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

    def main(self):
        """
        The main method of Main() class.

        :returns int: Error code.
        """

        print(self.title)
        print()
        print("Session ID:", self.logger.session_id)

        try:
            error_code = self.parse_commands()

        except KeyboardInterrupt:
            print("[!] CTRL+C detected, forcing to quit...")
            self.logger.critical("CTRL+C detected, forcing to quit...")
            error_code = 6

        except Exception as e:
            print("[CRITICAL] An unknown error occured:\n", e)
            self.logger.critical("An unknown error occured:")
            self.logger.critical(e)
            self.logger.debug('\n' + str(traceback.format_exc()))
            error_code = 5

        self.logger.info(f"Returned with error code {error_code}.")


if __name__ == "__main__":
    sys.exit(Main(sys.argv).main())
