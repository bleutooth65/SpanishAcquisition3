from nose.tools import eq_
import threading
import time
import unittest

from tests.tools import AssertHandler

from devices import tools


class SynchronizedTest(unittest.TestCase):
	class SynchronizedObject(object):
		def __init__(self):
			self.buf = []

			self.lock = threading.RLock()

		@tools.Synchronized()
		def do(self, values):
			for i in xrange(values):
				self.buf.append(i)
				time.sleep(0.001)


	class SynchronizedThread(threading.Thread):
		def __init__(self, obj, times, values):
			threading.Thread.__init__(self)

			self.obj = obj
			self.times = times
			self.values = values

		def run(self):
			for i in xrange(self.times):
				self.obj.do(self.values)


	def testSynchronization(self):
		"""
		Ensure that synchronized methods are called in the correct order.
		"""

		num_threads = 4

		times = 4
		values = 5

		obj = SynchronizedTest.SynchronizedObject()

		thrs = []
		for _ in xrange(num_threads):
			thrs.append(SynchronizedTest.SynchronizedThread(obj, times, values))

		for thr in thrs:
			thr.start()

		for thr in thrs:
			thr.join()

		eq_(obj.buf, range(values) * times * num_threads)


class BlockDataTest(unittest.TestCase):
	def testToAndFromBlockData(self):
		"""
		Routine conversions.
		"""

		binary_data = ''.join([chr(x) for x in xrange(256)])

		data = [
			('', '#10'),
			(' ', '#11 '),
			('something longer', '#216something longer'),
			('and binary data: ' + binary_data, '#3273and binary data: ' + binary_data)
		]

		for d, b in data:
			eq_(tools.BlockData.to_block_data(d), b)
			eq_(tools.BlockData.from_block_data(b), d)

	def testFromIndefiniteBlockData(self):
		"""
		Indefinite inputs.
		"""

		binary_data = ''.join([chr(x) for x in xrange(256)])

		data = [
			('', '#0\n'),
			(' ', '#0 \n'),
			('something longer', '#0something longer\n'),
			('and binary data: ' + binary_data, '#0and binary data: ' + binary_data + '\n')
		]

		for d, b in data:
			eq_(tools.BlockData.from_block_data(b), d)

	def testFromSlightlyBadData(self):
		"""
		Not valid, but parsable inputs.
		"""

		data = [
			('Too ', '#14Too long.', 'extra data ignored: long.'),
		]

		log = AssertHandler()

		for d, b, msg in data:
			log.flush()
			eq_(tools.BlockData.from_block_data(b), d)
			log.assert_logged('warning', msg)

	def testFromBadBlockData(self):
		"""
		Invalid inputs.
		"""

		data = ['', '123Off to a bad start!', '#', '#0', '#0non-terminated',
				'#X123', '#1', '#29', '#24test', '#44444Too short.']

		for b in data:
			try:
				tools.BlockData.from_block_data(b)
			except tools.BlockDataError:
				pass
			else:
				assert False, 'Expected BlockDataError.'


class TestBinaryBinaryEncoder(unittest.TestCase):
	def testEncodeDecode(self):
		"""
		Routine conversions.
		"""

		data = [
			('', '', {}, ''),
			('hex', '\x0e', {}, '0e'),
			('1234', '\x12\x34', {}, '1234'),
			('1234 5678 9 0 a b', '\x12\x34\x56\x78\x90\xab', {}, '1234 5678 90ab'),
			('  ABCDEF   FEDCBA   ', '\xab\xcd\xef\xfe\xdc\xba', {}, 'abcd effe dcba'),
			('0001 0203', '\x00\x01\x02\x03', {}, '0001 0203'),
			('00 010203', '\x00\x01\x02\x03', {'pair_size': 3}, '000102 03'),
			('00 01 02 03', '\x00\x01\x02\x03', {'pair_up': False}, '00010203'),
		]

		for u, e, args, d in data:
			eq_(tools.BinaryEncoder.encode(u), e)
			eq_(tools.BinaryEncoder.decode(e, **args), d)

	def testLength(self):
		"""
		Routine calculations.
		"""

		data = [
			('', 0),
			('nothing', 0),
			('0000', 2),
			('001', 2),
			('data 0101 234', 5),
			('data 0101 2345', 6),
			('data 0101 2345 6', 6),
		]

		for d, l in data:
			eq_(tools.BinaryEncoder.length(d), l)
