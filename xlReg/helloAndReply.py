# xlreg_py/xlReg/helloAndReply.py

from Crypto.Cipher      import PKCS1_OAEP
from Crypto.PublicKey   import RSA
from rnglib             import SystemRNG

__all__ = ['AES_BLOCK_SIZE', 'OAEP_SALT_SIZE',
           'clientEncryptHello','serverDecryptHello',]

AES_BLOCK_SIZE = 16
OAEP_SALT_SIZE = 20     # SHA1 hash length XXX is this in the right place ???

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

    iv1      = bytearray(AES_BLOCK_SIZE)
    rng.nextBytes(iv1)
    key1     = bytearray(2 * AES_BLOCK_SIZE)
    rng.nextBytes(key1)
    salt1    = bytearray(8)
    rng.nextBytes(salt1)
    oaepSalt = bytearray(OAEP_SALT_SIZE)
    # little-endiant version1
    version1 = bytearray(4)
    version1[0] = version         & 0xff
    version1[1] = (version >>  8) & 0xff
    version1[2] = (version >> 16) & 0xff
    version1[3] = (version >> 24) & 0xff

    msg = iv1 + key1 + salt1 + oaepSalt + version1

    # hash defaults to SHA1
    cipher = PKCS1_OAEP.new(ck)     # public key as encryption engine
    ciphertext = cipher.encrypt(msg)

    # DEBUG
    print("msg len is        %2d" % len(msg))
    print("ciphertext len is %2d" % len(ciphertext))
    # END

    # The IV, key, and salt are returned to allow the caller to confirm
    # that the server has decrypted them correctly -- that is, to confirm
    # that whoever is on the other end of the connection knows the RSA
    # private key.

    return ciphertext, iv1, key1, salt1

def serverDecryptHello(ciphertext, ckPriv):
    """ 
    The server uses its private RSA key to decryptthe message from
    the client, discarding the OAEP padding.
    """


    cipher = PKCS1_OAEP.new(ckPriv)
    msg = cipher.decrypt(ciphertext)

    # split the msg into its constituent bits
    iv1s  = msg[0 : AES_BLOCK_SIZE]
    key1s = msg[AES_BLOCK_SIZE : 3 * AES_BLOCK_SIZE ]
    salt1s = msg[3* AES_BLOCK_SIZE : 3 * AES_BLOCK_SIZE + 8]
    vOffset = 3 * AES_BLOCK_SIZE + 8 + OAEP_SALT_SIZE
    vBytes = msg[vOffset : vOffset + 4]
    version =  vBytes[0]        +  \
              (vBytes[1] <<  8) +  \
              (vBytes[2] << 16) +  \
              (vBytes[3] << 24)
    return iv1s, key1s, salt1s, version

def serverEncryptsHelloReply(iv1, key1, salt1, version2s):
    """
    We use iv1, key1 to AES-encrypt our reply.  The server returns salt1
    to show it has decrypted the hello correctly.  It also sends version2
    and salt2.  The server may have overridden the client's requested 
    protocol version.
    
    The method returns the server-selected AES iv2 and key2, salt2, and
    the AES-encrypted ciphertext.
    """
    
    rng = SystemRNG()

    iv2      = bytearray(AES_BLOCK_SIZE)
    rng.nextBytes(iv2)
    key2     = bytearray(2 * AES_BLOCK_SIZE)
    rng.nextBytes(key2)
    salt2    = bytearray(8)
    rng.nextBytes(salt2)
   
    # little-endiant version1
    version2    = bytearray(4)
    version2[0] = version2s         & 0xff
    version2[1] = (version2s >>  8) & 0xff
    version2[2] = (version2s >> 16) & 0xff
    version2[3] = (version2s >> 24) & 0xff
    
    reply = iv2 + key2 + salt2 + salt1 + version2

    # add PKCS7 padding


