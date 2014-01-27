# xlreg_py/xlReg/errors.py

BAD_ATTRS_LINE = 0
BAD_VERSION = 1
CANT_FIND_CLUSTER_BY_ID = 2
CANT_FIND_CLUSTER_BY_NAME = 3
CLIENT_MUST_HAVE_END_POINT = 4
CLUSTER_MEMBERS_MUST_HAVE_END_POINT = 5
CLUSTER_MUST_HAVE_MEMBER = 6
CLUSTER_MUST_HAVE_TWO = 7
ID_ALREADY_IN_USE = 8
ILL_FORMED_CLUSTER = 9
ILL_FORMED_CLUSTER_MEMBER = 10
ILL_FORMED_REG_CRED = 11
MISSING_CLOSING_BRACE = 12
MISSING_CLUSTER_NAME_OR_ID = 13
MISSING_END_POINTS_SECTION = 14
MISSING_MEMBERS_LIST = 15
MISSING_PRIVATE_KEY = 16
MISSING_REG_NODE_LINE = 17
MISSING_SERVER_INFO = 18
NAME_ALREADY_IN_USE = 19
NIL_CLUSTER = 20
NIL_NODE = 21
NIL_PRIVATE_KEY = 22
NIL_REGISTRY = 23
NIL_REG_NODE = 24
NIL_TOKEN = 25
NO_NODE_NO_KEYS = 26
RCVD_INVALID_MSG_FOR_STATE = 27
TAG_OUT_OF_RANGE = 28
UNEXPECTED_MSG_TYPE = 29
UNKNOWN_CLIENT = 30
WRONG_NUMBER_OF_BYTES_IN_ATTRS = 31

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
