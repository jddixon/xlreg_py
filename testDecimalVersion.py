#!/usr/bin/python

# testDecimalVersion.py

import  sys, unittest
if sys.version_info < (3,4):
    import sha3
from xlReg import decimalVersion as dv

class TestDecimalVErsion (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testEmpty(self):
        junk = dv.DecimalVersion(0)
        pass

    def test4IntConstructor(self):
        pass




if __name__ == '__main__':
    unittest.main()
