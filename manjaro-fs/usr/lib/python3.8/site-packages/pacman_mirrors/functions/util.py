#!/usr/bin/env python
#
# This file is part of pacman-mirrors.
#
# pacman-mirrors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pacman-mirrors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pacman-mirrors.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Pacman-Mirrors Utility Functions"""


import platform
import shutil
from sys import stdout

from pacman_mirrors.api import apifn
from pacman_mirrors.constants import txt


def async_disclaimer() -> None:
    for line in txt.ASYNC_DISCLAIM:
        print(line)


def extract_mirror_url(data: str) -> str:
    """Extract mirror url from data"""
    line = data.strip()
    if line.startswith("Server"):
        return line[9:].replace("$branch/$repo/$arch", "")


def get_country(data: str) -> str:
    """Extract mirror country from data"""
    line = data.strip()
    if line.startswith("[") and line.endswith("]"):
        return line[1:-1]
    elif line.startswith("## Country") or line.startswith("## Location"):
        return line[19:]


def get_protocol(url: str) -> str:
    """Extract protocol from url"""
    pos = url.find(":")
    return url[:pos]


def get_protocol_from_url(url: str) -> str:
    """
    Splits an url
    :param url:
    :returns protocol eg. http
    """
    colon = url.find(":")
    if colon:
        return url[:colon]
    return url


def location_from_url(url: str) -> str:
    """
    Splits an url
    :param url:
    :returns url string without protocol
    """
    colon = url.find(":")
    if colon:
        return url[colon:]
    return url


def i686_check(self, write: bool = False) -> None:
    if platform.machine() == "i686":
        self.config["x32"] = True
        if "x32" not in self.config["branch"]:
            self.config["branch"] = "x32-{}".format(self.config["branch"])
            if write:
                apifn.write_config_branch(self.config["branch"], self.config["config_file"], quiet=True)


def aarch64_check(self, write: bool = False) -> None:
    if platform.machine() == "aarch64":
        self.config["arm"] = True
        if "arm" not in self.config["branch"]:
            self.config["branch"] = "arm-{}".format(self.config["branch"])
            if write:
                apifn.write_config_branch(self.config["branch"], self.config["config_file"], quiet=True)                


def internet_message(tty: bool = False) -> None:
    """Message when internet connection is down"""
    msg(f"{txt.INTERNET_DOWN}", urgency=txt.INF_CLR, tty=tty)
    msg(f"{txt.MIRROR_RANKING_NA}", urgency=txt.INF_CLR, tty=tty)
    msg(f"{txt.INTERNET_ALTERNATIVE}", urgency=txt.INF_CLR, tty=tty)


def msg(message: str, urgency: str = "", tty: bool = False, color: str = "", newline: bool = False) -> None:
    """Helper for printing messages
    :param message:
    :param urgency:
    :param tty:
    :param color:
    :param newline:
    """
    reset = "\033[1;m"
    if urgency and color:
        color = ""
    if tty:
        if newline:
            print("\n")
        print(f"::{message}")
    else:
        if urgency:
            if newline:
                print("\n")
            print(f"::{urgency} {message}")
        else:
            if newline:
                print("\n")
            print(f"::{color}{message}{reset}")


def strip_protocol(url: str) -> str:
    return url.split("//")[1]


def terminal_size() -> tuple:
    """get terminal size"""
    # http://www.programcreek.com/python/example/85471/shutil.get_terminal_size
    cols = shutil.get_terminal_size().columns
    lines = shutil.get_terminal_size().lines
    result = (cols, lines)
    return result
