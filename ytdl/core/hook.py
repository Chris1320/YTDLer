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

import sys
from datetime import timedelta

from core import info


class YTDLHook:
    """
    YouTube-DL Hook.
    """

    def __init__(self, logger):
        """
        The initialization method of YTDLHook() class.

        :param logger: The logger object.
        """

        self.logger = logger

    def size_converter(self, bytes_to_convert: int, divisor: int = 1024) -> tuple[float, str]:
        """
        Automatically convert bytes into kilobytes/megabytes/etc.

        :param bytes_to_convert: This is the float to be converted.
        :param divisor: As far as I know, there are people who use 1000 instead of 1024 so I won't hardcode it.

        :returns: The value and the unit. (B, KB, MB, GB, TB, PB)
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
                            self.logger.debug("Returning in `petabytes` form.")
                            return (round(result / divisor, 2), "PB")  # Let's make PB the largest unit we'll use.

                        else:
                            self.logger.debug("Returning in `terabytes` form.")
                            return (round(result, 2), "TB")

                    else:
                        self.logger.debug("Returning in `gigabytes` form.")
                        return (round(result, 2), "GB")

                else:
                    self.logger.debug("Returning in `megabytes` form.")
                    return (round(result, 2), "MB")

            else:
                self.logger.debug("Returning in `kilobytes` form.")
                return (round(result, 2), "KB")

        except ZeroDivisionError:
            self.logger.debug("Returning in `bytes` form.")
            return (0, "B")

    def downloading(self, d) -> None:
        """
        :param d: The argument youtube_dl sends.
        """

        self.logger.debug("Hook called.")
        self.logger.debug("Setting t_size.")
        if d.get("total_bytes", None) is not None:
            self.logger.debug("t_size is d[\"total_bytes\"]")
            t_size = self.size_converter(d.get("total_bytes", None))
            percent_divisor = d.get("total_bytes", None)

        elif d.get("total_bytes_estimate", None) is not None:
            self.logger.debug("t_size is d[\"total_bytes_estimate\"]")
            t_size = self.size_converter(d.get("total_bytes_estimate", None))
            percent_divisor = d.get("total_bytes_estimate", None)

        else:
            self.logger.debug("t_size is NULL.")
            t_size = "---.--"
            percent_divisor = 0

        self.logger.debug("Setting dl_size.")
        dl_size = self.size_converter(d.get("downloaded_bytes", 0))
        percent_dividend = d.get("downloaded_bytes", 0)

        if d.get("eta", None) is not None:
            self.logger.debug("Setting ETA.")
            eta = str(timedelta(seconds=d.get("eta", 0)))

        else:
            self.logger.debug("Setting ETA. (ETA is N/A)")
            eta = "N/A"

        if d.get("speed", None) is not None:
            self.logger.debug("Setting speed.")
            speed_tmp = self.size_converter(d.get("speed", 0), 1000)  # Set it to 1000 because the unit is `bits` not `bytes`.
            speed = " | {0}{1}".format(speed_tmp[0], (speed_tmp[1].lower() + "ps"))

        else:
            self.logger.debug("speed is None.")
            speed = ""

        self.logger.debug("Setting percentage.")
        percentage = round((percent_dividend / percent_divisor) * 100, 1)

        self.logger.debug("Assembling description.")
        desc = f"[i] Downloaded: {dl_size[0]}{dl_size[1]}/{t_size[0]}{t_size[1]} ({percentage}%) [ETA: {eta}{speed}]"
        if len(desc) < info.max_desc_length:
            desc = desc + (' ' * (info.max_desc_length - len(desc)))

        self.logger.debug(desc)
        sys.stdout.write(f"\r{desc}")
        sys.stdout.flush()

    def main(self, d: dict):
        """
        The main method of YTDLHook() class.

        :param d: The argument youtube_dl sends.
        """

        self.logger.debug(f"Status is `{d['status']}`...")
        if d["status"] == "downloading":
            self.downloading(d)

        elif d["status"] == "error":
            pass

        elif d["status"] == "finished":
            print("[i] Post-processing...")

        else:
            self.logger.debug(f"Unknown status recieved: {d['status']}")
            print("[!] Unkown status recieved: `{0}`".format(d["status"]))
