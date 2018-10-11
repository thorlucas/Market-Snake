import marketsnake.core as core

class EMAPeriod(core.AbstractPeriod):
	def __init__(self, timestamp, ema):
		super().__init__(timestamp, {'ema': ema})

class EMATimeSeries(core.AbstractTimeSeries):
	def __init__(self, period = None, periods = None):
		super().__init__(periodType = EMAPeriod, periods = periods)
		self.period = period

	@classmethod
	def fromTimeSeries(cls, priceSeries, period, key = lambda p: p.close):
		emaSeries = cls(period)

		# The number of periods we will have
		length = len(priceSeries) - period + 1

		# Calculate the initial SMA
		emaSeries.emplace(priceSeries[length - 1].timestamp,
			ema = sum([key(i) for i in priceSeries[length - 1:]])/float(period)
		)

		# Calculating multiplier
		mult = 2.0 / (period + 1.0)

		# Calculating EMA for remaining periods
		for i in range(length - 2, -1, -1):
			# emaSeries[0] will be the newest calculed period (the previous period)
			emaSeries.emplace(priceSeries[i].timestamp,
				ema = (key(priceSeries[i]) - emaSeries[0].ema)*mult + emaSeries[0].ema
			)
		
		return emaSeries