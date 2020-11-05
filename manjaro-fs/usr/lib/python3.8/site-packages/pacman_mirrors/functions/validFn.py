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

"""Pacman-Mirrors Validation Functions"""

import os
import sys

from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import util


def custom_config_is_valid() -> bool:
    """Check validity of custom selection
    :return: True or False
    :rtype: bool
    """
    return os.path.isfile(conf.CUSTOM_FILE)


def country_list_is_valid(onlycountry: list, countrylist: list, tty: bool = False) -> bool:
    """Check if the list of countries are valid.
    :param onlycountry: list of countries to check
    :param countrylist: list of available countries
    :param tty:
    :return: True
    :rtype: bool
    """
    for country in onlycountry:
        if country not in countrylist:
            util.msg(message=f"{txt.OPTION}{txt.OPT_COUNTRY}: {txt.OPT_COUNTRY}: '{txt.UNKNOWN_COUNTRY}'",
                     urgency=txt.WRN_CLR,
                     tty=tty)
            util.msg(message=f"{txt.AVAILABLE_COUNTRIES}",
                     urgency=txt.INF_CLR,
                     tty=tty)
            print("{}".format(", ".join(countrylist)))
            sys.exit(1)  # exit gracefully
    return True
