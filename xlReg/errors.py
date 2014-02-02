# xlreg_py/xlReg/errors.py

BAD_ATTRS_LINE = -1
BAD_VERSION = -2
CANT_FIND_CLUSTER_BY_ID = -3
CANT_FIND_CLUSTER_BY_NAME = -4
CLIENT_MUST_HAVE_END_POINT = -5
CLUSTER_MEMBERS_MUST_HAVE_END_POINT = -6
CLUSTER_MUST_HAVE_MEMBER = -7
CLUSTER_MUST_HAVE_TWO = -8
ID_ALREADY_IN_USE = -9
ILL_FORMED_CLUSTER = -10
ILL_FORMED_CLUSTER_MEMBER = -11
ILL_FORMED_REG_CRED = -12
MISSING_CLOSING_BRACE = -13
MISSING_CLUSTER_NAME_OR_ID = -14
MISSING_END_POINTS_SECTION = -15
MISSING_MEMBERS_LIST = -16
MISSING_PRIVATE_KEY = -17
MISSING_REG_NODE_LINE = -18
MISSING_SERVER_INFO = -19
NAME_ALREADY_IN_USE = -20
NIL_CLUSTER = -21
NIL_NODE = -22
NIL_PRIVATE_KEY = -23
NIL_REGISTRY = -24
NIL_REG_NODE = -25
NIL_TOKEN = -26
NO_NODE_NO_KEYS = -27
RCVD_INVALID_MSG_FOR_STATE = -28
TAG_OUT_OF_RANGE = -29
UNEXPECTED_MSG_TYPE = -30
UNKNOWN_CLIENT = -31
WRONG_NUMBER_OF_BYTES_IN_ATTRS = -32

XLREG_ERRORS = [ \
	'badly formed attrs line',
	'badly formated VERSION',
	'cannot find cluster with this ID',
	'cannot find cluster with this name',
	'client must have at least one endPoint',
	'cluster members must have at least one endPoint',
	'cluster must have a member!',
	'cluster must have at least two members',
	'ID already in use',
	'ill-formed cluster serialization',
	'ill-formed cluster member serialization',
	'ill-formed regCred serialization',
	'missing closing brace',
	'missing cluster name or ID',
	'missing endPoints section',
	'missing members list',
	'missing private key line',
	'missing regNode line',
	'missing server info',
	'name already in use',
	'nil cluster argument',
	'nil node argument',
	'nil private key argument',
	'nil registry argument',
	'nil RegNode argument',
	'nil XLRegMsg_Token argument',
	'no node and no keys to build one',
	'invalid msg type for current state',
	'message tag of of range',
	'unexpected message type',
	'client unknown, not in registry',
	'wrong number of bytes in attrs',
]
