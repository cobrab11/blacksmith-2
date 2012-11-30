# coding: utf-8

#  BlackSmith mark.2
# exp_name = "alive_keeper" # /code.py v.x5
#  Id: 16~5c
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def alive_keeper(self):

		def alive_keeper_answer(disp, stanza):
			if stanza:
				Clients[get_disp(disp)].aKeeper = itypes.Number()

		while VarCache["alive"]:
			sleep(360)
			ThrIds = iThr.ThrNames()
			for disp_str, disp in Clients.iteritems():
				if not hasattr(disp, "aKeeper"):
					disp.aKeeper = itypes.Number()
				if disp.aKeeper._int() >= 3:
					disp.aKeeper = itypes.Number()
					ThrName = "%s-%s" % (Types[13], disp_str)
					if ThrName in ThrIds:
						for Thr in iThr.enumerate():
							if Thr._Thread__name == ThrName:
								Thr.kill()
					try:
						composeThr(connectAndDispatch, ThrName, (disp_str,)).start()
					except:
						delivery(AnsBase[28] % (disp_str))
				elif expansions.has_key(self.name):
					disp.aKeeper.plus()
					iq = xmpp.Iq(to = "%s/%s" % (disp_str, GenResource), typ = Types[10])
					iq.addChild(Types[16], namespace = xmpp.NS_PING)
					iq.setID("Bs-i%d" % Info["outiq"].plus())
					CallForResponse(disp_str, iq, alive_keeper_answer)
					del iq
				else:
					raise iThr.ThrKill("exit")
			del ThrIds

	def conf_alive_keeper(self):

		def conf_alive_keeper_answer(disp, stanza, conf):
			if Chats.has_key(conf):
				if xmpp.isErrorNode(stanza):
					if eCodes[6] == stanza.getErrorCode():
						Chats[conf].aKeeper = itypes.Number()
				else:
					Chats[conf].aKeeper = itypes.Number()

		while VarCache["alive"]:
			sleep(360)
			ThrIds = iThr.ThrNames()
			for conf in Chats.itervalues():
				if not (online(conf.disp) and conf.IamHere):
					continue
				if not hasattr(conf, "aKeeper"):
					conf.aKeeper = itypes.Number()
				if conf.aKeeper._int() >= 3:
					conf.aKeeper = itypes.Number()
					TimerName = ejoinTimerName(conf.name)
					if TimerName not in ThrIds:
						try:
							composeTimer(180, ejoinTimer, TimerName, (conf.name,)).start()
						except:
							pass
				elif expansions.has_key(self.name):
					conf.aKeeper.plus()
					iq = xmpp.Iq(to = "%s/%s" % (conf.name, conf.nick), typ = Types[10])
					iq.addChild(Types[18], namespace = xmpp.NS_PING)
					iq.setID("Bs-i%d" % Info["outiq"].plus())
					CallForResponse(conf.disp, iq, conf_alive_keeper_answer, {"conf": conf.name})
					del iq
				else:
					raise iThr.ThrKill("exit")
			del ThrIds

	def start_keepers(self):
		Name1 = self.alive_keeper.func_name
		Name2 = self.conf_alive_keeper.func_name
		for Thr in iThr.enumerate():
			ThrName = Thr._Thread__name
			if ThrName.startswith((Name1, Name2)):
				Thr.kill()
		composeThr(self.alive_keeper, Name1).start()
		composeThr(self.conf_alive_keeper, Name2).start()

	handlers = ((start_keepers, "02si"),)
