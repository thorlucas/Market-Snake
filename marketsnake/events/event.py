class Event(object):
	def __init__(self, alert = None):
		self.alert = alert

	def broadcast(self):
		self.alert.alert()