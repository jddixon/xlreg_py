#!/usr/bin/python

# ~/dev/py/xlreg_py/makeTestData

import  os, subprocess, sys, time
if sys.version_info < (3,4):
    import sha3
from Crypto.Cipher import AES
from xlReg import decimalVersion as dv
import rnglib

OPENSSL     = '/usr/bin/openssl'
SSH_KEYGEN  = '/usr/bin/ssh-keygen'
KEY_BITS    = 1024
KEY_BYTES   = KEY_BITS / 8
SHA1_BYTES  = 20

TEST_DATA_DIR  = "./testData"

# REG CRED TEST DATA ################################################
REG_CRED_DATA_DIR = os.path.join(TEST_DATA_DIR, 'regCred')

# HELLO AND REPLY TEST DATA #########################################
MAX_MSG     = KEY_BYTES -1 - 2 * SHA1_BYTES # one more than max value
AES_IV_LEN      = 16
AES_KEY_LEN     = 32
AES_BLOCK_LEN   = 16
SALT_LEN        =  8
VERSION_LEN     =  4

HELLO_DATA_LEN = AES_IV_LEN + AES_KEY_LEN + SALT_LEN + VERSION_LEN
UNPADDED_REPLY_LEN = HELLO_DATA_LEN + SALT_LEN
PADDING_LEN = ((UNPADDED_REPLY_LEN + AES_BLOCK_LEN - 1)/AES_BLOCK_LEN) * \
                AES_BLOCK_LEN - UNPADDED_REPLY_LEN
HELLO_REPLY_LEN = HELLO_DATA_LEN + SALT_LEN + PADDING_LEN

HR_TEST_DIR = os.path.join(TEST_DATA_DIR, 'helloAndReply')
KEY_FILE    = 'key-rsa'
PUBKEY_FILE = 'key-rsa.pub'
PEM_FILE    = 'key-rsa.pem'

PATH_TO_KEY             = os.path.join(HR_TEST_DIR, KEY_FILE)
PATH_TO_PUBKEY          = os.path.join(HR_TEST_DIR, PUBKEY_FILE)
PATH_TO_PEM             = os.path.join(HR_TEST_DIR, PEM_FILE)
PATH_TO_HELLO           = os.path.join(HR_TEST_DIR, 'hello-data')
PATH_TO_REPLY           = os.path.join(HR_TEST_DIR, 'reply-data')
PATH_TO_ENCRYPTED_REPLY = os.path.join(HR_TEST_DIR, 'reply-encrypted')

def makeOrClearTestDir(pathToDir):
    # create test directory if it doesn't exist
    if not os.path.exists(pathToDir):
        os.makedirs(pathToDir)
    else:
        files = os.listdir(pathToDir)
        for file in files:
            pathToFile = os.path.join(pathToDir, file)
            os.unlink(pathToFile)

# REG CRED DATA #####################################################

def makeRegCredData():
    makeOrClearTestDir(REG_CRED_DATA_DIR)

    # Z: copy stockton.regCred.dat to test_dir ----------------------
    with open('stockton.regCred.dat', 'r') as f:
        with open(os.path.join(REG_CRED_DATA_DIR, 'regCred.dat'), 'w') as g:
            data = f.read()
            g.write(data)

# HELLO AND REPLY DATA ##############################################

