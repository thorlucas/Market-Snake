import marketsnake.events.event as event
import marketsnake.core as core
from marketsnake.core import Direction

class CrossoverPeriod(core.AbstractPeriod):
	def __init__(self, timestamp, dir):
		super().__init__(timestamp, {'direction' : dir})

class CrossoverEvent(event.Event, core.AbstractTimeSeries):
	def __init__(self, base, signal, alert = None):
		self.base = base
		self.signal = signal
