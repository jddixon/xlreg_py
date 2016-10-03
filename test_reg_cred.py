#!/usr/bin/env python3
# testRegCred.py

""" Tests for the RegCred object. """

import os
import subprocess
import sys
import time
import unittest
from Crypto.PublicKey import RSA

from xlattice.util import DecimalVersion
from xlReg import regCred as rc
import rnglib as xr

KEY_BITS = 1024
SHA1_BYTES = 20
SHA2_BYTES = 32

SSH_KEYGEN = '/usr/bin/ssh-keygen'


class TestRegCred(unittest.TestCase):
    """ Test the RegCred (registry credentials) object. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _build_data(self, count):
        """ Create a string of bytes of a given length. """
        self.assertTrue(count > 0)
        data = bytearray(count)
        return data

    def _build_id(self, rng):
        """ construct an SHA1-like NodeID """
        data = self._build_data(SHA1_BYTES)
        rng.nextBytes(data)
        return data

    def test_empty(self):
        """ Verify that the regCred object is not empty. """
        try:
            rc1 = rc.parseRegCred(None)
            self.fail("parsed nil string")
        except RuntimeError:
            pass

    @classmethod
    def _make_or_clear_test_dir(cls, path_to_dir):
        """ Create test directory if it doesn't exist."""

        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
        else:
            files = os.listdir(path_to_dir)
            for file in files:
                path_to_file = os.path.join(path_to_dir, file)
                os.unlink(path_to_file)

    def _make_key_pair(self, rng, dir_path, keyName):
        """
        Create ssh RSA key pair (KEY_NAME-rsa and KEY_NAME-rsa.pub)
        and PEM version of public key (KEY_NAME-rsa.pem) in a directory
        guaranteed to exist and be writable.
        """
        self._make_or_clear_test_dir(dir_path)

        path_to_key = os.path.join(dir_path, keyName + '-rsa')
        path_to_pub = os.path.join(dir_path, keyName + '-rsa.pub')
        path_to_pem = os.path.join(dir_path, keyName + '-rsa.pem')

        # generate an ssh2 key pair in dir_path
        cmd = [SSH_KEYGEN, '-q', '-t', 'rsa', '-b', str(KEY_BITS),
               '-N', '',                       # empty passphrase
               '-f', path_to_key]
        result = subprocess.check_call(cmd)
        if result != 0:
            print("ssh-keygen call failed (result: %d); aborting" % result)
            sys.exit()

        # from id_rsa.pub generate the pem version of the public key

        # generate 'pem' = PKCS8 version of public key
        # this command writes to stdout
        file = open(path_to_pem, 'w')
        cmd = [SSH_KEYGEN, '-e', '-m', 'PKCS8', '-f', path_to_pub]
        result = subprocess.check_call(cmd, stdout=file)
        if result != 0:
            print("write to PEM file failed (result: %d); aborting" % result)
            file.close()
            sys.exit()
        file.close()

    def test_constructor(self):
        """ Test the object constructor."""

        now = time.time()
        rng = xr.SimpleRNG(now)

        name = 'foo'
        id_ = self._build_id(rng)

        ck_priv = RSA.generate(1024, os.urandom)
        ck_pub = ck_priv.publickey()
        ck_ = ck_pub.exportKey(format='OpenSSH')

        sk_priv = RSA.generate(1024, os.urandom)
        sk_pub = sk_priv.publickey()
        sk_ = sk_pub.exportKey(format='OpenSSH')

        ep_count = 1 + rng.nextInt16(3)  # so from 1 to 3
        end_points = []
        for ndx in range(ep_count):
            port = 1000 + rng.nextInt16(64000)    # values don't much matter
            ep_ = "TcpEndPoint: 127.0.0.1:%d" % port
            end_points.append(ep_)

        dv1 = DecimalVersion(rng.nextByte(), rng.nextByte(),
                             rng.nextByte(), rng.nextByte())

        #                name, id_,  ck_, sk_, end_points, version
        rc1 = rc.RegCred(name, id_, ck_, sk_, end_points, dv1)

        self.assertEqual(rc1.getName(), name)
        self.assertEqual(rc1.getID(), id_)
        self.assertEqual(rc1.getCommsPubKey(), ck_)
        self.assertEqual(rc1.getSigPubKey(), sk_)
        eps1 = rc1.getEndPoints()
        self.assertEqual(len(end_points), len(eps1))
        for ndx, ep_ in enumerate(eps1):
            self.assertEqual(ep_, eps1[ndx])

        # ye olde round-trip
        str1 = rc1.__str__()
        rc2 = rc.parseRegCred(str1)
        str2 = rc2.__str__()
        self.assertEqual(str2, str1)

if __name__ == '__main__':
    unittest.main()
