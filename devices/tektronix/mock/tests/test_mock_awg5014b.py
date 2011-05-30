import unittest

from devices.tektronix import awg5014b
from devices.tektronix.mock import mock_awg5014b


# Don't lose the real device.
real_AWG5014B = awg5014b.AWG5014B


def setup():
	# Run the tests with a fake device.
	awg5014b.AWG5014B = mock_awg5014b.MockAWG5014B

# Run this test class.
from devices.tektronix.server_tests.test_awg5014b import AWG5014BTest

def teardown():
	# Restore the real device for any remaining tests.
	awg5014b.AWG5014B = real_AWG5014B


if __name__ == '__main__':
	unittest.main()