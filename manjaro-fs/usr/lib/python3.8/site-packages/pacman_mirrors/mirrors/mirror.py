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


"""Pacman-Mirrors Mirror Class Module"""

from pacman_mirrors.constants import txt
from pacman_mirrors.functions.pools import get_continent


class Mirror:
    """Mirror Class"""

    def __init__(self):
        self.country_pool = []
        self.mirror_pool = []

    def add(self, country: str, url: str, protocols: list,
            branches: list = None, last_sync: str = None,
            resp_time: str = None) -> None:
        """Append mirror
        :param country:
        :param url:
        :param protocols:
        :param branches: optional from status.json
        :param last_sync: optional from status.json
        :param resp_time: optional from status.json
        """
        if branches is None:
            branches = [-1, -1, -1]
        if last_sync is None:
            last_sync = "00:00"
        if resp_time is None:
            resp_time = 0
        else:
            resp_time = dec(resp_time)
        if country not in self.country_pool:
            self.country_pool.append(country)
        # translate negative integer in status.json
        if last_sync == -1:
            last_sync = txt.SERVER_BAD  # "9999:99"
            resp_time = txt.SERVER_RES  # 99.99
        # sort protocols in reversed order https,http,ftps,ftp
        protocols = sorted(protocols, reverse=True)
        continent = get_continent(country.replace("_", " "))
        # add to pool
        self.mirror_pool.append({
            "continent": continent,
            "branches": branches,
            "country": country,
            "last_sync": last_sync,
            "protocols": protocols,
            "resp_time": resp_time,
            "url": url
        })

    def seed(self, servers: list, status: bool = False, custom: bool = False) -> None:
        """
        Seed mirrorlist
        :param servers:
        :param status:
        :param custom:
        """
        if custom:  # clear previous data
            self.country_pool = []
            self.mirror_pool = []
        for server in servers:
            if status:
                self.add(server["country"],
                         server["url"],
                         server["protocols"],
                         server["branches"],
                         server["last_sync"])
            else:
                self.add(server["country"],
                         server["url"],
                         server["protocols"])
