import marketsnake.events.event as event
import marketsnake.core as core
from marketsnake.core import Direction

class CrossoverPeriod(core.AbstractPeriod):
	def __init__(self, timestamp, dir):
		super().__init__(timestamp, {'dir' : dir})

class CrossoverEvent(event.Event, core.AbstractTimeSeries):
	def __init__(self, base, signal, alert = None, key = lambda p: p.ema):
		# TODO: Figure out a way to do this...
		#super().__init__(alert = alert)
		#super().__init__(periodType = CrossoverPeriod)
		event.Event.__init__(self, alert = alert)
		core.AbstractTimeSeries.__init__(self, periodType = CrossoverPeriod)

		self.key = key
		self.delta = signal - base
		
		lastSign = key(self.delta[-1]) > 0 # True: Positive, False: Negative or 0
		for p in reversed(self.delta):
			pSign = key(p) > 0
			if pSign is not lastSign:
				self.emplace(p.timestamp, dir = Direction.UP if pSign is True else Direction.DOWN)
			lastSign = pSign