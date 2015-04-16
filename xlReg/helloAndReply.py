# xlreg_py/xlReg/helloAndReply.py

from Crypto.Cipher      import PKCS1_OAEP, AES
from Crypto.PublicKey   import RSA
from rnglib             import SystemRNG
from xlReg              import AES_BLOCK_SIZE
from xlReg.pkcs7        import AddPKCS7Padding, StripPKCS7Padding

__all__ = ['clientEncryptHello',        'serverDecryptHello',
           'serverEncryptHelloReply',   'clientDecryptHelloReply',
        ]

AES_BLOCK_SIZE = 16

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
    # little-endiant version1
    version1 = bytearray(4)
    version1[0] = version         & 0xff
    version1[1] = (version >>  8) & 0xff
    version1[2] = (version >> 16) & 0xff
    version1[3] = (version >> 24) & 0xff

    msg = iv1 + key1 + salt1 + version1

    # hash defaults to SHA1
    cipher = PKCS1_OAEP.new(ck)     # public key as encryption engine
    ciphertext = cipher.encrypt(msg)

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
    vOffset = 3 * AES_BLOCK_SIZE + 8
    vBytes = msg[vOffset : vOffset + 4]
    version =  vBytes[0]        +  \
              (vBytes[1] <<  8) +  \
              (vBytes[2] << 16) +  \
              (vBytes[3] << 24)
    return iv1s, key1s, salt1s, version

def serverEncryptHelloReply(iv1, key1, salt1, version2s):
    """
    We use iv1, key1 to AES-encrypt our reply.  The server returns salt1
    to show it has decrypted the hello correctly.  It also sends version2
    and salt2.  The server may have overridden the client's requested
    protocol version.

    The method returns the server-selected AES iv2 and key2, salt2, and
    the AES-encrypted ciphertext.
    """

    # The cast to bytes avoids an "argument 1 must be read-only pinned buffer" 
    # error
    iv1 = bytes(iv1)
    key1 = bytes(key1)

    rng = SystemRNG()

    iv2      = bytearray(AES_BLOCK_SIZE)
    rng.nextBytes(iv2)
    iv2      = bytes(iv2)

    key2     = bytearray(2 * AES_BLOCK_SIZE)
    rng.nextBytes(key2)
    key2     = bytes(key2)

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
    paddedReply = AddPKCS7Padding(reply, AES_BLOCK_SIZE)

    # encrypt the reply using iv1, key1, CBC.  
    cipher = AES.new(key1, AES.MODE_CBC, iv1)
    ciphertext = iv1 + cipher.encrypt(paddedReply)

    return iv2, key2, salt2, ciphertext

def clientDecryptHelloReply(ciphertext, iv1, key1):
    """
    Decrypt the server's reply using the IV and key we sent to it.
    Returns iv2, key2, salt2 (8 bytes), and the original salt1.
    The pair iv2/key2 are to be used in future communications.
    Salt1 is returned to help confirm the integrity of the operation.
    """

    iv1  = bytes(iv1)
    key1 = bytes(key1)

    iv = ciphertext[0:AES_BLOCK_SIZE]
    # DEBUG - handle this more sensibly!
    if iv != iv1:
        print("server reply IV is not what was expected")
    # END
    cipher    = AES.new(key1, AES.MODE_CBC, iv1)
    plaintext = cipher.decrypt( ciphertext[AES_BLOCK_SIZE:])
    unpadded  = StripPKCS7Padding(plaintext, AES_BLOCK_SIZE)

    iv2     = unpadded[:AES_BLOCK_SIZE]
    key2    = unpadded[AES_BLOCK_SIZE : 3*AES_BLOCK_SIZE]
    salt2   = unpadded[3*AES_BLOCK_SIZE : 3*AES_BLOCK_SIZE + 8]
    salt1   = unpadded[3*AES_BLOCK_SIZE + 8 : 3*AES_BLOCK_SIZE + 16]
    vBytes  = unpadded[3*AES_BLOCK_SIZE + 16 : 3*AES_BLOCK_SIZE + 20]
    version2= vBytes[0]         |   \
              (vBytes[1] <<  8) |   \
              (vBytes[2] << 16) |   \
              (vBytes[3] << 24)

    return iv2, key2, salt2, salt1, version2

