import core
import EMA

class MACDIndicator(core.CrossoverAnalysis):
	def __init__(self, base, signal):
		super().__init__(base, signal)

	@classmethod
	def fromPriceSeries(cls, priceSeries, baseA = 12, baseB = 26, signal = 9):
		emaA = EMA.EMATimeSeries.fromTimeSeries(priceSeries, baseA)
		emaB = EMA.EMATimeSeries.fromTimeSeries(priceSeries, baseB)
		base = emaA - emaB
		emaS = EMA.EMATimeSeries.fromTimeSeries(base, signal, key = lambda p: p.value)

		return cls(base, emaS)