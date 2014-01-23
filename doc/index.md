# xlreg_py

A Python client for the xlReg cluster registry.

[xlReg](http://jddixon.github.com/xlattice_go/xlReg.html)
is a service which provides unique nodeIDs and allows you to register 
and join clusters.

An xlReg cluster is a number of machines
which will cooperate as a set of intercommunicating servers.  Each 
such server has two RSA keys.  One is used for creating digital signatures 
and the other for encrypting communications.  Each server also has at 
least one IP address used for intra-cluster communications.  In some
clusters each will also have a second IP address used for communications
with clients.

An xlReg client first contacts the server to provide configuration
information including its RSA public keys.  (It does _not_ register
its secret RSA private key.)  The xlReg server then issues the client
with a unique node ID, a 32-byte value.

Once an xlReg client has identified itself to the registry and proved
that it has the private key corresponding to its RSA public key, it 
can register clusters or join existing clusters.

After a machine joins a cluster the server
provides it with contact information for the other members of the 
cluster (ID, IP address(es), and sig and comms public keys).  The 
cluster members can then use this information to communicate without
further assistance from the xlReg server.

Cluster members will normally communicate with one another and clients
using agreed-upon protocols, but xlReg has no knowledge of these 
(although xlReg itself uses Google Protobuf protocols for this purpose).

#xlreg_py# is currently in development.
