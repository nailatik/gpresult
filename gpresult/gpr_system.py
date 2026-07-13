import datetime
import gettext
from pathlib import Path

import distro

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext


def get_timestamp():
    now = datetime.datetime.now()

    return now.strftime("%d-%m-%Y %H:%M")


def os_conf():
    os_id, os_version, os_name = distro.linux_distribution()

    return [
        [_("Operating system:"), os_id],
        [_("OS Version:"), f"{os_version} ({os_name})"],
    ]


def get_user_home_dir():
    home_dir = str(Path.home())

    return [_("Local Profile:"), home_dir]
