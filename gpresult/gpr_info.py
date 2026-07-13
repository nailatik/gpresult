import gettext
import json

from gi.repository import Alterator

gettext.bindtextdomain("gpresult", None)
gettext.textdomain("gpresult")
_ = gettext.gettext

_ACTION_LABELS = {
    Alterator.GpoAction.CREATE: _("Create"),
    Alterator.GpoAction.REPLACE: _("Replace"),
    Alterator.GpoAction.UPDATE: _("Update"),
    Alterator.GpoAction.DELETE: _("Delete"),
}


def _action_label(pref):
    return _ACTION_LABELS.get(pref.get_action())


def _format_filters(pref):
    raw = pref.get_filters()
    if not raw:
        return None

    try:
        filters = json.loads(raw)
    except (TypeError, ValueError):
        return None

    lines = []
    for f in filters:
        if isinstance(f, dict):
            for filter_type, attrs in f.items():
                lines.append(_("Filter type") + ": " + filter_type)
                if isinstance(attrs, dict):
                    for key, val in attrs.items():
                        lines.append("  " + _(key.capitalize()) + ": " + str(val))
    return "\n".join(lines) if lines else None


def _common_tail(pref):
    return [
        [_("Disabled"), pref.get_disabled()],
        [_("Remove policy"), pref.get_remove_policy()],
    ]


def _folder_info_list(pref):
    return [
        [_("Type"), _("Folder")],
        [_("Path"), pref.path],
        [_("Action"), _action_label(pref)],
        [_("Delete folder"), pref.delete_folder],
        [_("Delete subfolder"), pref.delete_sub_folder],
        [_("Delete files"), pref.delete_files],
        [_("Hidden folder"), pref.hidden_folder],
    ] + _common_tail(pref)


def _drive_info_list(pref):
    return [
        [_("Type"), _("Drive map")],
        [_("Login"), pref.login],
        [_("Password"), pref.password],
        [_("Direction"), pref.dir],
        [_("Path"), pref.path],
        [_("Action"), _action_label(pref)],
        [_("This drive"), pref.this_drive],
        [_("All drives"), pref.all_drives],
        [_("Label"), pref.label],
        [_("Persistent"), pref.persistent],
        [_("Use letter"), str(pref.use_letter)],
    ] + _common_tail(pref)


def _envvar_info_list(pref):
    return [
        [_("Type"), _("Environment variables")],
        [_("Name"), pref.name],
        [_("Value"), pref.value],
        [_("Action"), _action_label(pref)],
    ] + _common_tail(pref)


def _file_info_list(pref):
    return [
        [_("Type"), _("File")],
        [_("From path"), pref.from_path],
        [_("Source"), pref.source],
        [_("Action"), _action_label(pref)],
        [_("Target path"), pref.target_path],
        [_("Read only"), pref.read_only],
        [_("Archive"), pref.archive],
        [_("Hidden"), pref.hidden],
        [_("Suppress"), pref.suppress],
        [_("Executable"), pref.executable],
    ] + _common_tail(pref)


def _inifile_info_list(pref):
    return [
        [_("Type"), _("Inifile")],
        [_("Path"), pref.path],
        [_("Section"), pref.section],
        [_("Property"), pref.property],
        [_("Value"), pref.value],
        [_("Action"), _action_label(pref)],
    ] + _common_tail(pref)


def _networkshare_info_list(pref):
    return [
        [_("Type"), _("Network share")],
        [_("Name"), pref.name],
        [_("Action"), _action_label(pref)],
        [_("Path"), pref.path],
        [_("All regular"), pref.all_regular],
        [_("Abe"), pref.abe],
        [_("Limit users"), pref.limit_users],
        [_("Comment"), pref.comment],
    ] + _common_tail(pref)


def _shortcut_info_list(pref):
    return [
        [_("Type"), _("Shortcut")],
        [_("Destination"), pref.dest],
        [_("Path"), pref.path],
        [_("Expanded path"), pref.expanded_path],
        [_("Arguments"), pref.arguments],
        [_("Name"), pref.name],
        [_("Action"), _action_label(pref)],
        [_("Changed"), pref.get_changed()],
        [_("Icon"), pref.icon],
        [_("Comment"), pref.comment],
        [_("Perfom action in user context"), pref.is_in_user_context],
        [_("Link type"), pref.shortcut_type],
        [_("Desktop file template"), pref.desktop_file_template],
    ] + _common_tail(pref)


_CATEGORY_RENDERERS = {
    Alterator.GpoPreferenceType.FOLDERS: _folder_info_list,
    Alterator.GpoPreferenceType.DRIVES: _drive_info_list,
    Alterator.GpoPreferenceType.ENVIRONMENTVARIABLES: _envvar_info_list,
    Alterator.GpoPreferenceType.FILES: _file_info_list,
    Alterator.GpoPreferenceType.INIFILES: _inifile_info_list,
    Alterator.GpoPreferenceType.NETWORKSHARES: _networkshare_info_list,
    Alterator.GpoPreferenceType.SHORTCUTS: _shortcut_info_list,
}


def preference_info_list(pref):
    renderer = _CATEGORY_RENDERERS.get(pref.get_category())
    if renderer is None:
        return None
    return [renderer(pref), {"is_prefs": True}]


def preference_lifecycle_info_list(pref):
    lifecycle = [
        [_("UID"), pref.get_uid()],
        [_("Bypass errors"), pref.get_bypass_errors()],
        [_("Apply once"), pref.get_apply_once()],
    ]
    if pref.get_category() != Alterator.GpoPreferenceType.SHORTCUTS:
        lifecycle.append([_("Changed"), pref.get_changed()])
    lifecycle.append([_("Filters"), _format_filters(pref)])
    return lifecycle


def keyvalue_info_list(kv, with_previous=True):
    if with_previous:
        return [
            kv.get_key(),
            kv.get_value(),
            kv.get_previous_value(),
            {"type": kv.get_value_type(), "is_list": kv.get_is_list()},
        ]
    return [
        kv.get_key(),
        kv.get_value(),
        {"type": kv.get_value_type(), "is_list": kv.get_is_list()},
    ]


def gpo_info_list(gpo, with_previous=True, with_lifecycle=False):
    kvs = [
        keyvalue_info_list(kv, with_previous)
        for kv in sorted(gpo.get_keys() or [], key=lambda kv: kv.get_key())
    ]

    prefs = []
    for pref in gpo.get_preferences() or []:
        info = preference_info_list(pref)
        if info is None:
            continue
        if with_lifecycle:
            info[0].extend(preference_lifecycle_info_list(pref))
        prefs.append(info)

    return [
        ["GPO", gpo.get_name()],
        [_("Path"), gpo.get_path()],
        [_("Version"), gpo.get_version()],
        ["GUID", gpo.get_guid()],
        [_("Keys"), kvs or None],
        [_("Preferences"), prefs or None],
    ]
