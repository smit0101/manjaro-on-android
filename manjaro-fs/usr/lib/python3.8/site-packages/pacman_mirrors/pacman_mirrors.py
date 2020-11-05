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
# Authors: Esclapion <esclapion@manjaro.org>
#          philm <philm@manjaro.org>
#          Ramon Buldó <rbuldo@gmail.com>
#          Hugo Posnic <huluti@manjaro.org>
#          Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Pacman-Mirrors Main Module"""

import importlib.util
import os
import sys

import pacman_mirrors.functions.util
from pacman_mirrors.builder import common, fasttrack, interactive
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.functions import cliFn
from pacman_mirrors.functions import config_setup
from pacman_mirrors.functions import defaultFn
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import httpFn

from pacman_mirrors.functions import util
from pacman_mirrors.mirrors.mirror import Mirror
from pacman_mirrors.translation import i18n

try:
    importlib.util.find_spec("gi.repository.Gtk")
except ImportError:
    GTK_AVAILABLE = False
else:
    GTK_AVAILABLE = True
_ = i18n.language.gettext


class PacmanMirrors:
    """Class PacmanMirrors"""

    def __init__(self):
        """Init"""
        self.config = {
            "config_file": conf.CONFIG_FILE
        }
        self.continent = False
        self.custom = False
        self.default = False
        self.fasttrack = None
        self.geoip = False
        self.interactive = False
        self.max_wait_time = 2
        self.mirrors = Mirror()
        self.network = True
        self.no_display = False
        self.no_mirrorlist = False
        self.no_status = False
        self.quiet = False
        self.selected_countries = []
        self.tty = False
        self.use_async = False

    def run(self):
        """
        Run
        # Setup config: retunrs the config dictionary and true/false on custom
        # Parse commandline
        # i686 check - change branch to x32-$branch
        # sanitize config
        # Check network
        # Update mirror pool
        # Check if mirrorlist is not to be touched - normal exit
        # Handle missing network
        # Load default mirror pool
        # Build mirror list
        """
        (self.config, self.custom) = config_setup.setup_config()
        fileFn.create_dir(self.config["work_dir"])
        cliFn.parse_command_line(self, gtk_available=GTK_AVAILABLE)
        util.i686_check(self, write=True)
        util.aarch64_check(self, write=True)
        if not config_setup.sanitize_config(config=self.config):
            sys.exit(2)
        self.network = httpFn.check_internet_connection(tty=self.tty)
        if self.network:
            httpFn.download_mirror_pool(config=self.config, tty=self.tty, quiet=self.quiet)
        if self.no_mirrorlist:
            sys.exit(0)
        if not self.network:
            if not self.quiet:
                pacman_mirrors.functions.util.internet_message(tty=self.tty)
            self.config["method"] = "random"
            self.fasttrack = False
        """
        # Load configured mirror pool
        """
        defaultFn.load_config_mirror_pool(self)
        """
        # Decide which type of mirrorlist to create
        * Fasttrack
        * Interactive
        * Default
        """
        if self.use_async:
            util.async_disclaimer()
            resp = input()
            if resp.lower() == "n":
                exit(0)
        if self.fasttrack:
            fasttrack.build_mirror_list(self, limit=self.fasttrack)
        elif self.interactive:
            interactive.build_mirror_list(self)
        else:
            common.build_mirror_list(self)


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()

