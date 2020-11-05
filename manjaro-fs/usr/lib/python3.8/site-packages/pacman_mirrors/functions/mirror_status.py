#!/usr/bin/env python

from urllib import request
from urllib import error
import json
from pacman_mirrors.constants import colors
from pacman_mirrors.functions import printFn
from pacman_mirrors.functions.util import strip_protocol
from pacman_mirrors.functions.util import msg

C_KO = colors.RED
C_OK = colors.GREEN
C_NONE = colors.RESET


def get_local_mirrors() -> tuple:
    urls = []
    with open("/etc/pacman.d/mirrorlist", "r") as f_list:
        for line in f_list:
            if not line.startswith("Server"):
                continue
            line = line.split("=")[1].strip()
            line = line.split("$")[0]
            mirror_url = line.split('/')
            mirror_url.pop()
            mirror_branch = mirror_url.pop()
            line = "/".join(mirror_url)
            urls.append(line + "/",)
    return mirror_branch, urls


def get_state(states: list, branch: str) -> tuple:
    ret_color = C_OK
    status_text = "OK"
    x = states[0]
    if branch == "testing":
        x = states[1]
    if branch == "unstable":
        x = states[2]
    if x == 0:
        ret_color = C_KO
        status_text = "--"
    return ret_color, status_text


def print_status(self) -> int:
    system_branch, mirrors_pacman = get_local_mirrors()
    try:
        with request.urlopen('https://repo.manjaro.org/status.json') as f_url:
            req = f_url.read()
    except error.URLError:
        msg("Downloading status failed!", color=colors.BLUE)
        msg("Please check you network connection ...", color=colors.YELLOW)
        return 1  # return failure
    json_data = json.loads(req)
    mirrors = []
    for mirror in json_data:
        for protocol in mirror["protocols"]:
            temp = mirror.copy()
            temp["url"] = f"{protocol}://{strip_protocol(temp['url'])}"
            mirrors.append(temp)

    mirrors = [m for m in mirrors if m['url'] in mirrors_pacman]

    printFn.yellow_msg(f"Local mirror status for {system_branch} branch")
    exit_code = 0  # up-to-date
    for i, url in enumerate(mirrors_pacman):  # same order as pacman-conf
        try:
            mirror = [m for m in mirrors if m['url'] == url][0]
            color, text = get_state(mirror["branches"], system_branch)
            len_country = max(len(m['country']) for m in mirrors) + 1
            print(f"Mirror #{str(i + 1):2}", color, f"{text}", C_NONE,
                  f"{mirror['last_sync']:7} {mirror['country']:{len_country}} {mirror['url']}")
            if i == 0 and color == C_KO:
                exit_code = 4  # first mirror not sync !
        except IndexError:
            print(C_KO, f"Mirror #{i + 1:2}", f"{url} does not exist{C_NONE}")
            exit_code = 5  # not found

    # if exit_code == 0:
    #     msg("All good", color=colors.GREEN)
    # if exit_code == 4:
    #     msg("Primary mirror is not up-to-date", color=colors.YELLOW)
    # if exit_code == 5:
    #     msg("At least one mirror does not exist", color=colors.RED)
    return exit_code
