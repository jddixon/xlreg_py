# xlreg_py/xlReg/errors.py

""" Error codes and messages for Python xlReg package. """

BAD_ATTRS_LINE = -1
BAD_VERSION = -2
CANT_FIND_CLUSTER_BY_ID = -3
CANT_FIND_CLUSTER_BY_NAME = -4
CLUSTER_MEMBER_ID_IN_USE = -5
CLUSTER_MEMBERS_MUST_HAVE_END_POINT = -6
CLUSTER_MEMBER_NAME_IN_USE = -7
CLUSTER_MUST_HAVE_MEMBER = -8
CLUSTER_MUST_HAVE_TWO = -9
ID_ALREADY_IN_USE = -10
ILL_FORMED_CLUSTER = -11
ILL_FORMED_CLUSTER_MEMBER = -12
ILL_FORMED_REG_CRED = -13
MEMBER_MUST_HAVE_END_POINT = -14
MISSING_CLOSING_BRACE = -15
MISSING_CLUSTER_NAME_OR_ID = -16
MISSING_END_POINTS_SECTION = -17
MISSING_MEMBERS_LIST = -18
MISSING_NODE = -19
MISSING_PRIVATE_KEY = -20
MISSING_REG_NODE_LINE = -21
MISSING_SERVER_INFO = -22
NAME_ALREADY_IN_USE = -23
NIL_CLUSTER = -24
NIL_CLUSTER_MEMBER = -25
NIL_NODE = -26
NIL_PRIVATE_KEY = -27
NIL_REGISTRY = -28
NIL_REG_NODE = -29
NIL_TOKEN = -30
RCVD_INVALID_MSG_FOR_STATE = -31
TAG_OUT_OF_RANGE = -32
UNEXPECTED_MSG_TYPE = -33
WRONG_NUMBER_OF_BYTES_IN_ATTRS = -34

XLREG_ERRORS = [
    'badly formed attrs line',
    'badly formated VERSION',
    'cannot find cluster with this ID',
    'cannot find cluster with this name',
    'cluster member id already in use',
    'cluster members must have at least one endPoint',
    'cluster member name already in use',
    'cluster must have a member!',
    'cluster must have at least two members',
    'ID already in use',
    'ill-formed cluster serialization',
    'ill-formed cluster member serialization',
    'ill-formed regCred serialization',
    'member must have at least one endPoint',
    'missing closing brace',
    'missing cluster name or ID',
    'missing endPoints section',
    'missing members list',
    'missing node parameter',
    'missing private key line',
    'missing regNode line',
    'missing server info',
    'name already in use',
    'nil cluster argument',
    'nil cluster member argument',
    'nil node argument',
    'nil private key argument',
    'nil registry argument',
    'nil RegNode argument',
    'nil XLRegMsg_Token argument',
    'invalid msg type for current state',
    'message tag out of range',
    'unexpected message type',
    'wrong number of bytes in attrs',
]
