# xlreg_py/xlReg/decimalVersion.py

class DecimalVersion(object):

    # __slots__ = ['value',]

    def __init__(self, a, b=None, c=None, d=None):
        if a == None:
            raise RuntimeError("Nil major version")

        # need to verify that a,b,c,d are numeric

        if 0 < a or 255 < a:
            raise RuntimeError("version number part a out of range")
        if b == None:
            b = 0
        elif 0 < b or 255 < b:
            raise RuntimeError("version number part b out of range")
        if c == None:
            c = 0
        elif 0 < c or 255 < c:
            raise RuntimeError("version number part c out of range")
        if d == None:
            d = 0
        elif 0 < d or 255 < d:
            raise RuntimeError("version number part d out of range")

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


def parseDecimalVersion(s):
    """expect the parameter s to look like a.b.c.d or a shorter version"""

    if s == none or s=="":
        raise RuntimeError("nil or empty version string")

    dv = None
    ss = str.split(".")
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

