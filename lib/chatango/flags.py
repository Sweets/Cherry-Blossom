
def pack_flag(flags: str or int, flag: int) -> int:
    assert type(flags) in (str, int), "Invalid flags"
    assert type(flag) is int, "Invalid flag"
    return int(flags) | flag

def unpack_flag(flags: str or int, flag: int) -> int:
    assert type(flags) in (str, int), "Invalid flags"
    assert type(flag) is int, "Invalid flag"
    return int(flags) ^ flag

def has_flag(flags: str or int, flag: int) -> bool:
    assert type(flags) in (str, int), "Invalid flags"
    assert type(flag) is int, "Invalid flag"
    return int(flags) & flag

ROOM_FLAGS = {
    "list_taxonomy":                1, "noanons":              4, "noflagging":          8,
    "nocounter":                   16, "noimages":            32, "nolinks":            64,
    "novideos":                   128, "nostyledtext":       256, "nolinkschatango":   512,
    "nobrdcastmsgwithbw":        1024, "ratelimitregimeon": 2048, "channelsdisabled": 8192,
    "nlp_singlemsg":            16384, "nlp_msgqueue":     32768, "broadcast_mode":  65536,
    "closed_if_no_mods":       131072, "is_closed":       262144, "show_mod_icons": 524288,
    "mods_choose_visibility": 1048576, "nlp_ngram":      2097152, "no_proxies":    4194304,
    "has_xml":              268435456, "unsafe":       536870912
    } # Working on more "human-friendly" flag names, even though most of these are what Chatango calls them.

MODERATOR_FLAGS = {
    "deleted":           1, "edit_mods":                 2, "edit_mod_visibility":   4,
    "edit_bw":           8, "edit_restrictions":        16, "edit_group":           32,
    "see_counter":      64, "see_mod_channel":         128, "see_mod_actions":     256,
    "edit_nlp":        512, "edit_gp_annc":           1024, "edit_admins":        2048,
    "edit_supermods": 4096, "no_sending_limitations": 8192, "see_ips":           16384,
    "close_group":   32768, "can_broadcast":         65536, "mod_icon_visible": 131072,
    "is_staff":     262144, "staff_icon_visible":   524288
    }

MESSAGE_FLAGS = {
    "premium":           4, "bg_on":            8, "media_on":         16,
    "censored":         32, "show_mod_icon":   64, "show_staff_icon": 128,
    "default_icon":     64, "channel_red":    256, "channel_orange":  512,
    "channel_green":  1024, "channel_cyan":  2048, "channel_blue":   4096,
    "channel_purple": 8192, "channel_pink": 16384, "channel_mod":   32768
    }

# Defaults. I'm not exactly proud of the way this was written

DEFAULT_MODERATOR_FLAGS = ["see_mod_channel", "see_mod_actions", "see_counter", "see_ips", "can_broadcast"]
DEFAULT_ADMINISTRATOR_FLAGS = DEFAULT_MODERATOR_FLAGS + ["edit_mod_visibility", "edit_bw", "edit_restrictions", "edit_group", "edit_nlp", "edit_gp_annc", "no_sending_limitations", "is_staff"]

ADMINISTRATOR_ONLY = ["edit_mods", "edit_restrictions", "edit_mod_visibility", "edit_group", "edit_gp_annc", "close_group", "is_staff"]

ADMINISTRATOR_REQUIRED = DEFAULT_MODERATOR_FLAGS + ["no_sending_limitations", "edit_bw", "edit_nlp", "is_staff"]
