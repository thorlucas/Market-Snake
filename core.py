import datetime
import sortedcontainers as sc

## Base class representing a period of anything.
#  This is inherited by price period, or MA period.
class Period(object):
	## Constructs a period with a timestamp.
	#  @param timestamp should be a datetime.datetime object.
	def __init__(self, timestamp):
		self.timestamp = timestamp

	# Operators on the timestamps

	## Returns whether or not this is newer than the other.
	def __lt__(self, other):
		return self.timestamp > other.timestamp

	## Returns whether or not this is older than the other.
	def __gt__(self, other):
		return self.timestamp < other.timestamp

	## Returns whether or not this is equal to the other.
	def __eq__(self, other):
		return self.timestamp == other.timestamp

	def __hash__(self):
		return self.timestamp.__hash__()

	def __str__(self):
		return datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")

## Class representing an OHLCV price period.
class PricePeriod(Period):
	## Constructs a period with timestamp and OHLCV.
	#  @param timestamp should be a datetime.datetime object.
	#  @param open and the others should be numbers.
	def __init__(self, timestamp, open, high, low, close, volume):
		super().__init__(timestamp)
		self.open = open
		self.high = high
		self.low = low
		self.close = close
		self.volume = volume

	def __str__(self):
		s = """%s\n
			O: %f
			H: %f
			L: %f
			C: %f
			V: %d"""
		return s % (datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S"), self.open, self.high, self.low, self.close, self.volume)

class TimeSeries(object):
	## Constructs a sorted time series.
	#  @param periods is optionally a list of periods to be added.
	def __init__(self, periods = None):
		## This is the set of periods.
		#  It remains sorted by timestamp.
		#  Index 0 is the newest period.
		self.periods = sc.SortedSet(periods)

	## Gets a time period.
	#  Index 0 is the newest period.
	def __getitem__(self, index):
		return self.periods[index]

	## Returns whether or not the series contains a period.
	#  Note: This does not check the contents or type of period,
	#  only the timestamp.
	#  @param value should be a Period.
	def __contains__(self, value):
		return value in self.periods

	def __len__(self):
		return len(self.periods)

	def __str__(self):
		s = ""
		for p in self.periods:
			s += str(p) + "\n"
		return s

	## Adds a period to the series.
	def add(self, period):
		self.periods.add(period)