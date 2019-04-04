from random import *
class PLD:
	def __init__(self, pdrop):
		self.pdrop = float(pdrop)

	def exe_pld(self):
		rand = random()
		if rand > self.pdrop:
			return True
		else:
			return False
