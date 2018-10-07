import core

class EMAPeriod(core.AbstractPeriod):
	def __init__(self, timestamp, ema):
		super().__init__(timestamp, ema)

class EMATimeSeries(core.AbstractTimeSeries):
	def __init__(self, period, periods = None):
		super().__init__(periods)
		self.period = period

	@classmethod
	def fromTimeSeries(cls, priceSeries, period, key = lambda p: p.close):
		emaSeries = cls(period)

		# The number of periods we will have
		length = len(priceSeries) - period + 1

		# Calculate the initial SMA
		total = 0
		for i in range(period):
			total += key(priceSeries[length - 1 + i])
		total /= period
		emaSeries.add(EMAPeriod(priceSeries[length - 1].timestamp, total))

		# Calculating multiplier
		mult = 2.0 / (period + 1.0)

		# Calculating EMA for remaining periods
		for i in range(length - 2, -1, -1):
			# self[0] will be the newest calculed period (the previous period)
			total = (key(priceSeries[i]) - emaSeries[0].value)*mult + emaSeries[0].value
			emaSeries.add(EMAPeriod(priceSeries[i].timestamp, total))

		return emaSeries