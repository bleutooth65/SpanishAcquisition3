import functools

"""
Generic tools.
"""


def sift(items, cls):
	"""
	Filter out items which are not instances of cls.
	"""

	return [item for item in items if isinstance(item, cls)]


class Enum(set):
	"""
	An enumerated type.

	>>> e = Enum(['a', 'b', 'c'])
	>>> e.a
	'a'
	>>> e.d
	...
	AttributeError: 'Enum' object has no attribute 'd'
	"""

	def __getattribute__(self, name):
		if name in self:
			return name
		else:
			return set.__getattribute__(self, name)


class PubDict(dict):
	"""
	A locking, publishing dictionary.
	"""

	def __init__(self, lock, pub, topic, *args, **kwargs):
		"""
		lock: A re-entrant lock which supports context management.
		pub: A PubSub publisher.
		topic: The topic on which to send messages.
		"""

		dict.__init__(self, *args, **kwargs)

		self.lock = lock
		self.pub = pub
		self.topic = topic

	def __setitem__(self, k, v):
		"""
		Note: Values cannot be overwritten, to ensure that removal is always handled explicitly.
		"""

		with self.lock:
			if k in self:
				raise KeyError(k)

			if v is None:
				raise ValueError('No value given.')

			dict.__setitem__(self, k, v)

			self.pub.sendMessage('{0}.added'.format(self.topic), name=k, value=v)

	def __delitem__(self, k):
		with self.lock:
			dict.__delitem__(self, k)

			self.pub.sendMessage('{0}.removed'.format(self.topic), name=k)


class Synchronized(object):
	"""
	A decorator for methods which must be synchronized within an object instance.
	"""

	@staticmethod
	def __call__(f):
		@functools.wraps(f)
		def decorated(self, *args, **kwargs):
			with self.lock:
				return f(self, *args, **kwargs)

		return decorated


class Without(object):
	"""
	A no-op object for use with "with".
	"""

	def __enter__(self, *args, **kwargs):
		return None

	def __exit__(self, *args, **kwargs):
		return False