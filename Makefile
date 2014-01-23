# xlreg_py/Makefile
#
# XXX Need to fetch p.proto from XLREG_PROTO_HOME
#
xlReg/p.pb.go: p.proto
	protoc --python_out=xlReg p.proto

