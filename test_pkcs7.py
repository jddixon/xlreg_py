#!/usr/bin/env python3

# test_pkcs7.py

""" Test PKCS7 padding. """

import unittest
import rnglib
from xlattice.crypto import(
    addPKCS7Padding, pkcs7Padding, stripPKCS7Padding, AES_BLOCK_SIZE)


class TestPKCS7(unittest.TestCase):
    """ Test PKCS7 padding. """

    def setUp(self):
        """ Initialize the random number generator. """
        self.rng = rnglib.SimpleRNG()

    def test_pkcs7(self):
        """ Actually do the tests. """

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
        expected_len = 2 * AES_BLOCK_SIZE - 17
        self.assertEqual(len(padding), expected_len)
        self.assertEqual(padding[0], expected_len)

        padded_seven = addPKCS7Padding(seven, AES_BLOCK_SIZE)
        unpadded_seven = stripPKCS7Padding(padded_seven, AES_BLOCK_SIZE)
        self.assertEqual(seven, unpadded_seven)

        padded_fifteen = addPKCS7Padding(fifteen, AES_BLOCK_SIZE)
        unpadded_fifteen = stripPKCS7Padding(padded_fifteen, AES_BLOCK_SIZE)
        self.assertEqual(fifteen, unpadded_fifteen)

        padded_sixteen = addPKCS7Padding(sixteen, AES_BLOCK_SIZE)
        unpadded_sixteen = stripPKCS7Padding(padded_sixteen, AES_BLOCK_SIZE)
        self.assertEqual(sixteen, unpadded_sixteen)

        padded_seventeen = addPKCS7Padding(seventeen, AES_BLOCK_SIZE)
        unpadded_seventeen = stripPKCS7Padding(
            padded_seventeen, AES_BLOCK_SIZE)
        self.assertEqual(seventeen, unpadded_seventeen)


if __name__ == '__main__':
    unittest.main()
