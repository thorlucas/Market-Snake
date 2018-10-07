import core

class SMAPeriod(core.AbstractPeriod):
	def __init__(self, timestamp, sma):
		super().__init__(timestamp, sma)

class SMATimeSeries(core.AbstractTimeSeries):
	def __init__(self, period, periods = None):
		super().__init__(periods)
		self.period = period

	@classmethod
	def fromPriceSeries(cls, period, priceSeries):
		smaSeries = SMATimeSeries(period)

		# The number of periods we will have
		length = len(priceSeries) - period + 1
		for i in range(length):
			total = 0.0
			for j in range(period):
				total += priceSeries[i + j].close
			total /= period

			smaSeries.add(SMAPeriod(priceSeries[i].timestamp, total))

		return smaSeries