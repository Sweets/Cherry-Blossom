
ORIGIN = "http://st.chatango.com"

W12, SV2, SV4, SV6, SV8, SV10, SV12 = 75, 95, 110, 104, 101, 110, 116

FIXED_WEIGHTS = {
    "de-livechat":       5, "ronaldo7-net":      51, "peliculas-flv":    69,
    "watch-dragonball":  8, "kiiiikiii":         21, "narutochatt":      70,
    "narutowire":       10, "pokemonepisodeorg": 22, "darksouls2wiki":   54,
    "soccerjumbo":      21, "rgsmotrisport":     51, "myfoxdfw":         67,
    "leeplarp":         27, "ver-anime":          8, "dbzepisodeorg":    10,
    "animelinkz":       20, "mitvcanal":         56, "watchanimeonn":    22,
    "cricket365live":   21, "eafangames":        56, "cricvid-hitcric-": 51,
    "sport24lt":        56, "animeultimacom":    34, "stream2watch3":    56,
    "vipstand":         21, "ttvsports":         56
    } # TO-DO: this. Also need a different variable name lol

SERVER_MAP = [
    ["5",   W12], ["6",   W12], ["7",   W12], ["8",   W12], ["16",  W12],
    ["17",  W12], ["18",  W12], ["9",   SV2], ["11",  SV2], ["12",  SV2],
    ["13",  SV2], ["14",  SV2], ["15",  SV2], ["19",  SV4], ["23",  SV4],
    ["24",  SV4], ["25",  SV4], ["26",  SV4], ["28",  SV6], ["29",  SV6],
    ["30",  SV6], ["31",  SV6], ["32",  SV6], ["33",  SV6], ["35",  SV8],
    ["36",  SV8], ["37",  SV8], ["38",  SV8], ["39",  SV8], ["40",  SV8],
    ["41",  SV8], ["42",  SV8], ["43",  SV8], ["44",  SV8], ["45",  SV8],
    ["46",  SV8], ["47",  SV8], ["48",  SV8], ["49",  SV8], ["50",  SV8],
    ["52", SV10], ["53", SV10], ["55", SV10], ["57", SV10], ["58", SV10],
    ["59", SV10], ["60", SV10], ["61", SV10], ["62", SV10], ["63", SV10],
    ["64", SV10], ["65", SV10], ["66", SV10], ["68",  SV2], ["71", SV12],
    ["72", SV12], ["73", SV12], ["74", SV12], ["75", SV12], ["76", SV12],
    ["77", SV12], ["78", SV12], ["79", SV12], ["80", SV12], ["81", SV12],
    ["82", SV12], ["83", SV12], ["84", SV12]
    ] # I should really change this variable name, since it's not quite original.

FONT_FACES = {
        "0":       "Arial", "1":  "Comic", "2":    "Georgia",
        "3": "Handwriting", "4": "Impact", "5":   "Palatino",
        "6":     "Papyrus", "7":  "Times", "8": "Typewriter",

        "Arial":       "0", "Comic":  "1", "Georgia":    "2",
        "Handwriting": "3", "Impact": "5", "Palatino":   "5",
        "Papyrus":     "6", "Times":  "7", "Typewriter": "8"
        }

GROUP_VERSION = 15
MAX_MESSAGE_SIZE = 2900
