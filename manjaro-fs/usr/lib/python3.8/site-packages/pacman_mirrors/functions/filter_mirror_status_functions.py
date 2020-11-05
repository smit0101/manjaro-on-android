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

"""Pacman-Mirrors Filter Functions"""

from pacman_mirrors.constants import txt

# from constats.txt.py
# MIRROR RELATED
# LASTSYNC_OK = "24:00"  # last syncronize in the past 24 hours
# LASTSYNC_NA = "9800:00"  # last syncronization not available
# SERVER_BAD = "9999:99"  # default last syncronization status
# SERVER_RES = 99.99  # default response status


def filter_bad_mirrors(mirror_pool: list) -> list:
    """
    Remove known bad mirrors with last_sync == "9999:99" (status.json -1)
    :param mirror_pool:
    :return: list with bad mirrors removed
    """
    result = []
    mirrors = (x for x in mirror_pool if x["resp_time"] != txt.SERVER_BAD)
    for mirror in mirrors:
        result.append(mirror)
    return result


def filter_error_mirrors(mirror_pool: list) -> list:
    """
    Remove mirrors with resp_time == 99.99
    :param mirror_pool:
    :return: list with error mirrors removed
    """
    result = []
    mirrors = (x for x in mirror_pool if x["resp_time"] != txt.SERVER_RES)
    for mirror in mirrors:
        result.append(mirror)
    return result


def filter_poor_mirrors(mirror_pool: list, interval: int = 720) -> list:
    """
    Remove poorly updated mirrors last_sync is more than interval hours
    :param mirror_pool:
    :param interval: hours since last sync - defaults to 30 days
    :return: list with mirrors removed which has not synced since interval
    """
    result = []
    mirrors = (x for x in mirror_pool if int(str(x["last_sync"]).split(":")[0]) < interval)
    for mirror in mirrors:
        result.append(mirror)
    return result
