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

"""Pacman-Mirrors Converter Functions"""
import json

from pacman_mirrors.constants import txt
from pacman_mirrors.functions.util import \
    get_country, get_protocol, get_protocol_from_url, location_from_url


def translate_interactive_to_pool(selection: list, mirror_pool: list, tty: bool = False) -> tuple:
    """
    Translate the interactive selection back to mirror pool
    :param tty:
    :param selection: the custom mirror selection
    :param mirror_pool: the default mirror pool
    :return: tuple with custom mirror pool and mirrors for mirror list generation
    """
    custom_pool = []
    mirror_list = []

    for mirror in mirror_pool:
        location = location_from_url(mirror["url"])
        selected = (x for x in selection if location in x["url"])
        protocols = []
        for item in selected:
            protocols.append(get_protocol_from_url(item["url"]))
        if protocols:
            m = mirror
            m["protocols"] = protocols
            mirror_list.append(m)
            custom_pool.append(mirror)
    return custom_pool, mirror_list


def translate_pool_to_interactive(mirror_pool: list, tty: bool = False) -> list:
    """
    Translate mirror pool for interactive display
    :param tty:
    :param mirror_pool:
    :return: list of dictionaries
            {
                "country": "country_name",
                "resp_time": "m.sss",
                "last_sync": "HHh MMm",
                "url": "http://server/repo/"
            }
    """
    interactive_list = []
    for mirror in mirror_pool:
        try:
            _ = mirror_pool[0]
            last_sync = str(mirror["last_sync"]).split(":")
            mirror_url = location_from_url(mirror["url"])
            for idx, protocol in enumerate(mirror["protocols"]):
                interactive_list.append({
                    "country": mirror["country"],
                    "resp_time": str(mirror["resp_time"]),
                    "last_sync": f"{last_sync[0]}h {last_sync[1]}m",
                    "url": f"{protocol}{mirror_url}"
                })
        except (KeyError, IndexError):
            msg(
                message=f"{txt.HOUSTON}! {txt.MIRROR_POOL_EMPTY}!", urgency=txt.WRN_CLR, tty=tty)
            break
    return interactive_list


def list_to_tuple(list_data: list, named_tuple) -> list:
    """Comvert list to a list with named tuples
    :param list_data: the list to convert
    :param named_tuple: tuple list item converts to
    :return data: list of named tuples
    """
    tdata = json.dumps(list_data)
    data = json.loads(tdata, object_hook=lambda x: named_tuple(**x))
    return data


def rows_from_tuple(servers: list, join_string: str = " | ") -> list:
    """Generates equal formatted lines
    :param servers: named tuples
    :param join_string: string used to join tuple items
    :return lines: list of nicely formatted lines
    """
    rows = []
    if servers:

        # calculate max col width
        col_width = [max(len(text) for text in col) for col in zip(*servers)]
        # generate linies
        for line in servers:
            rows.append(join_string.join("{:{}}".format(text, col_width[i])
                                         for i, text in enumerate(line)))
    return rows
