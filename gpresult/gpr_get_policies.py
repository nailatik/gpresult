import sys

from gi.repository import Alterator

GPRESULT1_PATH = "/org/altlinux/alterator/gpresult"
TIMEOUT = -1


def _check(lib, status, exit_code):
    if status != 0:
        print(lib.get_last_error(), file=sys.stderr)
        sys.exit(1)
    if exit_code != 0:
        print(f"Backend exited with code {exit_code}", file=sys.stderr)
        sys.exit(1)


def _tag_scope(gpos, scope):
    for gpo in gpos:
        gpo.scope = scope
    return gpos


def _get_user_gpos(lib):
    status, gpos, exit_code = lib.gpresult_get_user_gpos(GPRESULT1_PATH, TIMEOUT)
    _check(lib, status, exit_code)
    return _tag_scope(gpos or [], "user")


def _get_machine_gpos(lib):
    status, gpos, exit_code = lib.gpresult_get_machine_gpos(GPRESULT1_PATH, TIMEOUT)
    _check(lib, status, exit_code)
    return _tag_scope(gpos or [], "machine")


def _get_all_gpos(lib):
    status, user_gpos, machine_gpos, exit_code = lib.gpresult_get_all_gpos(
        GPRESULT1_PATH, TIMEOUT
    )
    _check(lib, status, exit_code)
    return _tag_scope(user_gpos or [], "user") + _tag_scope(machine_gpos or [], "machine")


def _get_gpo_by(lib, cmd, cmd_arg):
    if cmd == "guid":
        status, gpo, exit_code = lib.gpresult_get_gpo_by_guid(
            GPRESULT1_PATH, TIMEOUT, cmd_arg
        )
    else:
        status, gpo, exit_code = lib.gpresult_get_gpo_by_name(
            GPRESULT1_PATH, TIMEOUT, cmd_arg
        )
    _check(lib, status, exit_code)
    return [gpo] if gpo is not None else []


def _filter_by(gpos, cmd, cmd_arg):
    if cmd == "guid":
        return [gpo for gpo in gpos if gpo.get_guid() == cmd_arg]
    return [gpo for gpo in gpos if gpo.get_name() == cmd_arg]


def get_policies(obj=None, cmd=None, cmd_arg=None):
    lib = Alterator.Glib()

    if cmd in ("guid", "name"):
        if obj == "user":
            return _filter_by(_get_user_gpos(lib), cmd, cmd_arg)
        if obj == "machine":
            return _filter_by(_get_machine_gpos(lib), cmd, cmd_arg)
        return _get_gpo_by(lib, cmd, cmd_arg)

    if obj == "user":
        return _get_user_gpos(lib)
    if obj == "machine":
        return _get_machine_gpos(lib)
    return _get_all_gpos(lib)
