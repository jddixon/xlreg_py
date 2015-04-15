# xlreg_py/xlReg/helloAndReply.py

from Crypto.Cipher      import PKCS1_OAEP
from Crypto.PublicKey   import RSA
from rnglib             import SystemRNG

def clientEncryptHello(version, ck):
    """ 
    Generate a client Hello message for public key ck  and 
    DecimalVersion version.

    version is a 4-byte unsigned int seen as a.b.c.d, in little-endian 
    byte order.

    ck is the server's RSA public key.

    The ciphertext, the message passed to the server, is 80 bytes long.  It 
    is encrypted using the server's RSA public key.  The message encrypted
    consists of 
    * iv1,      16 bytes, a random value
    * key1,     32 bytes, a random value
    * salt1,     8 bytes, a random value
    * oaepSalt, 20 bytes, a random value
    * version1,  4 bytes, the protocol version proposed by the client
    This first four of these are arrays of bytes which are filled with
    random values.

    Returns
    * ciphertext, the data above in encrypted form
    * iv1,      the 16-byte AES initialization vector
    * key1,     the 32-byte AES key
    * salt1,    an 8-byte random value
    """

    rng = SystemRNG()

    iv1      = bytearray(16)
    rnglib.NextBytes(iv1)
    key1     = bytearray(32)
    rnglib.NextBytes(key1)
    salt1    = bytearray(8)
    rnglib.NextBytes(salt1)
    oaepSalt = bytearray(20)
    # encode version1
    version1 = bytearray(4)
    version1[0] = version         & 0xff
    version1[1] = (version >>  8) & 0xff
    version1[2] = (version >> 16) & 0xff
    version1[3] = (version >> 24) & 0xff

    msg = iv1 + key1 + salt1 + oaepSalt + version1

    cipher = PKCS1_OAEP(ck)     # public key as encryption engine
    ciphertext = cipher.encrypt(msg)

    # The IV, key, and salt are returned to allow the lient to confirm
    # that the server has decrypted them correctly -- that is, to confirm
    # that whoever is on the other end of the connection knows the RSA
    # private key.

    return ciphertext, iv1, key1, salt1


    
    
