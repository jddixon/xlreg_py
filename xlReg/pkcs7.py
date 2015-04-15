# xlreg_py/pkcs7.py

# PKCS7 padding (RFC 5652) pads a message out to a whole multiple
# of the block size, with the value of each byte being the number
# of bytes of padding.  If the data passed is None, the function
# returns a full block of padding.

# def PKCS7Padding(data []byte, blockSize int) (padding []byte) 

def PKCS7Padding(data, blockSize): 
    
    if data and len(data) > 0:
        length = len(data)
    else:
        length = 0
    # we want from 1 to blockSize bytes of padding
    nBlocks = int((length + blockSize - 1) / blockSize)
    rem     = nBlocks*blockSize - length
    if rem == 0 :
        rem = blockSize
    padding = bytearray(rem)
    for i in range(rem):
        padding[i] = rem        # value of each byte is number of bytes
    return padding

# def AddPKCS7Padding(data []byte, blockSize int) (out []byte, err error) {

def AddPKCS7Padding(data, blockSize):
    if blockSize <= 1 :
        raise RuntimeError("ImpossibleBlockSize")
    else:
        padding = PKCS7Padding(data, blockSize)
        if data == None: 
            out = padding
        else:
            out = data + padding
    return out

# The data passed is presumed to have PKCS7 padding.  If possible, return
# a copy of the data without the padding.  Return an error if the padding
# is incorrect.

# def StripPKCS7Padding(data []byte, blockSize int) (out []byte, err error) {

def StripPKCS7Padding(data, blockSize):
    if blockSize <= 1 :
        raise RuntimeError("ImpossibleBlockSize")
    elif data == None:
        raise RuntimeError("NilData")
    
    lenData = len(data)
    if lenData < blockSize :
        raise RuntimeError("IncorrectPKCS7Padding")
    
    # examine the very last byte: it must be padding and must
    # contain the number of padding bytes added
    lenPadding = int(data[-1])
    if lenPadding < 1 or lenData < lenPadding :
        raise RuntimeError("IncorrectPKCS7Padding")
    else: 
        out = data[:lenData-lenPadding]
    return out
