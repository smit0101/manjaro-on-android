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

"""Manjaro-Mirrors File Functions"""

import datetime
import os
import sys

import pacman_mirrors.functions.util
from pacman_mirrors.constants import colors as color
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import util


def check_file(filename: str, folder: bool = False) -> bool:
    """
    Check existence of named file
    :param filename:
    :param folder:
    :returns bool if existing
    """
    if folder:
        return os.path.isdir(filename)
    return os.path.isfile(filename)


def create_dir(foldername: str) -> None:
    """
    Create named folder if not exist
    :param foldername:
    """
    os.makedirs(foldername, mode=0o755, exist_ok=True)


def delete_file(filename: str) -> None:
    """
    Delete the named file if exist
    :param filename:
    :return:
    """
    if os.path.isfile(filename):
        os.remove(filename)


def return_mirror_filename(config: object, tty: bool = False) -> tuple:
    """
    Find the mirror pool file
    :param config: config dictionary
    :param tty:
    :returns tuple with file and status
    """
    filename = ""
    status = False  # status.json or mirrors.json
    # decision on file availablity
    if check_file(config["status_file"]):
        status = True
        filename = config["status_file"]
    elif check_file(filename=config["mirror_file"]):
        filename = config["mirror_file"]
    if not filename:
        util.msg(message=f"\n{txt.HOUSTON}\n", tty=tty, color=color.RED)
        sys.exit(3)
    return filename, status


def write_mirror_list(config: object, servers: list, tty: bool = False, custom: bool = False,
                      quiet: bool = False, interactive: bool = False) -> None:
    """
    Write servers to /etc/pacman.d/mirrorlist
    :param config: configuration dictionary
    :param servers: list of servers to write
    :param tty: flag
    :param custom: flag
    :param quiet: flag
    :param interactive: flag
    """
    try:
        with open(config["mirror_list"], "w") as outfile:
            if not quiet:
                util.msg(message=f"{txt.WRITING_MIRROR_LIST}", urgency=txt.INF_CLR, tty=tty)
            # write list header
            write_mirrorlist_header(outfile, custom=custom)
            cols, lines = pacman_mirrors.functions.util.terminal_size()
            for server in servers:
                url = server["url"]
                protocol = server["protocols"][0]
                pos = url.find(":")
                server["url"] = f'{protocol}{url[pos:]}{config["branch"]}{config["repo_arch"]}'
                if server["resp_time"] == 99.99:
                    # do not write bad servers to mirrorlist
                    continue
                if interactive:
                    if not quiet:
                        message = f'{server["country"]:<15} : {server["url"]}'
                        util.msg(message=f"{message:.{cols}}", tty=tty)
                        # print()
                else:
                    msg_url = f'{protocol}{url[pos:]}{config["branch"]}'
                    if not quiet:
                        message = f'{server["country"]:<15} : {msg_url}'
                        util.msg(message=f"{message:.{cols}}", tty=tty)

                # write list entry
                write_mirrorlist_entry(outfile, server)
            if not quiet:
                util.msg(
                    message=f'{txt.MIRROR_LIST_SAVED}: {config["mirror_list"]}', urgency=txt.INF_CLR, tty=tty)
    except OSError as err:
        util.msg(message=f"{txt.CANNOT_WRITE_FILE}: {err.filename}: {err.strerror}", urgency=txt.ERR_CLR, tty=tty)

        sys.exit(2)


def read_mirror_file(filename: str) -> list:
    """
    Read content of named file - json data assumed
    :param filename:
    :returns: list of mirrors
    """
    return jsonFn.read_json_file(filename, dictionary=True)


def write_mirrorlist_header(handle: object, custom: bool = False) -> None:
    """
    Write mirrorlist header
    :param handle: handle to a file opened for writing
    :param custom: controls content of the header
    """
    # handle creation time in unicode
    # http://stackoverflow.com/questions/16034060/
    #  python3-datetime-datetime-strftime-failed-to-accept-utf-8-string-format
    generated_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    handle.write("##\n")
    if custom:
        handle.write(f"## Manjaro Linux {txt.MIRROR_LIST_CUSTOM_HEADER}\n"
                     f"## {txt.MIRROR_LIST_GENERATED_ON} {generated_timestamp}\n"
                     "##\n"
                     f"## {txt.PLEASE_USE} '{txt.MODIFY_CUSTOM}' {txt.MIRROR_LIST_CUSTOM_RESET}\n"
                     f"## {txt.PLEASE_USE} '{txt.RESET_ALL}' {txt.MIRROR_LIST_CUSTOM_RESET}\n"
                     f"## {txt.REMOVE_CUSTOM_CONFIG} '{txt.RESET_ALL}'\n")
    else:
        handle.write(f"## Manjaro Linux {txt.MIRROR_LIST_DEFAULT_HEADER}\n"
                     f"## {txt.MIRROR_LIST_GENERATED_ON} {generated_timestamp}\n"
                     "##\n"
                     f"## {txt.PLEASE_USE} '{txt.MODIFY_DEFAULT} [{txt.NUMBER}]' {txt.MIRROR_LIST_DEFAULT_MODIFY}\n"
                     f"## ({txt.USE_ZERO_FOR_ALL})\n")
    handle.write("##\n\n")


def write_mirrorlist_entry(handle: object, mirror: dict) -> None:
    """
    Write mirror to mirror list or file
    :param handle: handle to a file opened for writing
    :param mirror: mirror object
    """
    workitem = mirror
    handle.write(f'## Country : {workitem["country"]}\n')
    handle.write(f'Server = {workitem["url"]}\n\n')
