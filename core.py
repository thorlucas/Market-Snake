import datetime
import sortedcontainers as sc

## Base class representing a period of anything.
#  This is inherited by price period, or MA period.
class AbstractPeriod(object):
	## Constructs a period with a timestamp.
	#  @param timestamp should be a datetime.datetime object.
	def __init__(self, timestamp, values):
		self.timestamp = timestamp
		self.values = values

	def __getattr__(self, key):
		return self.values[key]

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
		return "%s\n%s" % (datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S"),
			"\n".join(["\t%s: %s" % (k, v) for k, v in self.values.items()]))

	def __sub__(self, other):
		if (self.values.keys() != other.values.keys()):
			raise TypeError("Cannot substract incompatible types %s and %s" % (self.__class__.__name__, other.__class__.__name__))

		return self.__class__(self.timestamp, **{k : (vs - vo) for ((k, vs), (_, vo)) in zip(self.values.items(), other.values.items())})

	def __add__(self, other): 
		if (self.values.keys() != other.values.keys()):
			raise TypeError("Cannot substract incompatible types %s and %s" % (self.__class__.__name__, other.__class__.__name__))
		
		return self.__class__(self.timestamp, **{k : (vs - vo) for ((k, vs), (_, vo)) in zip(self.values.items(), other.values.items())})

class AbstractTimeSeries(object):
	## Constructs a sorted time series.
	#  @param periods is optionally a list of periods to be added.
	def __init__(self, periodType = AbstractPeriod, periods = None):
		## Used for emplacing.
		self.periodType = periodType

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

	def __sub__(self, other):
		# TODO: Wildly inefficient and wasteful, and might rely on a bug
		trimmedSelf = other.periods.intersection(self.periods)
		trimmedOther = self.periods.intersection(other.periods)
		length = len(trimmedSelf)
		return self.__class__(periods=[trimmedSelf[i] - trimmedOther[i] for i in range(length)])

	def __add__(self, other):
		# TODO: Wildly inefficient and wasteful, and might rely on a bug
		trimmedSelf = other.periods.intersection(self.periods)
		trimmedOther = self.periods.intersection(other.periods)
		length = len(trimmedSelf)
		return self.__class__(periods=[trimmedSelf[i] + trimmedOther[i] for i in range(length)])

	## Adds a period to the series.
	def add(self, period):
		self.periods.add(period)

	## Emplaces a period
	def emplace(self, timestamp, **args):
		self.add(self.periodType(timestamp, **args))

class PricePeriod(AbstractPeriod):
	def __init__(self, timestamp, open, high, low, close, volume):
		super().__init__(timestamp, {'open' : open, 'high' : high, 'low' : low, 'close' : close, 'volume' : volume})

class PriceTimeSeries(AbstractTimeSeries):
	def __init__(self, periods = None):
		super().__init__(periodType = PricePeriod, periods = periods)