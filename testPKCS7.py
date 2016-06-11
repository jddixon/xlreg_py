#!/usr/bin/env python3

# testPKCS7.py

import os
import subprocess
import sys
import time
import unittest
import rnglib
from xlReg.pkcs7 import PKCS7Padding, AddPKCS7Padding, StripPKCS7Padding
from xlReg import AES_BLOCK_SIZE


class TestPKCS7 (unittest.TestCase):

    def setUp(self):
        self.rng = rnglib.SimpleRNG()

    def testPKCS7(self):
        seven = bytearray(7)
        self.rng.nextBytes(seven)

        fifteen = bytearray(15)
        self.rng.nextBytes(fifteen)

        sixteen = bytearray(16)
        self.rng.nextBytes(sixteen)

        seventeen = bytearray(17)
        self.rng.nextBytes(seventeen)

        padding = PKCS7Padding(seven, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE - 7)
        self.assertEqual(padding[0], AES_BLOCK_SIZE - 7)

        padding = PKCS7Padding(fifteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE - 15)
        self.assertEqual(padding[0], AES_BLOCK_SIZE - 15)

        padding = PKCS7Padding(sixteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE)
        self.assertEqual(padding[0], 16)

        padding = PKCS7Padding(seventeen, AES_BLOCK_SIZE)
        expectedLen = 2 * AES_BLOCK_SIZE - 17
        self.assertEqual(len(padding), expectedLen)
        self.assertEqual(padding[0], expectedLen)

        paddedSeven = AddPKCS7Padding(seven, AES_BLOCK_SIZE)
        unpaddedSeven = StripPKCS7Padding(paddedSeven, AES_BLOCK_SIZE)
        self.assertEqual(seven, unpaddedSeven)

        paddedFifteen = AddPKCS7Padding(fifteen, AES_BLOCK_SIZE)
        unpaddedFifteen = StripPKCS7Padding(paddedFifteen, AES_BLOCK_SIZE)
        self.assertEqual(fifteen, unpaddedFifteen)

        paddedSixteen = AddPKCS7Padding(sixteen, AES_BLOCK_SIZE)
        unpaddedSixteen = StripPKCS7Padding(paddedSixteen, AES_BLOCK_SIZE)
        self.assertEqual(sixteen, unpaddedSixteen)

        paddedSeventeen = AddPKCS7Padding(seventeen, AES_BLOCK_SIZE)
        unpaddedSeventeen = StripPKCS7Padding(paddedSeventeen, AES_BLOCK_SIZE)
        self.assertEqual(seventeen, unpaddedSeventeen)


if __name__ == '__main__':
    unittest.main()
