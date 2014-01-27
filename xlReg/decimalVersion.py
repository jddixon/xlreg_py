# xlreg_py/xlReg/decimalVersion.py

class DecimalVersion(object):

    # __slots__ = ['value',]

    def __init__(self, aIn, bIn=None, cIn=None, dIn=None):
        if aIn == None:
            raise RuntimeError("Nil major version")
        a = int(aIn)
        if a < 0 or 255 < a:
            raise RuntimeError("version number part a '%d' out of range" % a)
        if bIn == None:
            b = 0
        else:
            b = int(bIn)
            if b < 0 or 255 < b:
                raise RuntimeError("version part b '%d' out of range" % b)
        if cIn == None:
            c = 0
        else:
            c = int(cIn)
            if c < 0 or 255 < c:
                raise RuntimeError("version part c '%d' out of range" % c)
        if dIn == None:
            d = 0
        else:
            d = int(dIn)
            if d < 0 or 255 < d:
                raise RuntimeError("version part d '%d' out of range" % d)

        self.value = (0xff & a)         | ((0xff & b) << 8)  |  \
                     ((0xff & c) << 16) | ((0xff & d) << 24)


    def getA(self):
        return self.value & 0xff
    def getB(self):
        return (self.value >> 8) & 0xff
    def getC(self):
        return (self.value >> 16) & 0xff
    def getD(self):
        return (self.value >> 24) & 0xff

    def __eq__ (self, other):

        if type(other) != DecimalVersion:
            return False
        return self.value == other.value

    def __str__(self):
        a = self.getA()
        b = self.getB()
        c = self.getC()
        d = self.getD()
        if d != 0:
            s = "%d.%d.%d.%d" % (a,b,c,d)
        elif c != 0:
            s = "%d.%d.%d" % (a,b,c)
        else:
            s = "%d.%d" % (a,b)
        return s

def parseDecimalVersion(s):
    """expect the parameter s to look like a.b.c.d or a shorter version"""

    if s == None or s=="":
        raise RuntimeError("nil or empty version string")

    dv = None
    ss = s.split(".")
    length = len(ss)
    if length == 1:
        dv = DecimalVersion(ss[0])
    elif length == 2:
        dv = DecimalVersion(ss[0], ss[1])
    elif length == 3:
        dv = DecimalVersion(ss[0], ss[1], ss[2])
    elif length == 4:
        dv = DecimalVersion(ss[0], ss[1], ss[2], ss[3])
    else:
        raise RuntimeError("not a well-formed DecimalVersion: '%s'" % s)
    return dv

