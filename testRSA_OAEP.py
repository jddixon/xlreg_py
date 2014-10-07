#!/usr/bin/python

# testRSA_OAEP.py

import  os, sys, time, unittest
from Crypto.Cipher    import PKCS1_OAEP
from Crypto.PublicKey import RSA
import  rnglib

KEY_BITS = 2048
KEY_BYTES = KEY_BITS / 8
SHA1_BYTES = 20
MAX_MSG = KEY_BYTES -1 - 2 * SHA1_BYTES # one more than max value

TEST_DIR = 'tmp'

class TestRSA_OAEP (unittest.TestCase):

    def setUp(self):
        now = time.time()
        self.rng = rnglib.SimpleRNG(now)
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)

    def tearDown(self):
        pass

    def testBadMessages(self):
        #try:
        #    dv1 = dv.parseRsaOAEP(None)
        #    self.fail("parsed nil string")
        #except RuntimeError: 
        #    pass
        #try:
        #    dv1 = dv.parseRsaOAEP("")
        #    self.fail("parsed empty string")
        #except RuntimeError: 
        #    pass
        #try:
        #    dv1 = dv.parseRsaOAEP(" \t ")
        #    self.fail("parsed whitespace")
        #except ValueError: 
        #    pass        # GEEP
        pass

    def testEncryptDecrypt(self):

        # message
        msgLen = 30 + self.rng.nextInt16(MAX_MSG - 30) 
        msg   = bytearray(msgLen)
        self.rng.nextBytes(msg)

        # key
        key = RSA.generate(KEY_BITS)
        pubKey = key.publickey()
        pass


if __name__ == '__main__':
    unittest.main()