# xlreg_py/xlReg/helloAndReply.py

from M2Crypto import RSA, BIO
import rnglib

def clientEncryptHello(version, ck):
    """ 
    Generate a client Hello message for public key ck  and 
    DecimalVersion version.
    """

    # generate 56-byte random value = 16 byte IV + 32 byte key + 8 byte salt
    data = bytearray(56)
    rnglib.NextBytes(data)

    # append the version, a DecimalVersion, to the array.  Should be
    # able to use
    #    msg.extend(chunk)
    # or something similar, where chunk is version seen as a bytearray 

    # XXX STUB

    pubKey = str(ck).encode('utf8')
    bio = BIO.MemoryBuffer(pubKey) 
    rsa = RSA.load_pub_key_bio(bio)

    # pcsk#1 with oaep sometimes called pkcs#1 v2.0
    ciphertext = rsa.public_encrypt(data, RSA.pkcs1_oaep_padding)
    return ciphertext


    
    