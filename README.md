xlreg_py
========

A Python client for the xlReg cluster registry.

**xlReg** is a service which allows you to register a number of machines
which will cooperate as a cluser of intercommunicating servers.  Each 
server has two RSA keys.  One is used for creating digital signatures 
and the other for encrypting communications.  Each joining member 
registers the public key part of each of its RSA private keys with the
xlReg server.  It also registers one or more IP addresses through which
peers or clients can communicate.  The server provides each registrant with 
a unique ID, a 32-byte value.  After machines join the cluster the server
provides each with contact information for the other members of the 
cluster (ID, IP address(es), and sig and comms public keys).  The 
cluster members can then use this information to communicate without
further assistance from the xlReg server.