def makeHelloReplyData(rng):

    makeOrClearTestDir(HR_TEST_DIR)

    # A, B: generate an ssh2 key pair in HR_TEST_DIR -------------------
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
    with open(os.path.join(HR_TEST_DIR, 'version1.str'), 'w') as f:
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
    with open(os.path.join(HR_TEST_DIR, 'iv1'), 'w') as f:
        f.write(iv1)

    # G: write key1 -------------------------------------------------
    key1 = helloData[AES_IV_LEN:AES_IV_LEN + AES_KEY_LEN]
    with open(os.path.join(HR_TEST_DIR, 'key1'), 'w') as f:
        f.write(key1)

    # H: write salt1 ------------------------------------------------
    salt1 = helloData[AES_IV_LEN+AES_KEY_LEN:AES_IV_LEN + AES_KEY_LEN+SALT_LEN]
    with open(os.path.join(HR_TEST_DIR, 'salt1'), 'w') as f:
        f.write(salt1)  # GEEP

    # I: write version1 ---------------------------------------------
    version1 = helloData[AES_IV_LEN+AES_KEY_LEN+SALT_LEN:]
    with open(os.path.join(HR_TEST_DIR, 'version1'), 'w') as f:
        f.write(version1)

    # J: write hello-encrypted --------------------------------------
    # openssl rsautl -in test_dir/data -inkey test_dir/key-rsa.pem -pubin -encrypt -out test_dir/hello-encrypted -oaep
    cmd = [OPENSSL, 'rsautl', '-in', PATH_TO_HELLO,
            '-inkey', PATH_TO_PEM, '-pubin', '-encrypt',
            '-oaep', '-out', os.path.join(HR_TEST_DIR, 'hello-encrypted')]
    result = subprocess.check_call(cmd)
    if result != 0:
        print "OAEP encryption call failed (result: %d); aborting" % result
        system.exit()

    # generate more low-quality random data =========================
    replyData = bytearray(HELLO_DATA_LEN - VERSION_LEN)
    rng.nextBytes(replyData)      # that many random bytes

    # append version number -------------------------------
    dv2 = dv.DecimalVersion(5,6,7,8)
    replyData.append(dv2.getA())
    replyData.append(dv2.getB())
    replyData.append(dv2.getC())
    replyData.append(dv2.getD())

    # append salt1 ----------------------------------------
    for i in range(8):
        replyData.append(salt1[i])

    # append PKCS7 padding --------------------------------
    for i in range(PADDING_LEN):
        replyData.append(PADDING_LEN)

    # K: write reply_data -------------------------------------------
    with open(PATH_TO_REPLY, 'w') as f:
        f.write(replyData)

    # L: write iv2 --------------------------------------------------
    iv2 = replyData[0:AES_IV_LEN]
    with open(os.path.join(HR_TEST_DIR, 'iv2'), 'w') as f:
        f.write(iv2)

    # M: write key2 -------------------------------------------------
    key2 = replyData[AES_IV_LEN:AES_IV_LEN + AES_KEY_LEN]
    with open(os.path.join(HR_TEST_DIR, 'key2'), 'w') as f:
        f.write(key2)

    # N: write salt2 ------------------------------------------------
    salt2 = replyData[AES_IV_LEN+AES_KEY_LEN:AES_IV_LEN + AES_KEY_LEN+SALT_LEN]
    with open(os.path.join(HR_TEST_DIR, 'salt2'), 'w') as f:
        f.write(salt2)

    # O: write version2.str -----------------------------------------
    v2s = dv2.__str__()
    with open(os.path.join(HR_TEST_DIR, 'version2.str'), 'w') as f:
        f.write(v2s)

    # P: write version2 as byte slice -------------------------------
    v2 = bytearray(4)
    v2[0] = dv2.getA()
    v2[1] = dv2.getB()
    v2[2] = dv2.getC()
    v2[3] = dv2.getD()
    with open(os.path.join(HR_TEST_DIR, 'version2'), 'w') as f:
        f.write(v2)

    # Q: write padding as byte slice --------------------------------
    padding = bytearray(PADDING_LEN)
    # the essence of PKCS7:
    for i in range(PADDING_LEN):
        padding[i] = PADDING_LEN
    with open(os.path.join(HR_TEST_DIR, 'padding'), 'w') as f:
        f.write(padding)

    # R: AES-encrypt padded reply as replyEncrypted -----------------
    keyBuff = buffer(key1)
    ivBuff  = buffer(iv1)
    cipher1s = AES.new(keyBuff, AES.MODE_CBC, ivBuff)
    outBuff = buffer(replyData)
    replyEncrypted = cipher1s.encrypt(outBuff)

    # S: write reply-encrypted --------------------------------------
    with open(os.path.join(HR_TEST_DIR, 'reply-encrypted'), 'w') as f:
        f.write(replyEncrypted) # GEEPGEEP

# MAIN ##############################################################

def main():
    # set up random number generator --------------------------------
    now = time.time()
    rng = rnglib.SimpleRNG(now)

    makeRegCredData()
    makeHelloReplyData(rng)

if __name__ == '__main__':
    main()
