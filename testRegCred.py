#!/usr/bin/python3

# testRegCred.py

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


class TestRegCred (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _buildData(self, count):
        self.assertTrue(count > 0)
        data = bytearray(count)
        return data

    def _buildID(self, rng):
        """ construct an SHA1-like NodeID """
        data = self._buildData(SHA1_BYTES)
        rng.nextBytes(data)
        return data

    def testEmpty(self):
        try:
            rc1 = rc.parseRegCred(None)
            self.fail("parsed nil string")
        except RuntimeError:
            pass

    def _makeOrClearTestDir(self, pathToDir):
        # create test directory if it doesn't exist
        if not os.path.exists(pathToDir):
            os.makedirs(pathToDir)
        else:
            files = os.listdir(pathToDir)
            for file in files:
                pathToFile = os.path.join(pathToDir, file)
                os.unlink(pathToFile)

    def _makeKeyPair(self, rng, dirPath, keyName):
        """
        Create ssh RSA key pair (KEY_NAME-rsa and KEY_NAME-rsa.pub)
        and PEM version of public key (KEY_NAME-rsa.pem) in a directory
        guaranteed to exist and be writable.
        """
        self._makeOrClearTestDir(dirPath)

        pathToKey = os.path.join(dirPath, keyName + '-rsa')
        pathToPub = os.path.join(dirPath, keyName + '-rsa.pub')
        pathToPem = os.path.join(dirPath, keyName + '-rsa.pem')

        # generate an ssh2 key pair in dirPath
        cmd = [SSH_KEYGEN, '-q', '-t', 'rsa', '-b', str(KEY_BITS),
               '-N', '',                       # empty passphrase
               '-f', pathToKey]
        result = subprocess.check_call(cmd)
        if result != 0:
            print("ssh-keygen call failed (result: %d); aborting" % result)
            system.exit()

        # from id_rsa.pub generate the pem version of the public key

        # generate 'pem' = PKCS8 version of public key
        # this command writes to stdout
        f = open(pathToPem, 'w')
        cmd = [SSH_KEYGEN, '-e', '-m', 'PKCS8', '-f', pathToPub]
        result = subprocess.check_call(cmd, stdout=f)
        if result != 0:
            print("write to PEM file failed (result: %d); aborting" % result)
            f.close()
            system.exit()
        f.close()

    def testConstructor(self):

        now = time.time()
        rng = xr.SimpleRNG(now)

        name = 'foo'
        id = self._buildID(rng)

        ckPriv = RSA.generate(1024, os.urandom)
        ckPub = ckPriv.publickey()
        ck = ckPub.exportKey(format='OpenSSH')

        skPriv = RSA.generate(1024, os.urandom)
        skPub = skPriv.publickey()
        sk = skPub.exportKey(format='OpenSSH')

        epCount = 1 + rng.nextInt16(3)  # so from 1 to 3
        endPoints = []
        for i in range(epCount):
            port = 1000 + rng.nextInt16(64000)    # values don't much matter
            ep = "TcpEndPoint: 127.0.0.1:%d" % port
            endPoints.append(ep)

        dv1 = DecimalVersion(rng.nextByte(), rng.nextByte(),
                             rng.nextByte(), rng.nextByte())

        #                name, id,  ck, sk, endPoints, version
        rc1 = rc.RegCred(name, id, ck, sk, endPoints, dv1)

        self.assertEqual(rc1.getName(), name)
        self.assertEqual(rc1.getID(), id)
        self.assertEqual(rc1.getCommsPubKey(), ck)
        self.assertEqual(rc1.getSigPubKey(), sk)
        eps1 = rc1.getEndPoints()
        self.assertEqual(len(endPoints), len(eps1))
        for i in range(len(eps1)):
            self.assertEqual(endPoints[i], eps1[i])

        # ye olde round-trip
        s1 = rc1.__str__()
        rc2 = rc.parseRegCred(s1)
        s2 = rc2.__str__()
        self.assertEqual(s2, s1)

if __name__ == '__main__':
    unittest.main()
