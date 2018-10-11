import marketsnake.core as core

class SMAPeriod(core.AbstractPeriod):
	def __init__(self, timestamp, sma):
		super().__init__(timestamp, {'sma': sma})

class SMATimeSeries(core.AbstractTimeSeries):
	def __init__(self, period = None, periods = None):
		super().__init__(periodType = SMAPeriod, periods = periods)
		self.period = period

	@classmethod
	def fromTimeSeries(cls, priceSeries, period, key = lambda p: p.close):
		smaSeries = cls(period)

		# The number of periods we will have
		length = len(priceSeries) - period + 1
		for i in range(length):
			smaSeries.emplace(priceSeries[i].timestamp, 
				sma=sum([key(j) for j in priceSeries[i:i+period]])/float(period)
			)

		return smaSeries