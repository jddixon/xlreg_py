#!/usr/bin/env python3

# test_pkcs7.py

""" Test PKCS7 padding. """

import unittest
import rnglib
from xlattice.crypto import(
    add_pkcs7_padding, pkcs7_padding, strip_pkcs7_padding, AES_BLOCK_SIZE)


class TestPKCS7(unittest.TestCase):
    """ Test PKCS7 padding. """

    def setUp(self):
        """ Initialize the random number generator. """
        self.rng = rnglib.SimpleRNG()

    def test_pkcs7(self):
        """ Actually do the tests. """

        seven = bytearray(7)
        self.rng.next_bytes(seven)

        fifteen = bytearray(15)
        self.rng.next_bytes(fifteen)

        sixteen = bytearray(16)
        self.rng.next_bytes(sixteen)

        seventeen = bytearray(17)
        self.rng.next_bytes(seventeen)

        padding = pkcs7_padding(seven, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE - 7)
        self.assertEqual(padding[0], AES_BLOCK_SIZE - 7)

        padding = pkcs7_padding(fifteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE - 15)
        self.assertEqual(padding[0], AES_BLOCK_SIZE - 15)

        padding = pkcs7_padding(sixteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE)
        self.assertEqual(padding[0], 16)

        padding = pkcs7_padding(seventeen, AES_BLOCK_SIZE)
        expected_len = 2 * AES_BLOCK_SIZE - 17
        self.assertEqual(len(padding), expected_len)
        self.assertEqual(padding[0], expected_len)

        padded_seven = add_pkcs7_padding(seven, AES_BLOCK_SIZE)
        unpadded_seven = strip_pkcs7_padding(padded_seven, AES_BLOCK_SIZE)
        self.assertEqual(seven, unpadded_seven)

        padded_fifteen = add_pkcs7_padding(fifteen, AES_BLOCK_SIZE)
        unpadded_fifteen = strip_pkcs7_padding(padded_fifteen, AES_BLOCK_SIZE)
        self.assertEqual(fifteen, unpadded_fifteen)

        padded_sixteen = add_pkcs7_padding(sixteen, AES_BLOCK_SIZE)
        unpadded_sixteen = strip_pkcs7_padding(padded_sixteen, AES_BLOCK_SIZE)
        self.assertEqual(sixteen, unpadded_sixteen)

        padded_seventeen = add_pkcs7_padding(seventeen, AES_BLOCK_SIZE)
        unpadded_seventeen = strip_pkcs7_padding(
            padded_seventeen, AES_BLOCK_SIZE)
        self.assertEqual(seventeen, unpadded_seventeen)


if __name__ == '__main__':
    unittest.main()
