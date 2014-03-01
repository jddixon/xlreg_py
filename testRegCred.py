#!/usr/bin/python

# testRegCred.py

import  subprocess, sys, time, unittest
if sys.version_info < (3,4):
    import sha3
from xlReg import regCred as rc
import rnglib as xr

KEY_BITS   = 1024
SHA1_BYTES = 20
SHA3_BYTES = 32

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


    def sillyFun(self):
        print "I do nothing at all"         # JUNK, FOR DEBUGGING 

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

        self._makeOrClearTestDir(dirPath)

        pathToKey = os.path.join(dirPath, keyName + '-rsa')
        pathToPub = os.path.join(dirPath, keyName + '-rsa.pub')
        pathToPem = os.path.join(dirPath, keyName + '-rsa.pem')

        # XXX NONSENSE
        junk = 47000
        # "oh hello there"

        # generate an ssh2 key pair in dirPath 
        cmd = [SSH_KEYGEN, '-q', '-t', 'rsa', '-b', str(KEY_BITS),
                '-N', '',                       # empty passphrase
                '-f', pathToKey]
        result = subprocess.check_call(cmd)
        if result != 0:
            print "ssh-keygen call failed (result: %d); aborting" % result
            system.exit()
    
        # from id_rsa.pub generate the pem version of the public key
    
        # generate 'pem' = PKCS8 version of public key 
        # this command writes to stdout
        f =  open(pathToPem, 'w')
        cmd = [SSH_KEYGEN, '-e', '-m', 'PKCS8', '-f', pathToPub ]
        result = subprocess.check_call(cmd, stdout=f)
        if result != 0:
            print "write to PEM file failed (result: %d); aborting" % result
            f.close()
            system.exit()

        # XXX STUB: READ AND RETURN THE FILES

        f.close()       # GEEP

    def testConstructor(self):

        now = time.time()
        rng = xr.SimpleRNG(now)

        name = 'foo'
        id   = self._buildID(rng)

        #                name, id,  ck, sk, endPoints, version
        rc1 = rc.RegCred(name, id, None, None, None, None)

        self.assertEquals(rc1.getName(), name)
        self.assertEquals(rc1.getID(),   id)


        # round-trip
        # s = rc1.__str__();
        # self.assertEquals("1.2.3.4", s)
        # rc2 = rc.parseRegCred(s)
        # self.assertEquals(rc1.__eq__(rc2), True)
        # self.assertEquals(rc1, rc2)


if __name__ == '__main__':
    unittest.main()
