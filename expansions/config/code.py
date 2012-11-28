# coding: utf-8

#  BlackSmith mark.2
# exp_name = "config" # /code.py v.x5
#  Id: 19~4c
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def get_config(self, config):
		cfg = []
		for s in config.sections():
			cfg.append("[%s]" % (s.upper()))
			for (op, i) in config.items(s):
				cfg.append("%s = %s" % (op.upper(), str(i)))
		return "\r\n".join(cfg)

	ops = ("memory", "incoming", "chat", "private", "tls", "mserve", "getexc", "status", "resource")

	opsGeq = ("MaxMemory", "IncLimit", "ConfLimit", "PrivLimit", "ConTls", "Mserve", "GetExc", "DefStatus", "GenResource")

	def command_config(self, stype, source, body, disp):
		if body:
			ConfigDesc = {}
			for x in body.split():
				if not x.count("="):
					continue
				Name, data = x.split("=", 1)
				if not data:
					continue
				Name = Name.lower()
				for Title in GenCon.sections():
					if Name in GenCon.options(Title):
						if Name in self.ops[:4]:
							if not isNumber(data):
								continue
						elif Name in self.ops[4:-2]:
							if data not in ("True", "False"):
								continue
						elif Name in self.ops[-2:]:
							data = sub_desc(data, {chr(95): chr(32)})
						if not ConfigDesc.has_key(Title):
							ConfigDesc[Title] = {}
						ConfigDesc[Title][Name] = data
			if ConfigDesc:
				for Title in ConfigDesc.keys():
					for (Name, data) in ConfigDesc[Title].items():
						GenCon.set(Title, Name, data)
						if Name not in self.ops[-2:]:
							data = eval(data)
							if Name == self.ops[0]:
								data *= 1024
								data = (32768 if (data and data <= 32768) else data)
						globals()[self.opsGeq[self.ops.index(Name)]] = data
				cat_file(GenConFile, self.get_config(GenCon))
				ls = []
				for Name in ConfigDesc.values():
					ls.extend(Name.keys())
				answer = self.AnsBase[0] % (", ".join([Name.upper() for Name in ls]))
			else:
				answer = self.AnsBase[1]
		else:
			Message(source[0], self.AnsBase[2] + self.get_config(GenCon), disp)
			if stype == Types[1]:
				answer = AnsBase[11]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_cls_config(self, stype, source, body, disp):
		if body:
			list = body.split()
			if len(list) >= 2:
				body = (list.pop(0)).lower()
				if body in ("del", "удалить".decode("utf-8")):
					Name = (list.pop(0)).lower()
					if InstansesDesc.has_key(Name):
						clients = Clients.keys()
						if not Clients.has_key(Name) or len(clients) >= 2:
							if Name == GenDisp:
								clients.remove(GenDisp)
								Gen = choice(clients)
								delivery(self.AnsBase[6] % Gen)
								globals()["GenDisp"], Con = Gen, client_config(GenCon, "CLIENT")[1]
								for x in ConDisp.sections():
									z = client_config(ConDisp, x)
									if Gen == z[0]:
										Con = z[1]
										ConDisp.remove_section(x)
								GenCon.set("CLIENT", "serv", Con[0])
								GenCon.set("CLIENT", "port", Con[1])
								GenCon.set("CLIENT", "host", Con[2])
								GenCon.set("CLIENT", "user", Con[3])
								GenCon.set("CLIENT", "pass", Con[4])
								cat_file(GenConFile, self.get_config(GenCon))
								for x in ConDisp.sections():
									if Gen == client_config(ConDisp, x)[0]:
										ConDisp.remove_section(x)
							if Clients.has_key(Name):
								ThrIds = iThr.ThrNames()
								ThrName = "%s-%s" % (Types[13], Name)
								if ThrName in ThrIds:
									for Thr in iThr.enumerate():
										if Thr._Thread__name == ThrName:
											Thr.kill()
							for conf in Chats.itervalues():
								if conf.disp == Name:
									if online(Name):
										Message(conf.name, self.AnsBase[4], Name)
										sleep(0.2)
									conf.leave(self.AnsBase[5])
									conf.disp = IdleClient()
									conf.save()
									sleep(0.6)
									conf.join()
							if online(Name):
								try:
									Clients[Name].disconnect()
								except:
									pass
							if Flood.has_key(Name):
								del Flood[Name]
							del InstansesDesc[Name]
							for x in ConDisp.sections():
								if Name == client_config(ConDisp, x)[0]:
									ConDisp.remove_section(x)
							cat_file(ConDispFile, self.get_config(ConDisp))
							if Clients.has_key(Name):
								del Clients[Name]
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[7]
					else:
						answer = self.AnsBase[11]
				elif body in ("add", "добавить".decode("utf-8")):
					if len(list) >= 3:
						host = (list.pop(0)).lower()
						user = (list.pop(0)).lower()
						code = (list.pop(0))
						if list:
							port = (list.pop(0))
							if not isNumber(port):
								port = "5222"
						else:
							port = "5222"
						jid = "%s@%s" % (user, host)
						serv = (host)
						if list:
							serv = (list.pop(0)).lower()
						if not Clients.has_key(jid):
							if not InstansesDesc.has_key(jid):
								if connect_client(jid, (serv, port, host, user, code))[0]:
									Numb = itypes.Number()
									Name = "CLIENT%d" % (len(ConDisp.sections()) + Numb.plus())
									while ConDisp.has_section(Name):
										Name = "CLIENT%d" % (len(ConDisp.sections()) + Numb.plus())
									ConDisp.add_section(Name)
									ConDisp.set(Name, "serv", serv)
									ConDisp.set(Name, "port", port)
									ConDisp.set(Name, "host", host)
									ConDisp.set(Name, "user", user)
									ConDisp.set(Name, "pass", code)
									Instance, desc = client_config(ConDisp, Name)
									InstansesDesc[Instance] = desc
									cat_file(ConDispFile, self.get_config(ConDisp))
									try:
										Try_Thr(composeThr(DispatchHandler, "%s-%s" % (Types[13], Instance), (Instance,)), -1)
									except RuntimeError:
										answer = self.AnsBase[8]
									else:
										for conf in Chats.itervalues():
											if Instance == conf.disp:
												conf.join()
										answer = AnsBase[4]
								else:
									answer = self.AnsBase[9]
							else:
								answer = self.AnsBase[10]
						else:
							answer = self.AnsBase[10]
					else:
						answer = AnsBase[2]
				elif body in ("password", "пароль".decode("utf-8")):
					Name = (list.pop(0)).lower()
					if InstansesDesc.has_key(Name):
						if list:
							code = (list.pop(0))
							if list:
								if (list.pop(0)).lower() in ("set", "записать".decode("utf-8")):
									changed = True
						else:
							code, symbols = "", "%s.%s_%s+(!}{#)" % (CharCase[0], CharCase[1], CharCase[2])
							for x in xrange(24):
								code += choice(symbols)
						if locals().has_key("changed"):
							self.answer_register(self, disp, xmpp.Iq(typ = Types[8]), stype, source, code)
						elif online(Name):
							Disp = Clients[Name]
							iq = xmpp.Iq(Types[9] , xmpp.NS_REGISTER, to = Disp.Server, payload = [xmpp.Node("username", payload = [Disp.User]), xmpp.Node("password", payload = [code])])
							Info["outiq"].plus()
							CallForResponse(Disp, iq, self.answer_register, {"stype": stype, "source": source, "code": code})
						else:
							answer = self.AnsBase[12]
					else:
						answer = self.AnsBase[11]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		elif not len(ConDisp.sections()):
			answer = self.AnsBase[3]
		else:
			Message(source[0], self.AnsBase[2] + self.get_config(ConDisp), disp)
			if stype == Types[1]:
				answer = AnsBase[11]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source)

	def answer_register(self, disp, stanza, stype, source, code):
		if xmpp.isResultNode(stanza):
			Name = get_disp(disp)
			if Name == GenDisp:
				GenCon.set("CLIENT", "pass", code)
				cat_file(GenConFile, self.get_config(GenCon))
			else:
				for x in ConDisp.sections():
					if Name == client_config(ConDisp, x)[0]:
						ConDisp.set(x, "pass", code)
						cat_file(ConDispFile, self.get_config(ConDisp))
						break
			serv = InstansesDesc[Name][0]
			port = InstansesDesc[Name][1]
			host = InstansesDesc[Name][2]
			user = InstansesDesc[Name][3]
			InstansesDesc[Name] = (serv, port, host, user, code)
			answer = AnsBase[4]
		else:
			answer = AnsBase[7]
		Answer(answer, stype, source, disp)

	commands = (
		(command_config, "config", 8,),
		(command_cls_config, "client", 8,)
					)
