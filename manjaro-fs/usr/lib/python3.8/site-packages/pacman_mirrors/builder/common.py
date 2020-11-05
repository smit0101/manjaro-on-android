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

"""Pacman-Mirrors Common Mirror List Builder Module"""

from random import shuffle

from pacman_mirrors.builder.builder import build_pool
from pacman_mirrors.functions.filter_mirror_status_functions import \
    filter_error_mirrors

from pacman_mirrors.constants import txt

from pacman_mirrors.functions.outputFn import \
    write_pacman_mirror_list, write_custom_mirrors_json

from pacman_mirrors.functions.sortMirrorFn import sort_mirror_pool
from pacman_mirrors.functions.testMirrorFn import test_mirror_pool
from pacman_mirrors.functions.testMirrorAsyncFn import test_mirror_pool_async
from pacman_mirrors.functions import util


def build_mirror_list(self) -> None:
    """
    Generate common mirrorlist
    """
    work_pool = build_pool(self)

    """
    Check the length of selected_countries against the full countrylist
    If selected_countries is the lesser then we build a custom pool file
    """
    if len(self.selected_countries) < len(self.mirrors.country_pool):
        try:
            _ = self.selected_countries[0]
            write_custom_mirrors_json(self=self, selected_mirrors=work_pool)
        except IndexError:
            pass

    if self.config["method"] == "rank":
        if self.use_async:
            work_pool = test_mirror_pool_async(self=self, worklist=work_pool)
        else:
            work_pool = test_mirror_pool(self=self, worklist=work_pool)
        work_pool = sort_mirror_pool(worklist=work_pool, field="resp_time", reverse=False)
    else:
        shuffle(work_pool)

    """
    Write mirrorlist
    """
    try:
        _ = work_pool[0]
        write_pacman_mirror_list(self=self, selected_servers=work_pool)
        if self.custom:
            util.msg(message=f"{txt.MIRROR_LIST_CUSTOM_RESET} 'sudo {txt.MODIFY_CUSTOM}'",
                     urgency=txt.INF_CLR, tty=self.tty)
            util.msg(message=f"{txt.REMOVE_CUSTOM_CONFIG} 'sudo {txt.RESET_ALL}'",
                     urgency=txt.INF_CLR, tty=self.tty)
        if self.no_status:
            util.msg(message=f"{txt.OVERRIDE_STATUS_CHOICE}", urgency=txt.WRN_CLR, tty=self.tty)
            util.msg(message=f"{txt.OVERRIDE_STATUS_MIRROR}", urgency=txt.WRN_CLR, tty=self.tty)
    except IndexError:
        util.msg(message=f"{txt.NO_SELECTION}", urgency=txt.WRN_CLR, tty=self.tty)
        util.msg(message=f"{txt.NO_CHANGE}", urgency=txt.INF_CLR, tty=self.tty)
