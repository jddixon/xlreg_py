# xlreg_py/xlreg/regCred.py

""" Registry credentials as seen by client. """

import binascii
from xlattice.util import parseDecimalVersion

SHA1_BYTES = 20
SHA2_BYTES = 32


class RegCred(object):
    """ Registry credentials as seen by client. """

    __slots__ = ['_name', '_id', '_comms_pub_key', '_sig_pub_key',
                 '_end_points', '_version',
                 ]

    def __init__(self, name, id_, ck_, sk_, end_points, version):
        """ Initialize the instance. """
        if name is None or name == '':
            raise RuntimeError('nil or empty xlReg name')
        self._name = name

        if id_ is None or id_ == '':
            raise RuntimeError('nil or empty xlReg id')
        id_len = len(id_)
        if id_len != SHA1_BYTES and id_len != SHA2_BYTES:
            raise RuntimeError('id length not 20 and not 32')
        self._id = id_

        if ck_ is None or ck_ == '':
            raise RuntimeError('nil or empty xlReg commsPubKkey')
        # NOTE need better check(line)
        self._comms_pub_key = ck_

        if sk_ is None or sk_ == '':
            raise RuntimeError('nil or empty xlReg sigPubKkey')
        # NOTE need better chesk(s)
        self._sig_pub_key = sk_

        if end_points is None or len(end_points) == 0:
            raise RuntimeError('nil or empty end_points list')

        self._end_points = []
        for ep_ in end_points:
            # NOTE currently should begin with 'TcpEndPoint: '
            self._end_points.append(ep_)

        if version is None:
            raise RuntimeError('nil regCred version')
        # NOTE should check it's a 32-bit value
        self._version = version

    # properties
    def get_name(self):
        """ Return the name. """
        return self._name

    def get_id(self):
        """ Return the regCred ID. """
        return self._id

    def get_comms_pub_key(self):
        """ Return the communications public key. """
        return self._comms_pub_key

    def get_sig_pub_key(self):
        """ Return the public key for digital signatures. """
        return self._sig_pub_key

    def get_end_points(self):
        """ Return the associated EndPoint. """
        return self._end_points

    def get_version(self):
        """ Return the RegCred version number. """
        return self._version

    def __str__(self):
        """ Stringify the object. """
        strings = []
        strings.append('regCred {')
        strings.append('    Name: %s' % self._name)

        # uncommenting this yields 'odd length string' error
        #strings.append("    ID: %s" % binascii.b2a_hex(self._id))
        strings.append("    ID: %s" % dump_byte_array(self._id))

        strings.append(
            '    CommsPubKey: ' +
            dump_byte_array(
                self._comms_pub_key))
        strings.append('    SigPubKey: ' + dump_byte_array(self._sig_pub_key))
        strings.append('    EndPoints {')
        for ep_ in self._end_points:
            strings.append('        ' + ep_)
        strings.append('    }')
        strings.append('    Version: ' + self._version.__str__())
        strings.append('}')

        string = "\r\n".join(strings) + "\r\n"

        return string


def dump_byte_array(aaa):
    """ Stringify a byte array as hex. """
    out = ''
    for bbb in aaa:
        pair = "%02x" % bbb
        out += pair
    return out


def parse_reg_cred(line):
    """
    Expect rather loosely formatted registry credentials but require
    a space after colon (:) or left brace ({) delimiters.
    """

    if line is None or line == "":
        raise RuntimeError("nil or empty regCred string")

    lines = line.split("\r\n")
    line_count = len(lines)

    def skip_line_and_trim(ndx):
        """Return the first string containing something other than whitespace"""
        if ndx >= line_count:
            raise RuntimeError('no next line')
        while ndx < line_count:
            line = lines[ndx].strip()
            ndx += 1
            if len(line) > 0:
                break
        return line

    ndx = 0
    line = skip_line_and_trim(ndx)
    if line != 'regCred {':
        raise RuntimeError('not a well-formed regCred')

    line = skip_line_and_trim(ndx)
    parts = line.split(': ')
    if len(parts) != 2 or parts[0] != 'Name':
        raise RuntimeError('not a well-formed regCred')
    name = parts[1].strip()
    if len(name) < 1:
        raise RuntimeError('not a well-formed regCred: empty name')

    line = skip_line_and_trim(ndx)
    parts = line.split(': ')
    if len(parts) != 2 or parts[0] != 'ID':
        raise RuntimeError('not a well-formed regCred')
    hex_ = parts[1].strip()
    id_ = binascii.a2b_hex(hex_)

    # NOTE could require length of 20 or 32

    line = skip_line_and_trim(ndx)
    parts = line.split(': ')
    if len(parts) != 2 or parts[0] != 'CommsPubKey':
        raise RuntimeError('not a well-formed regCred')
    ck_ = binascii.a2b_hex(parts[1])

    line = skip_line_and_trim(ndx)
    parts = line.split(': ')
    if len(parts) != 2 or parts[0] != 'SigPubKey':
        raise RuntimeError('not a well-formed regCred')
    sk_ = binascii.a2b_hex(parts[1])

    line = skip_line_and_trim(ndx)
    if line != 'EndPoints {':
        raise RuntimeError('not a well-formed regCred')

    # collect end_points
    end_points = []

    while True:
        line = skip_line_and_trim(ndx)
        if line == '}':
            break
        parts = line.split(': ')
        if len(parts) != 2:
            raise RuntimeError('not a well-formed regCred end_point')
        protocol = parts[0].strip()
        address = parts[1].strip()
        end_points.append('%s: %s' % (protocol, address))

    line = skip_line_and_trim(ndx)
    parts = line.split(': ')
    if len(parts) != 2 or parts[0] != 'Version':
        raise RuntimeError('not a well-formed regCred')
    vers = parts[1].strip()
    version = parseDecimalVersion(vers)
    return RegCred(name, id_, ck_, sk_, end_points, version)
