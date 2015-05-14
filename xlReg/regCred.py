# xlreg_py/xlreg/regCred.py


import binascii
from Crypto.PublicKey import RSA
from xlattice.util import DecimalVersion, parseDecimalVersion

SHA1_BYTES = 20
SHA2_BYTES = 32

class RegCred(object):

	#type RegCred struct {
	#	Name        string
	#	ID          *xi.NodeID
	#	CommsPubKey *rsa.PublicKey    // CommsKey in token
	#	SigPubKey   *rsa.PublicKey    // SigKey in token
	#	EndPoints   []xt.EndPointI    // MyEnds in token
	#	Version     xu.DecimalVersion // not in token at all

    __slots__ = [ '_name', '_id', '_commsPubKey', '_sigPubKey',
        '_endPoints', '_version',
        ]

    def __init__(self, name, id, ck, sk, endPoints, version):
        if name == None or name == '':
            raise RuntimeError('nil or empty xlReg name')
        self._name = name
        
        if id == None or id == '':
            raise RuntimeError('nil or empty xlReg id')
        idLen = len(id)
        if idLen != SHA1_BYTES and idLen != SHA2_BYTES:
            raise RuntimeError('id length not 20 and not 32')
        self._id = id

        if ck == None or ck == '':
            raise RuntimeError('nil or empty xlReg commsPubKkey')
        # XXX need better check(s)
        self._commsPubKey = ck

        if sk == None or sk == '':
            raise RuntimeError('nil or empty xlReg sigPubKkey')
        # XXX need better chesk(s)
        self._sigPubKey = sk

        if endPoints == None or len(endPoints) == 0 :
            raise RuntimeError('nil or empty endPoints list')
        
        self._endPoints = []
        for ep in endPoints:
            # XXX currently should begin with 'TcpEndPoint: '
            self._endPoints.append(ep)

        if version == None:
            raise RuntimeError('nil regCred version')
        # XXX should check it's a 32-bit value
        self._version = version

    # properties 
    def getName(self):
        return self._name

    def getID(self):
        return self._id

    def getCommsPubKey(self):
        return self._commsPubKey

    def getSigPubKey(self):
        return self._sigPubKey

    def getEndPoints(self):
        return self._endPoints

    def getVersion(self):
        return self._version

    def __str__(self):
        ss = []
        ss.append('regCred {')
        ss.append('    Name: %s' % self._name)

        # uncommenting this yields 'odd length string' error
        #ss.append("    ID: %s" % binascii.b2a_hex(self._id))
        ss.append("    ID: %s" % dumpByteArray(self._id))
       
        ss.append('    CommsPubKey: ' + dumpByteArray(self._commsPubKey))
        ss.append('    SigPubKey: ' + dumpByteArray(self._sigPubKey))
        ss.append('    EndPoints {')
        for ep in self._endPoints :
            ss.append('        ' + ep)
        ss.append('    }')
        ss.append('    Version: ' + self._version.__str__())
        ss.append('}')

        s = "\r\n".join(ss) + "\r\n"
        
        return s

def dumpByteArray(a):
    out = ''
    for b in a:
        pair = "%02x" % b
        out += pair
    return out

def parseRegCred(s):
    """ 
    Expect rather loosely formatted registry credentials but require 
    a space after colon (:) or left brace ({) delimiters. 
    """

    if s == None or s == "" :
        raise RuntimeError("nil or empty regCred string")

    ss = s.split("\r\n")
    lineCount = len(ss)
    global i
    i = 0
    
    
    def skipSAndTrim() :
        """Return the first string containing something other than whitespace"""
        global i
        if i >= lineCount:
            raise RuntimeError('no next line')
        while i < lineCount:
            s = ss[i].strip()
            i += 1
            if len(s) > 0:
                break
        return s
       
    s = skipSAndTrim()
    if s != 'regCred {':
        raise RuntimeError('not a well-formed regCred')
    
    s = skipSAndTrim()
    parts = s.split(': ')
    if len(parts) != 2 or parts[0] != 'Name':
        raise RuntimeError('not a well-formed regCred')
    name = parts[1].strip()
    if len(name) < 1:
        raise RuntimeError('not a well-formed regCred: empty name')

    s = skipSAndTrim()
    parts = s.split(': ')
    if len(parts) != 2 or parts[0] != 'ID':
        raise RuntimeError('not a well-formed regCred')
    hex = parts[1].strip()
    id = binascii.a2b_hex(hex)
    
    # XXX could require length of 20 or 32    
        
    s = skipSAndTrim()
    parts = s.split(': ')
    if len(parts) != 2 or parts[0] != 'CommsPubKey':
        raise RuntimeError('not a well-formed regCred')
    ck = binascii.a2b_hex(parts[1])

    s = skipSAndTrim()
    parts = s.split(': ')
    if len(parts) != 2 or parts[0] != 'SigPubKey':
        raise RuntimeError('not a well-formed regCred')
    sk = binascii.a2b_hex(parts[1])

    s = skipSAndTrim()
    if s != 'EndPoints {':
        raise RuntimeError('not a well-formed regCred')
  
    # collect endPoints
    endPoints = []

    while True :
        s = skipSAndTrim()
        if s == '}':
            break
        parts = s.split(': ')
        if len(parts) != 2 :
            raise RuntimeError('not a well-formed regCred endPoint')
        protocol = parts[0].strip()
        address  = parts[1].strip()
        endPoints.append( '%s: %s' % (protocol, address) )

    s = skipSAndTrim()
    parts = s.split(': ')
    if len(parts) != 2 or parts[0] != 'Version':
        raise RuntimeError('not a well-formed regCred')
    v = parts[1].strip()
    version = parseDecimalVersion(v)
    return  RegCred(name, id, ck, sk, endPoints, version)

