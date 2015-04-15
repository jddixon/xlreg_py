#!/usr/bin/python3

# testRSA_OAEP.py

import  os, sys, time, unittest
from Crypto.Cipher    import PKCS1_OAEP
from Crypto.PublicKey import RSA
import  rnglib

import xlReg, xlReg.helloAndReply as hr, xlReg.decimalVersion as dv

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

        # set up private RSA key, get its public part
        KEYBITS = 2048
        ckPriv = RSA.generate(KEYBITS)          # generate a 2K bit private key
        # self.assertEqual(ckPriv.size(), KEYBITS) # fails, may be a little less
        ck      = ckPriv.publickey()
        self.assertEqual(ck.has_private(), False)
        
        # prepare DecimalVersion object, get its value, an int
        w = self.rng.nextInt16(256)
        x = self.rng.nextInt16(256)
        y = self.rng.nextInt16(256)
        z = self.rng.nextInt16(256)
        versionObj    = dv.DecimalVersion(w, x, y, z)
        version       = versionObj.value            # a property
        serialVersion = '%d.%d.%d.%d' % (w, x, y, z)
        versionFromS = dv.parseDecimalVersion(serialVersion)
        self.assertEqual(version, versionFromS.value)

        # CLIENT ENCRYPTS HELLO -------------------------------------

        ciphertext, iv1, key1, salt1 = hr.clientEncryptHello(version, ck)
        self.assertEqual(len(ciphertext),   KEYBITS/8)
        self.assertEqual(len(iv1),          hr.AES_BLOCK_SIZE)
        self.assertEqual(len(key1),         2 * hr.AES_BLOCK_SIZE)
        self.assertEqual(len(salt1),        8)

        # SERVER DECRYPTS HELLO -------------------------------------
        iv1s, key1s, salt1s, versionS = hr.serverDecryptHello(
                ciphertext, ckPriv)
        
        # in real use, the server could require a different version
        self.assertEqual(versionS, version)
        self.assertEqual(iv1,   iv1s)
        self.assertEqual(key1,  key1s)
        self.assertEqual(salt1, salt1s)

        # SERVER PREPARES AND ENCRYPTS REPLY ------------------------


        # CLIENT DECRYPTS REPLY -------------------------------------

if __name__ == '__main__':
    unittest.main()
