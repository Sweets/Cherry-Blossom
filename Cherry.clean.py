
# CherryLib version 5 (major.micro)
# Features:

# Contact:
# Coil  - <coil@[redacted email]>  - Maintainer, programmer, clean up
# Judge - <[redacted email]>  - Programmer

# Cherry - A flexible Python based Chatango library used to connect
# to rooms, private messaging, as well as update a user profile.
# Supports most, if not all of Chatango's new features (Websocket support)

# Readme:

# This version of Cherry is an edited branch, and is different from the original to keep some
# features specific to my bot. I am not required, whether by law, or otherwise, to post my non-edited version,
# and as such, I shant.
# Also, please understand, Judge and I wrote this file a long time ago, and it wasn't written to meet any other
# sort of requirement aside from being a library for Chatango. This means that it wasn't written to be readable,
# and it wasn't written so we would add features at the request of its users, as its inteded users only included
# one person, me.
# To sum this up, I won't continue to maintain this. You're free to report issues if you please, but there's no point.

# Also, don't bother trying to tell me Cherry is bad. I know it's bad.

# -Coil

# Licensed under MIT.

# Dependencies:
# Python 3
# Requests         (pip install requests)
# Websocket-client (pip install websocket-client)

# Errors:
# CherryError        - Usually errors from the websocket, get/post requests, etc. (can also be raised from ConnectionManager)
# CherryAuthError    - Lib unable to login to account, credentials are either invalid or do not match the selected user
# CherryMessageError - Error messaging rooms/pms

version    = "5.1"

makeObject = lambda kw = None: (type("CherryObject", (), kw)) if isinstance(kw, dict) else None
modules    = [
					"html",   "json", "random",    "re",   "requests",
					"socket", "sys",  "threading", "time", "websocket",
					"html.parser", "getpass"
				]

class CherryError(Exception): pass        # General
class CherryImportError(Exception): pass  # Imports pls
class CherryAuthError(Exception): pass    # User authentication
class CherryMessageError(Exception): pass # Messaging

missing_Dependencies = []
pip_Install_Commands = {
		"requests":  "pip install requests",
		"websocket": "pip install websocket-client"
	}
for module in modules:
	try:
		vars()[module] = __import__(module)
	except ImportError:
		command = pip_Install_Commands.get(module, None)
		string  = module
		if command:
			string += " ({})".format(
					command
				)
		missing_Dependencies.append(string)

if len(missing_Dependencies):
	raise CherryImportError("You have %s missing dependenc%s: %s" % (
			str(len(missing_Dependencies)),
			"ies" if len(missing_Dependencies) > 1 else "y",
			", ".join(missing_Dependencies)
		))
	exit(0)

pyver = sys.version_info
if pyver[0] >= 3:
	if pyver[2] < 4:
		html.unescape = html.parser.HTMLParser().unescape
else:
	raise CherryError("Improper Python version, please ensure that you have Python 3+ installed and running on the server.")
	exit(0)

