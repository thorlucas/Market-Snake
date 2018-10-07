import core

class SMAPeriod(core.Period):
	def __init__(self, timestamp, sma):
		super().__init__(timestamp)
		self.sma = sma

	def __str__(self):
		s = """%s
			%f"""
		return s % (super().__str__(), self.sma)

class SMATimeSeries(core.TimeSeries):
	def __init__(self, priceSeries, period):
		super().__init__()

		self.period = period

		# The number of periods we will have
		length = len(priceSeries) - period + 1
		for i in range(length):
			total = 0.0
			for j in range(period):
				total += priceSeries[i + j].close
			total /= period

			self.add(SMAPeriod(priceSeries[i].timestamp, total))
