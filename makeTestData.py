#!/usr/bin/python

# ~/dev/py/xlreg_py/makeTestData

import  os, subprocess, sys, time
if sys.version_info < (3,4):
    import sha3
from xlReg import decimalVersion as dv
import rnglib

SSH_KEYGEN = '/usr/bin/ssh-keygen'
KEY_BITS = 1024
KEY_BYTES = KEY_BITS / 8
SHA1_BYTES = 20
MAX_MSG = KEY_BYTES -1 - 2 * SHA1_BYTES # one more than max value

AES_IV_LEN  = 16
AES_KEY_LEN = 32
SALT_LEN    =  8
VERSION_LEN =  4

MSG_LEN = AES_IV_LEN + AES_KEY_LEN + SALT_LEN + VERSION_LEN

TEST_DIR    = './test_dir'           # XXX OVERWRITES this directory
KEY_FILE    = 'key-rsa'
PUBKEY_FILE = 'key-rsa.pub'
PEM_FILE    = 'key-rsa.pem'

PATH_TO_KEY     = os.path.join(TEST_DIR, KEY_FILE)
PATH_TO_PUBKEY  = os.path.join(TEST_DIR, PUBKEY_FILE)
PATH_TO_PEM     = os.path.join(TEST_DIR, PEM_FILE)
PATH_TO_DATA    = os.path.join(TEST_DIR, 'data')

def main():

    now = time.time()
    rng = rnglib.SimpleRNG(now)
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    
    # generate an ssh2 key pair in TEST_DIR -------------------------
    cmd = [SSH_KEYGEN, '-q', '-t', 'rsa', '-b', '1024',
            '-N', '',                       # empty passphrase
            '-f', PATH_TO_KEY]
    result = subprocess.check_call(cmd)
    if result != 0:
        print "ssh-keygen call failed (result: %d); aborting" % result
        system.exit()

    # from id_rsa.pub generate the pem version of the public key

    # generate pem version of public key --------------------------
    # this command writes to stdout
    f =  open(PATH_TO_PEM, 'w')
    # XXX pkcs8 doesn't work
    cmd = [SSH_KEYGEN, '-f', PATH_TO_PUBKEY, '-e', '-m', 'pem']
    result = subprocess.check_call(cmd, stdout=f)
    if result != 0:
        print "write to PEM file failed (result: %d); aborting" % result
        f.close()
        system.exit()
    f.close()

    # generate low-quality random data ------------------------------
    dv1 = dv.DecimalVersion(1,2,3,4)
    msg = bytearray(MSG_LEN - VERSION_LEN)
    rng.nextBytes(msg)      # that many random bytes
   
    # XXX silly but will do for now 
    # XXX notice this keeps the version little-endian
    msg.append(dv1.getD())
    msg.append(dv1.getC())
    msg.append(dv1.getB())
    msg.append(dv1.getA())

    with open(PATH_TO_DATA, 'w') as f:
        f.write(msg)

if __name__ == '__main__':
    main()