class Utilities(object):
	errors  = list()
	w12, sv2, sv4, sv6, sv8, sv10, sv12 = 75, 95, 110, 104, 101, 110, 116
	weights = makeObject({
			"specials": {
				'de-livechat':      '5',  'ronaldo7-net':      '51', 'peliculas-flv':    '69',
				'watch-dragonball': '8',  'kiiiikiii':         '21', 'narutochatt':      '70',
				'narutowire':       '10', 'pokemonepisodeorg': '22', 'darksouls2wiki':   '54',
				'soccerjumbo':      '21', 'rgsmotrisport':     '51', 'myfoxdfw':         '67',
				'leeplarp':         '27', 'ver-anime':         '8',  'dbzepisodeorg':    '10',
				'animelinkz':       '20', 'mitvcanal':         '56', 'watchanimeonn':    '22',
				'cricket365live':   '21', 'eafangames':        '56', 'cricvid-hitcric-': '51',
				'sport24lt':        '56', 'animeultimacom':    '34', 'stream2watch3':    '56',
				'vipstand':         '21', 'ttvsports':         '56'
			},
			"weights": [
				["5",   w12], ["6",   w12], ["7",   w12], ["8",   w12], ["16",  w12],
				["17",  w12], ["18",  w12], ["9",   sv2], ["11",  sv2], ["12",  sv2],
				["13",  sv2], ["14",  sv2], ["15",  sv2], ["19",  sv4], ["23",  sv4],
				["24",  sv4], ["25",  sv4], ["26",  sv4], ["28",  sv6], ["29",  sv6],
				["30",  sv6], ["31",  sv6], ["32",  sv6], ["33",  sv6], ["35",  sv8],
				["36",  sv8], ["37",  sv8], ["38",  sv8], ["39",  sv8], ["40",  sv8],
				["41",  sv8], ["42",  sv8], ["43",  sv8], ["44",  sv8], ["45",  sv8],
				["46",  sv8], ["47",  sv8], ["48",  sv8], ["49",  sv8], ["50",  sv8],
				["52", sv10], ["53", sv10], ["55", sv10], ["57", sv10], ["58", sv10],
				["59", sv10], ["60", sv10], ["61", sv10], ["62", sv10], ["63", sv10],
				["64", sv10], ["65", sv10], ["66", sv10], ["68",  sv2], ["71", sv12],
				["72", sv12], ["73", sv12], ["74", sv12], ["75", sv12], ["76", sv12],
				["77", sv12], ["78", sv12], ["79", sv12], ["80", sv12], ["81", sv12],
				["82", sv12], ["83", sv12], ["84", sv12]
			]
		})
	flags = makeObject({
			"room": {
				"LIST_TAXONOMY":          1,      "NOANONS":            4,      "NOFLAGGING":        8,   
				"NOCOUNTER":              16,     "NOIMAGES":           32,     "NOLINKS":           64,
				"NOVIDEOS":               128,    "NOSTYLEDTEXT":       256,    "NOLINKSCHATANGO":   512,
				"NOBRDCASTMSGWITHBW":     1024,   "RATELIMITREGIMEON":  2048,   "CHANNELSDISABLED":  8192,
				"NLP_SINGLEMSG":          16384,  "NLP_MSGQUEUE":       32768,  "BROADCAST_MODE":    65536,
				"CLOSED_IF_NO_MODS":      131072, "IS_CLOSED":          262144, "SHOW_MOD_ICONS":    524288,
				"MODS_CHOOSE_VISIBILITY": 1048576,
				"NLP_NGRAM":              2097152,
				"NO_PROXIES":             4194304,
				"HAS_XML":                268435456,
				"UNSAFE":                 536870912
			},
			"moderator": {
				"DELETED":        1,      "EDIT_MODS":              2,     "EDIT_MOD_VISIBILITY": 4,
				"EDIT_BW":        8,      "EDIT_RESTRICTIONS":      16,    "EDIT_GROUP":          32,
				"SEE_COUNTER":    64,     "SEE_MOD_CHANNEL":        128,   "SEE_MOD_ACTIONS":     256,
				"EDIT_NLP":       512,    "EDIT_GP_ANNC":           1024,  "EDIT_ADMINS":         2048,
				"EDIT_SUPERMODS": 4096,   "NO_SENDING_LIMITATIONS": 8192,  "SEE_IPS":             16384,
				"CLOSE_GROUP":    32768,  "CAN_BROADCAST":          65536, "MOD_ICON_VISIBLE":    131072,
				"IS_STAFF":       262144, "STAFF_ICON_VISIBLE":     524288
			},
			"message": {
				"PREMIUM":      4,    "BG_ON":         8,   "MEDIA_ON":        16,
				"CENSORED":     32,   "SHOW_MOD_ICON": 64,  "SHOW_STAFF_ICON": 128,
				"DEFAULT_ICON": 64,   "CHANNEL_RED":   256, "CHANNEL_BLUE":    2048,
				"CHANNEL_MOD":  32768
			}
		})

	@staticmethod
	def get_Server(name):
		if (name in Utilities.weights.specials):
			return Utilities.weights.specials[name.lower()]
		else:
			name    = re.sub("-|_", "q", name.lower())
			alpha   = int(name[0:5], 36)
			beta    = max(int(name[6:9] or '0', 36), 1000)
			gamma   = (alpha % beta) / beta
			delta   = sum(x[1] for x in Utilities.weights.weights)
			epsilon = 0
			for weight, zeta in Utilities.weights.weights:
				epsilon += (zeta / delta)
				if (gamma <= epsilon):
					return weight
			return None

	@staticmethod
	def pm_Auth(username, password):
		try:
			data    = {
				"user_id":     username,
				"password":    password,
				"storecookie": "on",
				"checkerrors": "yes"
			}
			cookies = requests.post("http://chatango.com/login", data = data).cookies
			return cookies.get("auth.chatango.com", None), cookies.get("id.chatango.com", None)
		except (socket.gaierror, requests.packages.urllib3.exceptions.ProtocolError, requests.exceptions.ConnectionError):
			return (None, None, ('gaierror', 'name or service not known'))

	@staticmethod
	def anonymous_User_Id(number, uid):
		number = str(number).split(".")[0]
		number = number[-4:] if number.isdigit() else "3452"
		uid    = str(uid[-4:])
		return "".join([ str( ( (int(x) + int(y)) % 10 )) for x, y in zip(number, uid)])

class Event(object):
	def __init__(self, data, room, name, target, *args):
		self.controller    = data['controller']
		self.room          = room
		self.time          = (data['interval'], data['delay'])
		self.target        = target
		self.thread        = makeObject({
				"active":   False,
				"loop":     False,
				"instance": None
			})
		if hasattr(room, self.target):
			if self.time[0] > 0:
				self.thread.loop     = True
				self.thread.instance = threading.Timer(self.time[0], self.spawn_Event, args=(args))
			else:
				self.thread.instance = threading.Thread(target=self.spawn_Event, name=self.name, args=(args))
			self.thread.active       = True
			self.thread.instance.daemon  = True
			self.thread.instance.start()

	def spawn_Event(self, *args):
		if self.time[1] > 0:
			time.sleep(self.time[1])
		if self.thread.loop:
			while self.thread.active:
				getattr(self.room, self.target)(*args)
				time.sleep(self.time[0])
		else:
			getattr(self.room, self.target)(*args)

	def terminate_Event(self):
		self.thread.loop     = False
		self.thread.active   = False
		self.thread.instance = None

class ConnectionManager(object):
	def __init__(self, room, weight, port, manager):
		self.alive     = False
		self.websocket = None
		self.thread    = None
		self.manager   = manager
		self.make_Connection(room, weight, port)
		
	def make_Connection(self, room, weight, port):
		try:
			URL = "ws://{}.chatango.com:{}".format(
					weight, port
				)
			self.websocket = websocket.create_connection(URL, origin="http://st.chatango.com")
			self.thread    = Event({
				"controller": self.manager,
				"interval":    0.1,
				"delay":       0}, self, "{}:{}".format(weight, room), "manage_Websocket", self.manager, room)
			self.alive     = True
			return self
		except Exception as e:
			Utilities.errors.append([time.time(), e, self.manager])
			raise CherryError(e)

	def manage_Websocket(self, manager, room):
		try:
			buffer = self.websocket.recv()
			if self.manager.controller.debug == True:
				print(buffer)
				print(Utilities.errors)
			self.manager.maintain(buffer)
		except (websocket._exceptions.WebSocketConnectionClosedException, BrokenPipeError, socket.error, ConnectionResetError):
			if self.alive == True and hasattr(self.manager, "name"):
				self.manager.controller.leave_Room(self.manager.name)
			else:
				self.end_Connection()
		except Exception as e:
			if self.manager.controller.show_runtime_errors == True:
				self.manager.call("runtime_Error", time.time(), e, self.manager)
			Utilities.errors.append([time.time(), e, self.manager])

	def end_Connection(self, call=False):
		self.websocket.close()
		self.thread.terminate_Event()
		self.alive = False
		if call == True:
			self.manager.controller.call("room_Disconnected", self.manager.name)

