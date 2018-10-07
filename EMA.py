import core

class EMAPeriod(core.Period):
	def __init__(self, timestamp, ema):
		super().__init__(timestamp)
		self.ema = ema

	def __str__(self):
		s = """%s
			%f"""
		return s % (super().__str__(), self.ema)

class EMATimeSeries(core.TimeSeries):
	def __init__(self, priceSeries, period):
		super().__init__()

		self.period = period

		# The number of periods we will have
		length = len(priceSeries) - period + 1

		# Calculate the initial SMA
		total = 0
		for i in range(period):
			total += priceSeries[length - 1 + i].close
		total /= period
		self.add(EMAPeriod(priceSeries[length - 1].timestamp, total))

		# Calculating multiplier
		mult = 2.0 / (period + 1.0)

		# Calculating EMA for remaining periods
		for i in range(length - 2, -1, -1):
			# self[0] will be the newest calculed period (the previous period)
			total = (priceSeries[i].close - self[0].ema)*mult + self[0].ema
			self.add(EMAPeriod(priceSeries[i].timestamp, total))