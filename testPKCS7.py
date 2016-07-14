#!/usr/bin/env python3

# testPKCS7.py

import os
import subprocess
import sys
import time
import unittest
import rnglib
from xlattice.crypto import (
    addPKCS7Padding, pkcs7Padding, stripPKCS7Padding, AES_BLOCK_SIZE)


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

        padding = pkcs7Padding(seven, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE - 7)
        self.assertEqual(padding[0], AES_BLOCK_SIZE - 7)

        padding = pkcs7Padding(fifteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE - 15)
        self.assertEqual(padding[0], AES_BLOCK_SIZE - 15)

        padding = pkcs7Padding(sixteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE)
        self.assertEqual(padding[0], 16)

        padding = pkcs7Padding(seventeen, AES_BLOCK_SIZE)
        expectedLen = 2 * AES_BLOCK_SIZE - 17
        self.assertEqual(len(padding), expectedLen)
        self.assertEqual(padding[0], expectedLen)

        paddedSeven = addPKCS7Padding(seven, AES_BLOCK_SIZE)
        unpaddedSeven = stripPKCS7Padding(paddedSeven, AES_BLOCK_SIZE)
        self.assertEqual(seven, unpaddedSeven)

        paddedFifteen = addPKCS7Padding(fifteen, AES_BLOCK_SIZE)
        unpaddedFifteen = stripPKCS7Padding(paddedFifteen, AES_BLOCK_SIZE)
        self.assertEqual(fifteen, unpaddedFifteen)

        paddedSixteen = addPKCS7Padding(sixteen, AES_BLOCK_SIZE)
        unpaddedSixteen = stripPKCS7Padding(paddedSixteen, AES_BLOCK_SIZE)
        self.assertEqual(sixteen, unpaddedSixteen)

        paddedSeventeen = addPKCS7Padding(seventeen, AES_BLOCK_SIZE)
        unpaddedSeventeen = stripPKCS7Padding(paddedSeventeen, AES_BLOCK_SIZE)
        self.assertEqual(seventeen, unpaddedSeventeen)


if __name__ == '__main__':
    unittest.main()