class Room(object):
	def __init__(self, username, password, name, controller):
		self.controller  = controller
		self.weight      = Utilities.get_Server(name)
		self.name        = name
		self.time        = None
		self.users       = makeObject({
				"owner":        "",
				"moderators":   {},
				"participant":  makeObject({}),
				"participants": []
			})
		self.banned      = makeObject({
				"words":        [],
				"users":        []
			})
		self.limit       = 0
		self.limited     = 0
		self.closed      = False
		self.silent      = False
		self.user        = makeObject({
				"uid":          str(int(random.randrange(10**15,(10**16)-1))),
				"name":         username,
				"ip_Address":   None,
				"format":       [
						"",   # Font colour
						"",   # Name colour
						11,   # Font size
						0,    # Font face
						False # Use bg
					],
				"extra_Format": [
						False, # Italic
						False, # Bold
						False  # Underline
					]
			})
		self.flags       = None
		self.uids        = makeObject({})
		self.uidkeys     = []
		if not isinstance(self.weight, type(None)):
			self.unum       = None
			self.messages   = {}
			self.finished   = False
			self.checking   = []
			self.msg_queue  = []
			self.connection = ConnectionManager(self.name, "s{}".format(self.weight), 1800, self)
			self.proceed(username, password)
	
	def heartbeat(self):
		self.out("\r\n", end = "\x00")
	
	def proceed(self, username, password):
		self.out(
				"bauth",
				self.name,
				self.user.uid,
				username,
				password,
				end  = "\x00"
			)
		Event({
			"controller": self,
			"interval":    20,
			"delay":       0}, self, "event:ping", "heartbeat")

	def maintain(self, buffer):
		buffer    = buffer.split(":")
		command   = buffer[0]
		buffer    = buffer[1:]
		if self.controller.debug == True:
			print(self.name, command, buffer)
		if hasattr(self, "cmd_" + command.capitalize().replace("_", "")):
			try:
				getattr(self, "cmd_" + command.capitalize().replace("_", ""))(buffer)
			except Exception as e:
				pass
		else:
			if buffer != "":
				pass
		if int(self.limit) > 0:
			if int(self.limited) == 0 and len(self.msg_queue):
				self.out(*self.msg_queue.pop(0))
	
	def out(self, *args, end="\r\n"):
		try:
			self.connection.websocket.send(
					":".join(args) + end
				)
		except (websocket._exceptions.WebSocketConnectionClosedException, BrokenPipeError, socket.error, ConnectionResetError):
			self.controller.leave_Room(self.name)

	def call(self, name, *args):
		try:
			if hasattr(self, "controller"):
				if hasattr(self.controller, name):
					getattr(self.controller, name)(*args)
		except Exception as e:
			print(str(e))

	def get_Authorization(self, username):
		username = username.capitalize()
		if username.isalnum():
			if username == self.users.owner.capitalize():
				return 2
			elif username in self.users.moderators.keys():
				return 1
			else:
				return 0
		else:
			return False

	def room_Check(self):
		if not self.finished:
			self.checking.append(1)
			if self.get_Authorization(self.user.name) >= 1:
				if sum(self.checking) == 4:
					delattr(self, "checking")
					self.finished = True
			else:
				if sum(self.checking) == 3:
					delattr(self, "checking")
					self.finished = True
			if self.finished:
				self.call("room_Finished", self)
		else:
			pass

	##################################################################################################################
	#                                                                                                                #
	# COMMANDS METHODS . . . BITCH!                                                                                  #
	#                                                                                                                #
	##################################################################################################################

	def cmd_Ok(self, buffer):
		#print(buffer)
		if buffer[2].lower() in ["m","c"]:
			if buffer[2].lower() == "c":
				self.closed = True
			self.users.owner = buffer[0].lower()
			if buffer[6] != "":
				for user in buffer[6].split(";"):
					user, permissions = user.split(",")[0], user.split(",")[1]
					self.users.moderators[user.capitalize()] = sorted([k.lower() for k, v in Utilities.flags.moderator.items() if (int(permissions) & v) == v])
			self.time            = buffer[4]
			self.user.ip_Address = buffer[5]
			self.flags           = sorted([k.lower() for k, v in Utilities.flags.room.items() if (int(buffer[-1]) & v) == v])
			self.call("room_Connected", self)
		pass

	def cmd_Inited(self, buffer):
		self.out("blocklist", "block", "", "next", "500")
		self.out("g_participants", "start")
		self.out("getbannedwords")
		self.out("getratelimit")
		
	def cmd_Gparticipants(self, buffer):
		self.users.participants = []
		for user in ":".join(buffer).split(";"):
			user = user.split(":")

			username = user[3]
			if username == "None":
				if user[4] != "None":
					username = "#" + user[4]
				else:
					username = None
			else:
				username = username.capitalize()

			if username != None:
				self.users.participants.append(username)
				if username[0] != "#":
					setattr(self.users.participant, username.capitalize(), makeObject({
							"time":       user[1],
							"session_id": user[0],
							"uid":        user[2]
						}))
		self.room_Check()

	def cmd_Bw(self, buffer):
		words = []
		for x in buffer:
			if x != "":
				words.append(x.split("%2C"))
		self.banned.words = words
		self.room_Check()

	def cmd_Blocklist(self, buffer):
		if len(buffer) and buffer[0] != "":
			blocklist = ":".join(buffer).split(";")
			for ban in blocklist:
				ban = ban.split(":")
				self.banned.users.append(
					makeObject({
						"username":   ban[2],
						"unid":       ban[0],
						"ip_addr":    ban[1],
						"time":       ban[3],
						"moderator":  ban[4]
					}))
			self.out("blocklist", "block", self.banned.users[-1].time, "next", "500")
		else: self.room_Check()

	def cmd_Getratelimit(self, buffer):
		self.limit   = buffer[0]
		self.limited = buffer[1]
		self.room_Check()

	def cmd_Ratelimited(self, buffer):
		self.limited = buffer[1]

	def cmd_Ratelimitset(self, buffer):
		x = buffer[0]
		self.limit = x
		if x > 0:
			self.call("slow_Mode_Enabled", self, x)
		elif x == 0:
			self.call("slow_Mode_Disabled", self)

	def cmd_N(self, buffer):
		self.unum = buffer[0]

	def cmd_Groupflagsupdate(self, buffer):
		self.flags = sorted([k.lower() for k, v in Utilities.flags.room.items() if (int(buffer[-1]) & v) == v])
		self.call("room_Flag_Update", self, self.flags)

	def cmd_Premium(self, buffer):
		state_Table = {
			"INFO_NOT_AVAILABLE": 0,
			"NEVER_BEEN_PREMIUM": 100,
			"GIFTEE":             210,
			"PAYER":              200,
			"EXPIRED_GIFTEE":     111,
			"EXPIRED_PAYER":      101,
			"PENDING":            -1
		}
		if int(buffer[1]) > time.time():
			self.user.format[-1] = True
			self.out("msgbg", "1")
		self.user.premium_Status = state_Table[buffer[0]]

	def cmd_B(self, buffer):
		if buffer[1] != "":
			username = buffer[1].lower()
		else:
			if buffer[2] != "":
				username = "#" + buffer[2].lower()
			else:
				n_regex     = re.search("<n(.*?)/>", buffer[9])
				if not isinstance(n_regex, type(None)):
					username = "!anon{}".format(
							Utilities.Anonymous_User_Id(n_regex.group(1), buffer[3])
						)
				else:
					username = "!anon????"
		if username.lower() != self.user.name.lower():
			p_message = ":".join(buffer[9:])
			p_regex   = re.search("(<n([a-zA-Z0-9]{1,6})\/>)?(<f x([\d]{0,2})([0-9a-fA-F]{6}|[0-9a-fA-F]{3}|[0-9a-fA-F]{1})?=\"([0-9a-zA-Z]*)\">)?", p_message)
			if isinstance(p_regex.group(1), str):
				n_color   = p_regex.group(2)
			else:
				n_color   = "000"
			if isinstance(p_regex.group(3), str):
				f_color   = p_regex.group(5) if p_regex.group(5) != "" else "000" or "000"
				size      = int(p_regex.group(4)) if p_regex.group(4) != "" else 11 or 11
				face      = p_regex.group(6) if p_regex.group(6) != "" else "0" or "0"
			else:
				f_color = "000"
				size = 11
				face = "0"

			self.messages[buffer[5]] = makeObject({
					"buffer":   html.escape(":".join(buffer[0:])),
					"time":        buffer[0],
					"username":    username,
					"uid":         buffer[3],
					"unid":        buffer[4],
					"pid":         buffer[5],
					"ip_addr":     buffer[6],
					"flags":       sorted([k.lower() for k, v in Utilities.flags.message.items() if (int(buffer[7]) & v) == v]),
					"message":  makeObject({
							"content": re.sub("\r|\n", " ", html.unescape(re.sub("<(.*?)>", "", p_message))),
							"color": makeObject({
									"name": n_color,
									"font": f_color
								}),
							"face": face,
							"size": int(size)
						})
				})
	
	def cmd_U(self, buffer):
		post = self.messages.get(buffer[0], None)
		if not isinstance(post, type(None)):
			post.pid = buffer[1]
			if post.message.content:
				pingre = re.search("@{}".format(self.user.name), post.message.content, re.IGNORECASE)
				if hasattr(self.controller, "prefix"):
					if post.message.content[0:len(self.controller.prefix)] == self.controller.prefix:
						command   = post.message.content[len(self.controller.prefix):].split(" ")
						arguments = command[1:]
						command   = command[0].lower()
						self.call("receive_Command", self, post, self.get_Authorization(post.username), command, arguments)
					else:
						if not isinstance(pingre, type(None)):
							self.call("receive_Ping", self, post)
						self.call("receive_Message", self, post, self.get_Authorization(post.username))
				else:
					if not isinstance(pingre, type(None)):
						self.call("receive_Ping", self, post)
					self.call("receive_Message", self, post, self.get_Authorization(post.username))

	def cmd_Showfw(self, buffer):
		self.call("slow_Down", self)

	def cmd_Showtb(self, buffer):
		self.call("restricted", self, int(int(buffer[0])/60))

	def cmd_Tb(self, buffer):
		self.call("restricted_Remainder", self, int(int(buffer[0])/60))

	def cmd_Climited(self, buffer):
		self.call("cmd_Sent_Too_Fast", self, buffer[1], ":".join(buffer[2:]))

	def cmd_Mods(self, buffer):
		old_mods = [u for u in self.users.moderators.keys()]
		new_mods = [x.split(",")[0].capitalize() for x in buffer]
		for mod in old_mods:
			if mod not in new_mods:
				self.call("user_Demodded", self, mod)
		for mod in new_mods:
			if mod not in old_mods:
				self.call("user_Modded", self, mod)
		self.users.moderators = {key:value for key,value in [(x.split(",")[0].capitalize(), sorted([k.lower() for k, v in Utilities.flags.moderator.items() if (int(x.split(",")[1]) & v) == v])) for x in buffer]}

	def cmd_Blocked(self, buffer):
		self.banned.users.append(
				makeObject({
					"unid":      buffer[0],
					"ip_addr":   buffer[1],
					"username":  buffer[2],
					"time":      buffer[4],
					"moderator": buffer[3],
				})
			)
		self.call("user_Banned", self, buffer[2].lower(), buffer[3].lower())

	def cmd_Unblocked(self, buffer):
		unid = buffer[0]
		for ban in self.banned.users:
			if ban.unid == unid:
				self.banned.users.remove(ban)
		self.call("user_Unbanned", self, buffer[2].lower(), buffer[3].lower())

	def cmd_Clearall(self, buffer):
		if buffer[0] == "ok":
			self.call("room_Cleared", self)

	def cmd_Updgroupinfo(self, buffer):
		self.call("room_Updated", self, [x for x in buffer])

	def cmd_Ubw(self, buffer):
		self.out("getbannedwords")
		self.call("bannedwords_Updated", self)

	def cmd_Annc(self, buffer):
		message = re.sub("<(.*?)>", "", buffer[2])
		self.call("receive_Announcement", self, message)

	def cmd_System(self, buffer):
		self.call("group_System_Message", self, buffer)

	def cmd_Private(self, buffer):
		self.call("private_Group_Message", self, buffer)

	def cmd_Group(self, buffer):
		self.call("group_Message", self, buffer)

	def cmd_Participant(self, buffer):
		bit, uid = buffer[0], buffer[1]
		if bit == '0':
			user = buffer[3]
			if user != "None":
				delattr(self.uids, uid)
			if user.capitalize() in self.users.participants:
				self.users.participants.remove(user.capitalize())
			delattr(self.users.participants, user.capitalize())
			self.call("user_Left", self, user, uid)
		if bit == '1':
			user = buffer[3]
			if user != "None":
				setattr(self.uids, uid, user)
				self.uidkeys.append(uid)
				if user.capitalize() not in self.users.participants:
					self.users.participants.append(user.capitalize())
				setattr(self.users.participant, user.capitalize(),
						makeObject({
								"time":       buffer[-1],
								"session_id": buffer[2],
								"uid":        uid
							})
					)
			self.call("user_Joined", self, user, uid)
		if bit == '2':
			if buffer[3] != "None":
				user = buffer[3]
			else:
				if uid in self.uidkeys:
					user = getattr(self.uids, uid) # MARKER HERE
				else:
					user = None
			if uid in self.uidkeys and isinstance(user, str):
				self.users.participants.remove(getattr(self.uids, uid))
				setattr(self.uids, uid, user)
				self.users.participants.append(user.capitalize())
			if uid in self.uidkeys and isinstance(user, type(None)):
				user = getattr(self.uids, uid)
				self.users.participants.remove(user.capitalize())
				delattr(self.uids, uid)
			if uid not in self.uidkeys and isinstance(user, str):
				self.users.participants.append(user.capitalize())
				setattr(self.uids, uid, user)
			self.call("user_Switched", self, user, uid)

	##################################################################################################################
	#                                                                                                                #
	# MISCELLANEOUS METHODS                                                                                          #
	#                                                                                                                #
	##################################################################################################################

	def message(self, *args, conjoin=" ", channel=None, badge=None, flags=[]):
		if len(args):
			def wrap_Message(message, tag=""):
				if isinstance(tag, str) and tag != "":
					message = "<{}>{}</{}>".format(
							tag.lower(),
							message,
							tag.lower()
						)
				return message
			settings       = self.user.format
			extra_Settings = self.user.extra_Format
			if not self.closed and not self.silent:
				channels = {
						"blue":   2048,
						"red":    256,
						"mod":    32768
					}
				badges   = {
						"shield": 64,
						"staff":  128
					}
				message  = conjoin.join([str(a) for a in args]) if isinstance(conjoin, str) else " ".join([str(a) for a in args])
				flags    = [f for f in flags if isinstance(f, int)]
				if isinstance(badge, str) and badge.lower() in ["staff","shield"]:
					flags.append(badges[badge])
				if isinstance(channel, str) and channel.lower() in ["red", "blue", "mod"]:
					flags.append(channels[channel])
				if isinstance(channel, list):
					for chan in channel:
						chan = chan.lower()
						if chan in ["red", "blue", "mod"]:
							flags.append(channels[chan])
				if any(extra_Settings):
					if extra_Settings[0] == True:
						message = wrap_Message(message, "i")
					if extra_Settings[1] == True:
						message = wrap_Message(message, "b")
					if extra_Settings[2] == True:
						message = wrap_Message(message, "u")
				message = "<n{}/><f x{}{}=\"{}\">".format(
								settings[1], settings[2],
								settings[0], settings[3]
							) + message.replace(self.controller.password, "[redacted]")
				if sys.getsizeof(message) < 2900:
					if int(self.limited) == 0:
						self.out("bm", "t12j", str(sum(flags)), message)
					elif int(self.limited) > 0:
						self.msg_queue.append(["bm", "t12j", str(sum(flags)), message])
					else:
						raise CherryMessageError("Failed message on {} ({}). self.limited={}".format(str(self), self.name, self.limited))

	def format_Post(self, font_Face=0, font_Size=0, font_Color="", name_Color="", italic=False, bold=False, underline=False, background=False):
		def assert_Hexadecimal(value):
			if len(value) in [1,3,6]:
				try:
					if 0 <= int(value, 16) <= 16777215:
						return True
					else:
						return False
				except ValueError:
					return False
			else:
				return False
		settings       = self.user.format
		extra_Settings = self.user.extra_Format
		if assert_Hexadecimal(font_Color):
			settings[0] = font_Color
		if assert_Hexadecimal(name_Color):
			settings[1] = name_Color
		if 9 <= int(font_Size) <= (22 if settings[-1] == True else 14):
			if len(str(font_Size)) == 1:
				font_Size = "0" + str(font_Size)
			settings[2] = font_Size
		settings[3] = font_Face
		if any([isinstance(italic, bool), isinstance(bold, bool), isinstance(underline, bool)]) and any([italic, bold, underline]):
			if italic:
				extra_Settings[0] = True
			if bold:
				extra_Settings[1] = True
			if underline:
				extra_Settings[2] = True
		if background == True:
			self.background(True)
		else:
			if settings[-1] == True:
				self.background(False)

	def last_Post(self, match, data="username"):
		post = None
		try:
			post = sorted([x for x in list(self.messages.values()) if getattr(x, data) == match], key=lambda x:x.time, reverse=True)[0]
		except Exception as e:
			pass
		return post

	def background(self, enabled=False):
		booltable = {
			0: False,
			1: True
		}
		if isinstance(enabled, int) and enabled in [0,1]:
			enabled = booltable[enabled]
		if enabled == True:
			self.out("getpremium")
		else:
			self.out("msgbg", "0")
			self.user.format[-1] = False

	def flag_User(self, username):
		_post = self.last_Post(username.lower())
		if _post:
			self.out("g_flag", _post.pnum)
			return True
		else:
			return False

	def moderation(self, username, _action = -1):
		if username.isalnum() and isinstance(_action, int) and -2 <= _action <= 1:
			username = username.lower()
			if _action == -2: # Bans a user
				_post = self.last_Post(username)
				if _post:
					unid, ip = _post.unid, _post.ip_addr
					if username[0] in ["#", "!"]:
						self.out("block", unid, ip, "")
					else:
						self.out("block", unid, ip, username)
					self.banned.users.append(makeObject({
							"unid":      unid,
							"ip_addr":   ip,
							"username":  username,
							"time":      time.time(),
							"moderator": self.user.name
						}))
			if _action == -1: # Unbans them bitches
				_ban = [x for x in self.banned.users if x.username == username]
				if len(_ban) > 0:
					self.out("removeblock", _ban[0].unid, _ban[0].ip_addr, _ban[0].username.lower())
					for x in self.banned.users:
						if x.unid == _ban[0].unid:
							self.banned.users.remove(x)
			if _action == 1 and (self.user.name.lower() == self.users.owner or "edit_mods" in self.users.moderators.get(self.user.name.capitalize(), [])): # Demods user
				if username in self.users.moderators:
					self.out("removemod", username)
			if _action == 2 and (self.user.name.lower() == self.users.owner or "edit_mods" in self.users.moderators.get(self.user.name.capitalize(), [])): # Mods user
				if username not in self.users.moderators:
					self.out("addmod", username)

	def delete(self, username, amount = 0):
		if isinstance(username, str) and username.lower() in self.users.participants:
			_post = self.last_Post(username.lower())
			if _post:
				unid = _post.unid
				if amount == 0:
					self.out("delallmsg", unid, _post.ip_addr, _post.username)
				elif amount > 0:
					for x in range(0, amount):
						_LastPost = self.last_Post(username.lower())
						self.out("delmsg", _LastPost.pid)
						del self.messages[_LastPost.pid]
		elif isinstance(username, str) and username.lower()[0] in ["#", "!"]:
			_post = self.last_Post(username.lower())
			if _post:
				unid = _post.unid
				if amount == 0:
					self.out("delallmsg", unid, _post.ip_addr, "")
				elif amount > 0:
					for x in range(0, _card):
						_LastPost = self.last_Post(username.lower())
						self.out("delmsg", _LastPost.pid)
						del self.messages[_LastPost.pid]
		elif isinstance(username, str) and username.lower() == "*":
			if self.get_Authorization(self.user.name) == 2 or (self.users.moderators.get(self.user.name.capitalize(), None) != None and 'edit_group' in self.users.moderators[self.user.name.capitalize()]):
				self.out("clearall")
			else:
				pass
		else:
			pass

