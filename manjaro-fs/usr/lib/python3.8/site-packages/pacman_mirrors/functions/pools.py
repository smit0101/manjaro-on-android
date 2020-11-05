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

"""Pacman-Mirrors Country Functions"""
from pacman_mirrors.constants.timezones import countries

from pacman_mirrors.functions.httpFn import get_ip_country
from pacman_mirrors.functions.validFn import country_list_is_valid, custom_config_is_valid


def build_country_list(self: list) -> list:
    """
    Do a check on the users country selection
    :param self:
    :return: list of valid countries
    :rtype: list
    """
    """
    # Dear Fellow Manjaro Maintainer:
    # When I wrote this code, only I knew how it worked.
    # Now, no one knows!
    #
    # Therefore if you are trying to optimize
    # this routine and it fails (most surely),
    # please increase this counter as a warning for the next maintainer.
    #
    # total_hours_wasted_here = 1
    """
    result = []
    if self.selected_countries:
        if self.selected_countries == ["all"]:
            result = self.mirrors.country_pool
        else:
            if country_list_is_valid(onlycountry=self.selected_countries,
                                     countrylist=self.mirrors.country_pool,
                                     tty=self.tty):
                result = self.selected_countries
    # this executes when geoip or continent is True
    if not result:
        # get country
        if self.geoip:
            country = get_geo_country(self.mirrors.country_pool)
            if country:
                result.append(country)
        # get country list for continent
        if self.continent:
            continent_mirror_countries = get_continent_countries(get_geo_continent(), self.mirrors.mirror_pool)
            if continent_mirror_countries:
                result = continent_mirror_countries
        # validate result
        # do not return an empty list
        if not result:
            result = self.mirrors.country_pool
    return result


def get_continent(country: str) -> str:
    """
    Database query for continent where country belongs
    :param country:
    """
    continent = (x for x in countries if country in x["name"])
    for x in continent:
        return x["continent"].strip().replace(" ", "_")
    return ""


def get_continent_countries(continent: str, mirror_pool: list) -> list:
    """
    Database query for countries on continent
    :param continent:
    :param mirror_pool:
    :return: list
    """
    result = []
    mirror_countries = [c for c in mirror_pool if continent in c["continent"]]
    for m in mirror_countries:
        if m["country"] not in result:
            result.append(m["country"])
    return result


def get_geo_continent() -> str:
    """
    Return geo continent from IP
    Spaces in name are replaced with underscores
    """
    return _get_ip_continent().replace(" ", "_")


def get_geo_country(country_pool: list) -> str:
    """
    Return geo country if possible
    :param country_pool:
    :return: country name if found - spaces are replaced with underscores
    """
    geo_country = _get_ip_country().replace(" ", "_")
    selection = (x for x in country_pool if geo_country in x)
    for c in selection:
        return c
    return ""


def _get_ip_country() -> str:
    """
    Get country from ip address
    :return: country name
    """
    return get_ip_country().strip()


def _get_ip_continent() -> str:
    """
    Get continent from ip address
    :return:
    """
    country = _get_ip_country()
    continents = (x for x in countries if country in x["name"])
    for continent in continents:
        return continent["continent"].strip()
    return ""
