## AlphaVantage API class.
#  This will fetch data from alpha vantage using the config file.
#  TODO: Make a generic API class that this inherits from.
#  TODO: Make the API used part of the config.

import configparser
import urllib.request
import json
import datetime
import marketwatch.core as core

class AlphaVantage(object):
	"""docstring for AlphaVantage"""
	def __init__(self, configFile):
		config = configparser.ConfigParser(interpolation=None)
		config.read(configFile)
		APIOpts = config['API']
		TestingOpts = config['TESTING']

		ApiKey = APIOpts['API_KEY']
		
		EndpointBase = APIOpts['ENDPOINT_BASE']
		IntradayBase = APIOpts['FUNC_INTRADAY']

		self.TestMode = TestingOpts.getboolean('TEST_MODE')
		self.TestData = TestingOpts["TEST_DATA"]
		
		## Endpoint for function intraday.
		#  Format with (symbol, interval period in minutes).
		self.FuncIntraday = EndpointBase % (ApiKey, IntradayBase)

	def getJson(self, endpoint):
		with urllib.request.urlopen(endpoint) as req:
			return json.loads(req.read())

	def getFile(self, filename):
		with open(filename, "r") as f:
			return json.loads(f.read())

	## Gets intraday data for a symbol.
	#  @param symbol is a string of the symbol to get.
	#  @param interval is an integer minutes for the interval.
	#  @returns a time series.
	def Intraday(self, symbol, interval):
		series = core.PriceTimeSeries()

		if not self.TestMode:
			json = self.getJson(self.FuncIntraday % (symbol, interval))["Time Series (%dmin)" % (interval)]
		else:
			json = self.getFile(self.TestData)["Time Series (%dmin)" % (interval)]

		for dateString in json:
			timestamp = datetime.datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
			series.emplace(timestamp,
						   open   =	float(json[dateString]["1. open"]),
						   high   =	float(json[dateString]["2. high"]),
						   low    =	float(json[dateString]["3. low"]),
						   close  =	float(json[dateString]["4. close"]),
						   volume =	int(json[dateString]["5. volume"])
			)

		return series