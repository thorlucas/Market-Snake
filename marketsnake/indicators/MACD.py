import marketsnake.core as core
import marketsnake.indicators.EMA as EMA

class MACDTimeSeries(core.CompoundTimeSeries):
	def __init__(self, base, signal):
		super().__init__({'base':base, 'signal':signal})

	@classmethod
	def fromTimeSeries(cls, timeSeries, longPeriod = 26, shortPeriod = 12, signalPeriod = 9, key = lambda p: p.close):
		emaLong  = EMA.EMATimeSeries.fromTimeSeries(timeSeries, longPeriod,  key = key)
		emaShort = EMA.EMATimeSeries.fromTimeSeries(timeSeries, shortPeriod, key = key)
		baseSeries = emaShort - emaLong

		signalSeries = EMA.EMATimeSeries.fromTimeSeries(baseSeries, signalPeriod, key = lambda p: p.ema)

		return cls(baseSeries, signalSeries)