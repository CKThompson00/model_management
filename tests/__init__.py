"""
Test runner for all tests.
"""

import unittest
import sys

# Discover and run all tests
loader = unittest.TestLoader()
suite = loader.discover('tests', pattern='test_*.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Exit with non-zero code if tests failed
sys.exit(0 if result.wasSuccessful() else 1)
