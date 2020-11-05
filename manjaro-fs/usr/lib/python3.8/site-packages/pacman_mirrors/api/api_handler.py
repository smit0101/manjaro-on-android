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

"""Pacman-Mirrors API Handler Module"""

import shutil
import sys

from pacman_mirrors.constants import txt
from pacman_mirrors.api import apifn
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import util


def set_config(self, set_pfx: str = None, set_branch: str = None,
               re_branch: bool = False, set_protocols: bool = False, set_url: str = None) -> None:
    """
    Api configuration function
    :param self:
    :param set_pfx: prefix to the config paths
    :param set_branch: replace branch in pacman-mirrors.conf
    :param re_branch: replace branch in mirror list
    :param set_protocols: replace protocols in pacman-mirrors.conf
    :param set_url: replace mirror url in mirror list
    """
    if set_url is None:
        set_url = ""

    if set_pfx is None:
        set_pfx = ""

    """
    # apply api configuration to internal configuration object
    # Apply prefix if present
    """
    if set_pfx:
        set_pfx = apifn.sanitize_prefix(set_pfx)
        self.config["config_file"] = set_pfx + self.config["config_file"]
        self.config["custom_file"] = set_pfx + self.config["custom_file"]
        self.config["mirror_file"] = set_pfx + self.config["mirror_file"]
        self.config["mirror_list"] = set_pfx + self.config["mirror_list"]
        self.config["status_file"] = set_pfx + self.config["status_file"]
        self.config["work_dir"] = set_pfx + self.config["work_dir"]

    """
    # First API task: Set branch
    """
    if set_branch:
        # Apply branch to internal config
        self.config["branch"] = set_branch
        util.i686_check(self=self, write=False)
        util.aarch64_check(self=self, write=False)
        """
        # pacman-mirrors.conf could absent so check for it
        """
        if not fileFn.check_file(filename=self.config["config_file"]):
            """
            # Copy from host system
            """
            fileFn.create_dir(set_pfx + "/etc")
            shutil.copyfile("/etc/pacman-mirrors.conf",
                            self.config["config_file"])
            """
            # Normalize config
            """
            apifn.normalize_config(filename=self.config["config_file"])
        """
        # Write branch to config
        """
        apifn.write_config_branch(
            branch=self.config["branch"], filename=self.config["config_file"], tty=self.tty, quiet=self.quiet)
    """
    # Second API task: Create a mirror list
    """
    if set_url:
        """
        # mirror list dir could absent so check for it
        """
        fileFn.create_dir(foldername=set_pfx + "/etc/pacman.d")
        mirror = [
            {
                "url": apifn.sanitize_url(set_url),
                "country": "BUILDMIRROR",
                "protocols": [set_url[:set_url.find(":")]],
                "resp_time": "00.00"
            }
        ]
        fileFn.write_mirror_list(
            config=self.config, servers=mirror, tty=self.tty, quiet=self.quiet)
        # exit gracefully
        sys.exit(0)
    """
    # Third API task: Write protocols to config
    """
    if set_protocols:
        apifn.write_protocols(
            protocols=self.config["protocols"], filename=self.config["config_file"], tty=self.tty, quiet=self.quiet)
    """
    # Fourth API task: Rebranch the mirrorl ist
    """
    if re_branch:
        if not set_branch:
            util.msg(message=f"{txt.API_ERROR_BRANCH}", urgency=txt.ERR_CLR, tty=self.tty)
            # print(".: {} {}".format(txt.ERR_CLR, txt.API_ERROR_BRANCH))
            sys.exit(1)
        apifn.write_mirrorlist_branch(
            newbranch=self.config["branch"], filename=self.config["config_file"], tty=self.tty, quiet=self.quiet)