class Pm(object):
	def __init__(self, auth, controller):
		self.controller = controller
		self.time       = None
		self.friend     = makeObject({})
		self.user       = makeObject({
				"uid":          str(int(random.randrange(10**15,(10**16)-1))),
				"name":         auth[1].lower(),
				"ip_addr":      None,
				"premium":      "INFO_NOT_AVAILABLE",
				"format":       [
						"",   # Font colour
						"",   # Name colour
						11,   # Font size
						0,    # Font face
						False # Use bg
					],
				"extra_Format": [
						False, # Italic
						False, # Bold
						False  # Underline
					]
			})
		self.messages   = {}
		self.connection = ConnectionManager("__pms__", "c1", 8080, self)
		if self.connection.alive:
			self.proceed(auth[0])

	def heartbeat(self):
		self.out("\r\n", end = "\x00")

	def proceed(self, auth):
		self.out("tlogin", auth, end="\x00")
		self.call("pm_Connected")
		Event({
			"controller": self,
			"interval":    20,
			"delay":       0}, self, "event:ping", "heartbeat")

	def maintain(self, buffer):
		buffer    = buffer.split(":")
		command   = buffer[0]
		buffer    = buffer[1:]
		if self.controller.debug == True:
			print(command, buffer)
		if hasattr(self, "cmd_" + command.capitalize().replace("_", "")):
			try:
				getattr(self, "cmd_" + command.capitalize().replace("_", ""))(buffer)
			except Exception as e:
				pass
		else:
			if buffer != "":
				pass

	def out(self, *args, end="\r\n"):
		try:
			self.connection.websocket.send(
					":".join(args) + end
				)
		except (websocket._exceptions.WebSocketConnectionClosedException, BrokenPipeError, socket.error, ConnectionResetError):
			self.connection.end_Connection()
			self.call("pm_Disconnected")

	def call(self, name, *args):
		if hasattr(self, "controller"):
			if hasattr(self.controller, name):
				getattr(self.controller, name)(*args)

	##################################################################################################################
	#                                                                                                                #
	# COMMANDS METHODS                                                                                               #
	#                                                                                                                #
	##################################################################################################################

	def cmd_Ok(self, buffer):
		self.out("wl")
		self.call("pm_Initialized")

	def cmd_Denied(self, buffer):
		self.connnection.end_Connection()
		self.call("pm_Denied")

	def cmd_Time(self, buffer):
		self.time = float(buffer[0].strip("\r\n\x00"))

	def cmd_Kickingoff(self, buffer):
		self.connection,end_Connection()
		self.call("pm_Kicked")

	def cmd_Wl(self, buffer):
		self.friend = makeObject({})
		if len(buffer) >= 4:
			for i in range(0, len(buffer), 4):
				friend = buffer[i:(i+4)]
				if friend[2] == "on":
					idle_State = int(friend[3])
					if idle_State >= 1:
						idle_State = True
					if idle_State == 1:
						idle_State = True
					if idle_State == 0:
						idle_State = False
				elif friend[2] == "off":
					idle_State = False
				else:
					idle_State = False
				setattr(self.friend, friend[0].capitalize(), makeObject({
						"status": friend[2],
						"idle": makeObject({
								"status": idle_State,
								"time": int(friend[3])
							}),
						"time": float(friend[1])
					}))

	def cmd_Idleupdate(self, buffer):
		if hasattr(self.friend, buffer[0].capitalize()):
			friend = getattr(self.friend, buffer[0].capitalize())
			if buffer[1] == "0":
				friend.idle.time   = time.time()
				friend.idle.status = True
			else:
				friend.idle.time   = 0
				friend.idle.status = False

	def cmd_Premium(self, buffer):
		state_Table = {
			"INFO_NOT_AVAILABLE": 0,
			"NEVER_BEEN_PREMIUM": 100,
			"GIFTEE":             210,
			"PAYER":              200,
			"EXPIRED_GIFTEE":     111,
			"EXPIRED_PAYER":      101,
			"PENDING":            -1
		}
		if int(buffer[1].replace("\r\n\x00", "")) > int(time.time()):
			self.user.format[-1] = True
			self.out("msgbg", "1")
		self.user.premium = state_Table[buffer[0]]

	def cmd_Wloffline(self, buffer):
		if hasattr(self.friend, buffer[0].capitalize()):
			friend = getattr(self.friend, buffer[0].capitalize())
			friend.idle.time   = 0
			friend.idle.status = False
			friend.time        = float(buffer[1])
			friend.status      = "off"
			self.call("friend_Offline", buffer[0].capitalize())

	def cmd_Wlonline(self, buffer):
		if hasattr(self.friend, buffer[0].capitalize()):
			friend = getattr(self.friend, buffer[0].capitalize())
			friend.idle.time   = 0
			friend.idle.status = False
			friend.time        = float(buffer[1])
			friend.status      = "on"
			self.call("friend_Online", buffer[0].capitalize())

	def cmd_Wldelete(self, buffer):
		if hasattr(self.friend, buffer[0].capitalize()):
			if buffer[1] == "deleted":
				delattr(self.friend, buffer[0].capitalize())
				self.call("friend_Deleted", buffer[0].capitalize(), time.time())

	def cmd_Wladd(self, buffer):
		if not hasattr(self.friend, buffer[0].capitalize()):
			if buffer[1] != "invalid":
				if buffer[1] == "on":
					idle_State = None
					idle_Time  = int(buffer[2])
					if idle_Time > 1:
						idle_State = True
					if idle_Time == 1:
						idle_State = True
					if idle_Time == 0:
						idle_State = False
					time = time.time()
				else:
					idle_State = False
					idle_Time  = 0
					time       = float(buffer[2])
				setattr(self.friend, buffer[0].capitalize(), makeObject({
						"status": buffer[1],
						"idle":   makeObject({
								"status": idle_State,
								"time":   idle_Time
							}),
						"time":   time
					}))
				self.call("friend_Added", buffer[0].capitalize(), time.time())

	def cmd_Msgoff(self, buffer):
		self.cmd_Msg(buffer, extension="offline")

	def cmd_Msg(self, buffer, extension=None):
		base = "pm_Message"
		if isinstance(extension, str):
			base += ("_" + extension.capitalize())
		if buffer[0] == buffer[1]:
			username = buffer[0].lower()
		elif buffer[0] != buffer[1]:
			username = "#" + buffer[0].lower()
		else:
			username = "__anon__"
		time    = float(buffer[3])
		message = self.sanitize(":".join(buffer[5:]))
		self.call(base, username, time, message)

	def cmd_Toofast(self, buffer):
		self.call("too_Fast")

	##################################################################################################################
	#                                                                                                                #
	# MISCELLANEOUS METHODS                                                                                          #
	#                                                                                                                #
	##################################################################################################################

	def sanitize(self, string):
		return html.unescape(re.sub("(<(.*?)>|\r\n\x00)", "", string))

	def message(self, *args, conjoin=" ", username=None):
		if len(args) and isinstance(username, str) and username.isalnum() and 1 <= len(username) <= 20:
			def wrap_Message(message, tag=""):
				if isinstance(tag, str) and tag != "":
					message = "<{}>{}</{}>".format(
							tag.lower(),
							message,
							tag.lower()
						)
				return message
			settings       = self.user.format
			extra_Settings = self.user.extra_Format
			message  = conjoin.join([str(a) for a in args]) if isinstance(conjoin, str) else " ".join([str(a) for a in args])
			if any(extra_Settings):
				if extra_Settings[0] == True:
					message = wrap_Message(messages, "i")
				if extra_Settings[1] == True:
					message = wrap_Message(messages, "b")
				if extra_Settings[2] == True:
					message = wrap_Message(messages, "u")
			message = "<n{}/><m v=\"1\"><g xs0=\"0\"><g x{}s{}=\"{}\">{}</g></g></m>".format(
					str(settings[1]).upper(), str(settings[2]).lower(),
					str(settings[0]),         str(settings[3]),
					message.replace(self.controller.password, "[redacted]")
				)
			if sys.getsizeof(message) < 2900:
				self.out("msg", username.lower(), message)
			else:
				raise CherryMessageError("[PmObject %s, %s] Maximum message byte length exceeded (< 2900)." % (str(self), time.time()))
		else:
			raise CherryMessageError("[PmObject %s, %s] Cannot send null message." % (str(self), time.time()))

	def format_Post(self, font_Face=0, font_Size=0, font_Color="", name_Color="", italic=False, bold=False, underline=False, background=False):
		def assert_Hexadecimal(value):
			if len(value) in [1,3,6]:
				try:
					if 0 <= int(value, 16) <= 16777215:
						return True
					else:
						return False
				except ValueError:
					return False
			else:
				return False
		settings       = self.user.format
		extra_Settings = self.user.extra_Format
		if assert_Hexadecimal(font_Color):
			settings[0] = font_Color
		if assert_Hexadecimal(name_Color):
			settings[1] = name_Color
		if 9 <= int(font_Size) <= (22 if settings[-1] == True else 14):
			if len(str(font_Size)) == 1:
				font_Size = "0" + str(font_Size)
			settings[2] = font_Size
		settings[3] = font_Face
		if any([isinstance(italic, bool), isinstance(bold, bool), isinstance(underline, bool)]) and any([italic, bold, underline]):
			if italic:
				extra_Settings[0] = True
			if bold:
				extra_Settings[1] = True
			if underline:
				extra_Settings[2] = True
		if background == True:
			self.background(True)
		else:
			if settings[-1] == True:
				self.background(False)

	def background(self, enabled=False):
		booltable = {
			0: False,
			1: True
		}
		if isinstance(enabled, int) and enabled in [0,1]:
			enabled = booltable[enabled]
		if enabled == True:
			self.out("getpremium")
		else:
			self.out("msgbg", "0")
			self.user.format[-1] = False

