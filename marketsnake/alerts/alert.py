## Base callback function
class Callback(object):
	## Creates a callback object.
	#  @param callback is a function or a callable class.
	#  @param cbParams are a set of parameters that will be passed when called.
	def __init__(self, callback, cbParams = {}):
		self.callback = callback
		self.cbParams = cbParams

	## Calls the callback function.
	#  @param addParams are additional params added to the callback
	def __call__(self, addParams = {}):
		self.callback(**self.cbParams, **addParams)

class AbstractAlert(object):
	def __init__(self, callback):
		self.callback = callback

	def alert(self):
		self.callback()