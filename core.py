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
		if isinstance(other, self.__class__):
			return self.timestamp > other.timestamp
		elif isinstance(other, datetime.datetime):
			return self.timestamp > other
		else:
			raise TypeError('Cannot compare type %s with %s' % (other.__class__, self.__class__))

	## Returns whether or not this is older than the other.
	def __gt__(self, other):
		if isinstance(other, self.__class__):
			return self.timestamp < other.timestamp
		elif isinstance(other, datetime.datetime):
			return self.timestamp < other
		else:
			raise TypeError('Cannot compare incompatible types %s with %s' % (other.__class__, self.__class__))

	## Returns whether or not this is equal to the other.
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.timestamp == other.timestamp
		elif isinstance(other, datetime.datetime):
			return self.timestamp == other
		else:
			raise TypeError('Cannot compare incompatible types %s with %s' % (other.__class__, self.__class__))

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

## Abstract time series that should be inherited from.
#  Basically a sorted collection of periods with some operators.
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
		if isinstance(index, (int, slice)):
			return self.periods[index]
		elif isinstance(index, datetime.datetime):
			return self.periods[self.periods.index(index)]
		else:
			raise KeyError("Cannot fetch item from %s with key type %s" % (self.__class__, type(index)))

	## Returns whether or not the series contains a period.
	#  Note: This does not check the contents or type of period,
	#  only the timestamp.
	#  @param value should be a Period.
	def __contains__(self, value):
		return value in self.periods

	def __len__(self):
		return len(self.periods)

	def __str__(self):
		return '\n'.join([str(p) for p in self.periods])

	## Subtracts time series.
	#  It does this on a value by value basis.
	#  The class taken is that of the left.
	#  Classes are first checked by compatibiltiy (identical values).
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

## Compounds several time series together.
#  This is for things like MACD and Ichimoku that consist of
#  several time series together.
#  Arithematic typically makes no sense for these, so it's
#  not implemented by default.
class CompoundTimeSeries(object):
	## Creates a compound time series.
	#  @param series is a dictionary of named series to be accessed by __getattr__.
	def __init__(self, series, periodType = AbstractPeriod):
		self.series = series
		self.periodType = periodType

	def __getattr__(self, key):
		return self.series[key]

	def __getitem__(self, index):
		# TODO: Implement int version!
		# The int version should account for offset time series, etc.
		# It's going to be a little complex.
		if isinstance(index, datetime.datetime):
			return self.periodType(index, { k : v[index] for k, v in self.series.items()})
		elif isinstance(index, (int, slice)):
			raise NotImplementedError("Fetching by type %s not implemented yet." % type(index))
		else:
			raise TypeError("Cannot fetch item from %s with key type %s" % (self.__class__, type(index)))

	def __str__(self):
		# TODO: Broken for some fuckin' reason
		return '\n'.join([
			'\n'.join([
					str(p) for p in self.series[k]
				])
			for k in self.series
			])

## OHLCV Periods
class PricePeriod(AbstractPeriod):
	def __init__(self, timestamp, open, high, low, close, volume):
		super().__init__(timestamp, {'open' : open, 'high' : high, 'low' : low, 'close' : close, 'volume' : volume})

## OHLCV Series
class PriceTimeSeries(AbstractTimeSeries):
	def __init__(self, periods = None):
		super().__init__(periodType = PricePeriod, periods = periods)