class Blossom(object):
	def __init__(self, username=None, password=None, rooms=None, show_runtime_errors=False, debug=False):
		self.username            = username or input("Username (leave blank for anon): ") or ""
		self.password            = password or getpass.getpass("Password (leave blank for anon): ") or ""
		self.user_auth           = Utilities.pm_Auth(self.username.lower(), self.password)
		self.show_runtime_errors = show_runtime_errors if isinstance(show_runtime_errors, bool) else False
		self.debug               = debug if isinstance(debug, bool) else False
		if self.user_auth[0]:
			if hasattr(self, "seed"):
				getattr(self, "seed")()
			self.pm           = Pm(self.user_auth, self)
			self.rooms        = []
			if isinstance(rooms, list):
				for room in rooms:
					self.join_Room(room)
			else:
				rooms = input("Room names (split by a comma. e.g. room1,room2): ")
				if len(rooms) > 0 and rooms.join("") != "":
					for room in rooms.split(","):
						self.join_Room(room)
			if [r.name.lower() for r in self.rooms] == [r.lower() for r in rooms]:
				if hasattr(self, "seeded"):
					getattr(self, "seeded")()
			while (any([r.connection.alive for r in self.rooms]) or self.pm.connection.alive):
				try:
					time.sleep(1)
				except KeyboardInterrupt:
					exit(0)
			exit(0)
		else:
			if len(self.user_auth) == 3:
				cherry_exception = self.user_auth[2]
				raise CherryError(cherry_exception)
			elif len(self.user_auth) == 2:
				raise CherryAuthError("Authentication error.")

	def call(self, name, *args):
		if hasattr(self, name):
			getattr(self, name)(*args)

	def join_Room(self, name):
		if isinstance(name, str):
			name = name.lower()
			if re.sub("-|_", "q", name).isalnum() and len(name) <= 20:
				room = Room(self.username, self.password, name, self)
				if room.name:
					self.rooms.append(room)

	def leave_Room(self, name):
		room = self.defer(name.lower())
		if room != None:
			room.connection.end_Connection(True)
			del self.rooms[self.rooms.index(room)]

	def defer(self, name):
		name   = name.lower()
		obj    = None
		search = True
		while search == True:
			for room in self.rooms:
				if room.name.lower() == name:
					obj    = room
					search = False
			if obj == None:
				search = False
		if not isinstance(obj, type(None)):
			return obj

	def format(self, font_Face=0, font_Size=0, font_Color="", name_Color="", italic=False, bold=False, underline=False, background=False):
		def Format(object):
			object.format_Post(
					font_Face  = font_Face,
					font_Size  = font_Size,
					font_Color = font_Color,
					name_Color = name_Color,
					italic     = italic,
					bold       = bold,
					underline  = underline,
					background = background
				)
		for room in self.rooms:
			if room != None:
				Format(room)
		Format(self.pm)

	def die(self, close_All_Connections=True, show_Errors=True):
		if close_All_Connections == True:
			for room in self.rooms:
				self.leave_Room(room.name)
			self.pm.connection.end_Connection()
		if show_Errors == True:
			print("\n".join(Utilities.errors))
		exit(0)
