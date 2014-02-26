#!/usr/bin/python

# ~/dev/py/xlreg_py/makeTestData

import  os, subprocess, sys, time
if sys.version_info < (3,4):
    import sha3
from xlReg import decimalVersion as dv
import rnglib

OPENSSL     = '/usr/bin/openssl'
SSH_KEYGEN  = '/usr/bin/ssh-keygen'
KEY_BITS    = 1024
KEY_BYTES   = KEY_BITS / 8
SHA1_BYTES  = 20
MAX_MSG     = KEY_BYTES -1 - 2 * SHA1_BYTES # one more than max value

AES_IV_LEN  = 16
AES_KEY_LEN = 32
SALT_LEN    =  8
VERSION_LEN =  4

HELLO_DATA_LEN = AES_IV_LEN + AES_KEY_LEN + SALT_LEN + VERSION_LEN

TEST_DIR    = './test_dir'           # XXX OVERWRITES this directory
KEY_FILE    = 'key-rsa'
PUBKEY_FILE = 'key-rsa.pub'
PEM_FILE    = 'key-rsa.pem'

PATH_TO_KEY     = os.path.join(TEST_DIR, KEY_FILE)
PATH_TO_PUBKEY  = os.path.join(TEST_DIR, PUBKEY_FILE)
PATH_TO_PEM     = os.path.join(TEST_DIR, PEM_FILE)
PATH_TO_HELLO    = os.path.join(TEST_DIR, 'hello-data')

def main():
    # set up random number generator --------------------------------
    now = time.time()
    rng = rnglib.SimpleRNG(now)

    # create test directory if it doesn't exist ---------------------
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    
    # A, B: generate an ssh2 key pair in TEST_DIR -------------------
    cmd = [SSH_KEYGEN, '-q', '-t', 'rsa', '-b', str(KEY_BITS),
            '-N', '',                       # empty passphrase
            '-f', PATH_TO_KEY]
    result = subprocess.check_call(cmd)
    if result != 0:
        print "ssh-keygen call failed (result: %d); aborting" % result
        system.exit()

    # from id_rsa.pub generate the pem version of the public key

    # C: generate 'pem' = PKCS8 version of public key ---------------
    # this command writes to stdout
    f =  open(PATH_TO_PEM, 'w')
    cmd = [SSH_KEYGEN, '-e', '-m', 'PKCS8', '-f', PATH_TO_PUBKEY, ]
    result = subprocess.check_call(cmd, stdout=f)
    if result != 0:
        print "write to PEM file failed (result: %d); aborting" % result
        f.close()
        system.exit()
    f.close()

    # D: write version1.str -----------------------------------------
    dv1 = dv.DecimalVersion(1,2,3,4)
    v1s = dv1.__str__()
    with open(os.path.join(TEST_DIR, 'version1.str'), 'w') as f:
        f.write(v1s)
    
    # generate low-quality random data ==============================
    helloData = bytearray(HELLO_DATA_LEN - VERSION_LEN)
    rng.nextBytes(helloData)      # that many random bytes
  
    # append version number -------------------------------
    dv1 = dv.DecimalVersion(1,2,3,4)
    # XXX silly but will do for now 
    # XXX version is big-endian
    helloData.append(dv1.getA())
    helloData.append(dv1.getB())
    helloData.append(dv1.getC())
    helloData.append(dv1.getD())

    # E: write hello_data -------------------------------------------
    with open(PATH_TO_HELLO, 'w') as f:
        f.write(helloData)
    # F: write iv1 --------------------------------------------------
    iv1 = helloData[0:AES_IV_LEN]
    with open(os.path.join(TEST_DIR, 'iv1'), 'w') as f:
        f.write(iv1)
   
    # G: write key1 -------------------------------------------------
    key1 = helloData[AES_IV_LEN:AES_IV_LEN + AES_KEY_LEN]
    with open(os.path.join(TEST_DIR, 'key1'), 'w') as f:
        f.write(key1)
   
    # H: write salt1 ------------------------------------------------
    salt1 = helloData[AES_IV_LEN+AES_KEY_LEN:AES_IV_LEN + AES_KEY_LEN+SALT_LEN]
    with open(os.path.join(TEST_DIR, 'salt1'), 'w') as f:
        f.write(salt1)
   
    # I: write version1 ---------------------------------------------
    version1 = helloData[AES_IV_LEN+AES_KEY_LEN+SALT_LEN:]
    with open(os.path.join(TEST_DIR, 'version1'), 'w') as f:
        f.write(version1)

    # J: write hello-encrypted --------------------------------------
    # openssl rsautl -in test_dir/data -inkey test_dir/key-rsa.pem -pubin -encrypt -out test_dir/hello-encrypted -oaep
    cmd = [OPENSSL, 'rsautl', '-in', PATH_TO_HELLO,
            '-inkey', PATH_TO_PEM, '-pubin', '-encrypt',
            '-oaep', '-out', os.path.join(TEST_DIR, 'hello-encrypted')]
    result = subprocess.check_call(cmd)
    if result != 0:
        print "OAEP encryption call failed (result: %d); aborting" % result
        system.exit()

    # K: write version2.str -----------------------------------------
    dv2 = dv.DecimalVersion(5,6,7,8)
    v2s = dv2.__str__()
    with open(os.path.join(TEST_DIR, 'version2.str'), 'w') as f:
        f.write(v2s)
   
    # Z: copy stockton.regCred.dat to test_dir ----------------------
    with open('stockton.regCred.dat', 'r') as f:
        with open(os.path.join(TEST_DIR, 'regCred.dat'), 'w') as g:
            data = f.read()
            g.write(data)

if __name__ == '__main__':
    main()
