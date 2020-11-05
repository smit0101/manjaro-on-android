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
# Authors: Esclapion
#          Hugo Posnic <huluti@manjaro.org>

"""Pacman-Mirrors API Functions Module"""


import os
import sys
import tempfile

from pacman_mirrors.constants import txt
from pacman_mirrors.functions import util


def find_mirrorlist_branch(filename: str, tty: bool = False) -> str:
    """find and return the branch found in mirrorlist
    :param filename:
    :param tty:
    """
    try:
        with open(filename) as mirrorlist:
            for line in mirrorlist:
                if "Server = " in line:
                    workstring = line.strip()[-21:]  # /unstable/$repo/$arch
                    pos = workstring.find("/")
                    workstring = workstring[pos + 1:]
                    pos = workstring.find("/")
                    return workstring[:pos]
    except OSError as err:
        util.msg(message=f"{txt.CANNOT_READ_FILE}: {err.filename}: {err.strerror}",
                 urgency=txt.ERR_CLR,
                 tty=tty)
        sys.exit(2)


def normalize_config(filename: str) -> None:
    """Normalize configuration
    :param filename:
    """
    normalize_country(filename)
    normalize_method(filename)
    normalize_protocols(filename)
    normalize_ssl(filename)
    normalize_testfile(filename)


def normalize_country(filename: str) -> None:
    """Write default OnlyCountry =
    :param filename:
    """
    lookfor = "OnlyCountry ="
    default = "# OnlyCountry =\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(f"{default}")
                replaced = True
            else:
                tmp.write(f"{line}")
        if not replaced:
            tmp.write(f"{default}")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_method(filename: str) -> None:
    """Write default Method = rank
    :param filename:
    """
    lookfor = "Method ="
    default = "# Method = rank\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(f"{default}")
                replaced = True
            else:
                tmp.write(f"{line}")
        if not replaced:
            tmp.write(f"{default}")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_protocols(filename: str) -> None:
    """Write default Protocols =
    :param filename:
    """
    lookfor = "Protocols ="
    default = "# Protocols =\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(f"{default}")
                replaced = True
            else:
                tmp.write(f"{line}")
        if not replaced:
            tmp.write(f"{default}")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_ssl(filename: str) -> None:
    """Write default SSLVerify = False
    :param filename:
    """
    lookfor = "SSLVerify ="
    default = "# SSLVerify = False\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(f"{default}")
                replaced = True
            else:
                tmp.write(f"{line}")
        if not replaced:
            tmp.write(f"{default}")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_testfile(filename: str) -> None:
    """Write default TestFile = core.db.tar.gz
    :param filename:
    """
    lookfor = "TestFile ="
    default = "# TestFile = core.db.tar.gz\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(f"{default}")
                replaced = True
            else:
                tmp.write(f"{line}")
        if not replaced:
            tmp.write(f"{default}")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def sanitize_prefix(prefix: str) -> str:
    """Sanitize prefix
    :param prefix:
    :returns sanitized prefix
    """
    if prefix.endswith("/"):
        prefix = prefix[:-1]
    return prefix


def sanitize_url(url: str) -> str:
    """Sanitize url
    :param url:
    :returns sanitized url
    """
    if url.endswith("/"):
        return url
    return url + "/"


def write_config_branch(branch: str, filename: str, tty: bool = False, quiet: bool = False) -> None:
    """Write branch
    :param branch:
    :param filename:
    :param tty:
    :param quiet:
    """
    lookfor = "Branch ="
    default = "# Branch = stable\n"
    if branch == "stable":
        branch = default
    else:
        branch = "Branch = {}\n".format(branch)
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if lookfor in line:
                    tmp.write(branch)
                    replaced = True
                else:
                    tmp.write(f"{line}")
            if not replaced:
                tmp.write(branch)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            util.msg(
                message=f"{txt.API_CONF_RE_BRANCH}", urgency=txt.INF_CLR, tty=tty)
    except OSError as err:
        util.msg(
            message=f"{txt.CANNOT_READ_FILE}: {err.filename}: {err.strerror}", urgency=txt.ERR_CLR, tty=tty)
        sys.exit(2)


def write_mirrorlist_branch(newbranch: str, filename: str, tty: bool = False, quiet: bool = False) -> None:
    """Write branch in mirrorlist
    :param newbranch:
    :param filename:
    :param tty:
    :param quiet:
    """
    lookfor = "Server ="
    branch = find_mirrorlist_branch(filename=filename, tty=tty)
    try:
        with open(filename) as mirrorlist, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            for line in mirrorlist:
                if lookfor in line:
                    line = line.replace(branch, newbranch)
                    tmp.write(f"{line}")
                else:
                    tmp.write(f"{line}")
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            util.msg(
                message=f"{txt.API_MIRRORLIST_RE_BRANCH}", urgency=txt.INF_CLR, tty=tty)
    except OSError as err:
        util.msg(
            message=f"{txt.CANNOT_READ_FILE}: {err.filename}: {err.strerror}", urgency=txt.ERR_CLR, tty=tty)
        sys.exit(2)


def write_protocols(protocols: str, filename: str, tty: bool = False, quiet: bool = False) -> None:
    """Write protocols
    :param protocols:
    :param filename:
    :param tty:
    :param quiet:
    """
    lookfor = "Protocols ="
    default = "# Protocols = \n"
    if protocols:
        protocols = "Protocols = {}\n".format(",".join(protocols))
    else:
        protocols = default
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if lookfor in line:
                    tmp.write(protocols)
                    replaced = True
                else:
                    tmp.write(f"{line}")
            if not replaced:
                tmp.write(protocols)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            util.msg(
                message=f"{txt.API_CONF_PROTOCOLS}", urgency=txt.INF_CLR, tty=tty)
    except OSError as err:
        util.msg(
            message=f"{txt.CANNOT_READ_FILE}: {err.filename}: {err.strerror}", urgency=txt.ERR_CLR, tty=tty)
        sys.exit(2)
