class Packet:
	def __init__(self, payload, seq, ack, flag_syn=0, flag_ack=0, flag_fin=0):
		self.payload = payload
		self.seq = seq
		self.ack = ack
		self.flag_syn = flag_syn
		self.flag_ack = flag_ack
		self.flag_fin = flag_fin
