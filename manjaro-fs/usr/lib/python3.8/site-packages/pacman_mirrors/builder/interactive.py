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

"""Pacman-Mirrors Interactive Mirror List Builder Module"""

from operator import itemgetter
from random import shuffle

from pacman_mirrors.builder.builder import build_pool
from pacman_mirrors.constants import txt

from pacman_mirrors.functions.conversion import \
    translate_interactive_to_pool, translate_pool_to_interactive

from pacman_mirrors.functions.filter_mirror_pool_functions import \
    filter_user_branch

from pacman_mirrors.functions.outputFn import \
    write_custom_mirrors_json, write_pacman_mirror_list

from pacman_mirrors.functions.sortMirrorFn import sort_mirror_pool
from pacman_mirrors.functions.testMirrorFn import test_mirror_pool
from pacman_mirrors.functions import util
from pacman_mirrors.functions.testMirrorAsyncFn import test_mirror_pool_async


def build_mirror_list(self) -> None:
    """
    Prompt the user to select the mirrors with an interface.
    Outputs a "custom" mirror file
    Outputs a pacman mirrorlist,
    """
    worklist = build_pool(self)

    # rank or shuffle the mirrorlist before showing the ui
    if not self.default:
        # if not default run method before selection
        if self.config["method"] == "rank":
            if self.use_async:
                worklist = test_mirror_pool_async(self=self, worklist=worklist)
            else:
                worklist = test_mirror_pool(self=self, worklist=worklist)
            worklist = sort_mirror_pool(worklist=worklist, field="resp_time", reverse=False)
        else:
            shuffle(worklist)

    """
    Create a list for display in ui.
    The gui and the console ui expect the supplied list
    to be in the old country dictionary format.
    {
        "country": "country_name",
        "resp_time": "m.sss",
        "last_sync": "HHh MMm",
        "url": "http://server/repo/"
    }
    """
    interactive_list = translate_pool_to_interactive(mirror_pool=worklist, tty=self.tty)

    # import the correct ui
    if self.no_display:
        # in console mode
        from pacman_mirrors.dialogs import consoleui as ui
    else:
        # gtk mode
        from pacman_mirrors.dialogs import graphicalui as ui

    interactive = ui.run(server_list=interactive_list, random=self.config["method"] == "random",
                         default=self.default)

    # process user choices
    if interactive.is_done:
        """
        translate interactive list back to our json format
        """
        custom_pool, mirror_list = translate_interactive_to_pool(selection=interactive.custom_list,
                                                                 mirror_pool=self.mirrors.mirror_pool, tty=self.tty)

        """
        Try selected method on the mirrorlist
        """
        try:
            _ = mirror_list[0]
            # using the default runs method after selection
            if self.default:
                if self.config["method"] == "rank":
                    if self.use_async:
                        mirror_list = test_mirror_pool_async(self=self, worklist=mirror_list)
                    else:
                        mirror_list = test_mirror_pool(self=self, worklist=mirror_list)
                    mirror_list = sorted(mirror_list, key=itemgetter("resp_time"))
                else:
                    shuffle(mirror_list)
        except IndexError:
            pass

        """
        Write custom mirror pool
        Write mirrorlist
        """
        try:
            _ = custom_pool[0]
            self.custom = True
            self.config["country_pool"] = ["Custom"]

            """
            Writing the custom mirror pool file
            """
            write_custom_mirrors_json(self=self, selected_mirrors=custom_pool)

            """
            Writing mirrorlist
            If the mirror list is empty because 
            no up-to-date mirrors exist for users branch
            raise IndexError to the outer try-catch
            """
            try:
                _ = mirror_list[0]
                write_pacman_mirror_list(self, mirror_list)
                if self.no_status:
                    util.msg(message=f"{txt.OVERRIDE_STATUS_CHOICE}", urgency=txt.WRN_CLR, tty=self.tty)
                    util.msg(message=f"{txt.OVERRIDE_STATUS_MIRROR}", urgency=txt.WRN_CLR, tty=self.tty)
            except IndexError:
                raise IndexError
        except IndexError:
            util.msg(message=f"{txt.NO_SELECTION}", urgency=txt.WRN_CLR, tty=self.tty)
            util.msg(message=f"{txt.NO_CHANGE}", urgency=txt.INF_CLR, tty=self.tty)
