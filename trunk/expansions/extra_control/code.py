# coding: utf-8

#  BlackSmith mark.2
# exp_name = "extra_control" # /code.py v.x9
#  Id: 01~7c
#  Code © (2009-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	sep = chr(38)*2

	def command_turbo(self, stype, source, body, disp):
		if body:
			if self.sep in body:
				ls = body.split(self.sep)
				lslen = len(ls) - 1
				if lslen < 4 or enough_access(source[1], source[2], 7):
					for numb, body in enumerate(ls):
						body = body.strip()
						body = body.split(None, 1)
						cmd = (body.pop(0)).lower()
						if Cmds.has_key(cmd):
							if body:
								body = body[0]
							else:
								body = ""
							Cmds[cmd].execute(stype, source, body, disp)
							if numb not in (0, lslen):
								sleep(2)
						else:
							answer = AnsBase[6]
				else:
					answer = AnsBase[10]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_remote(self, stype, source, body, disp):
		confs = sorted(Chats.keys())
		if body:
			body = body.split(None, 3)
			if len(body) >= 3:
				x = (body.pop(0)).lower()
				if x in confs:
					conf = x
				elif isNumber(x):
					Number = (int(x) - 1)
					if Number >= 0 and Number <= len(confs):
						conf = confs[Number]
					else:
						conf = None
				else:
					conf = None
				if conf:
					typ = (body.pop(0)).lower()
					if typ in ("chat", "чат".decode("utf-8")):
						stype_ = Types[1]
					elif typ in ("private", "приват".decode("utf-8")):
						stype_ = Types[0]
					else:
						stype_ = None
					if stype_:
						cmd = (body.pop(0)).lower()
						if body:
							body = body[0]
						else:
							body = ""
						if 2048 >= len(body):
							if Cmds.has_key(cmd):
								cmd = Cmds[cmd]
								if cmd.isAvalable and cmd.handler:
									Info["cmd"].plus()
									if stype_ == Types[1]:
										disp_ = Chats[conf].disp
									else:
										disp_ = get_disp(disp)
									sThread("command", cmd.handler, (cmd.exp, stype_, (source[0], conf, source[2]), body, disp_), cmd.name)
									cmd.numb.plus()
									source = get_source(source[1], source[2])
									if source:
										cmd.desc.add(source)
								else:
									answer = AnsBase[19] % (cmd.name)
							else:
								answer = AnsBase[6]
						else:
							answer = AnsBase[5]
					else:
						answer = AnsBase[9]
				else:
					answer = AnsBase[8]
			else:
				answer = AnsBase[2]
		else:
			answer = enumerated_list(confs)
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_private(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.split(None, 1)
				cmd = (body.pop(0)).lower()
				if Cmds.has_key(cmd):
					if body:
						body = body[0]
					else:
						body = ""
					Cmds[cmd].execute(Types[0], source, body, disp)
				else:
					answer = AnsBase[6]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	commands = (
		(command_turbo, "turbo", 1,),
		(command_remote, "remote", 8,),
		(command_private, "private", 1,)
					)
