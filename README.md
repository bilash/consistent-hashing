# consistent-hashing
A simple consistent hashing implementation in Python.

The underlying data structure (a BST) is also implemented from scratch.
I also added a bunch of tests to test the addition and deletion of nodes.

This implementation can be improved by providing virtual nodes for each node for improved load balancing
while distributing keys evenly to nodes.

**Algorithm summary**

Consistent hashing is a hashing technique that maps keys to nodes with the assumption that nodes may join and leave the system at random.
The defining feature is that when a new node joins or an existing node leaves the system, only a small set of key-to-node assignments need to 
change. If we have M keys and N nodes in our system, the expected number of key-to-node re-mapping
is M/N in the event of a node addition or removal. This is a significant improvement from regular hashing, which would probably
re-map almost all the keys when a node leaves or joins.

In traditional hashing we have a fixed number of bins or buckets where we place our keys in. 
In consistent hashing we remove this limitation of a fixed number of bins. Instead, we hash the keys to a virtually unlimited integer space 
and place our bins randomly throughout the same integer space. The bin that is closest to a hashed key in a clockwise direction 
is our target bin for the key! 

Brief description of how consistent hashing works:

1. All keys and nodes are mapped to the same integer space (typically between -2^64 and 2^64, or something like that).
2. If we have N nodes, they are assigned IDs which are essentially the hash numbers of their names.
3. If we have M keys, they hashed to the integer space where the nodes are already mapped to.
4. If a key's hashed number matches a node's ID, then we trivially return the node [ID]. Otherwise, we find the next node ID
 greater than the key's hash value. If no such node ID were found within the range's positive end, we wrap around and return 
 the node ID with the smallest value. Thus we basically form a ring of nodes in the system.
5. When a new node is added to the system it is placed in the hash ring according to it's ID (which is the hash value of it's name).
 All nodes between it's ID and it's previous node's ID are then re-mapped to this node. So, the only node that is affected 
 in the process is the node immediately after this new node in the ring. Some of the keys that would point to that next node 
  will now point to the newly added node. The expected number of keys moved around is M/N.
6. Similarly, when a node leaves the system, all the keys between the leaving node and the node immediately preceeding it 
  are re-mapped to the node immediately following the leaving node in the ring. Again, expected number of keys moved around is M/N.
 
**Implementation summary** 
 
The key ingredient in implementing the consistent hashing algorithm is using an efficient data structure to quickly look up the number 
that is equal to or greater than the key's hash value. One such data structure is the binary search tree (BST). A BST can store all the 
node IDs of existing nodes. When a key needs to be mapped to a node, we simply hash the key and look up the node ID nearest to the hash 
value of the key.

**Slightly-modified BST**
 
 The binary search tree we've used needed a little modification from the standard implementation to make it act like a sorted 
 ring of values. When looking up a value, if we reach the end of the BST and no target node was found we needed 
 to wrap around and return the first node.
 
 **Improved load balancing**
 
 The basic implementation can be improved further to make the key-to-node mapping more balanced by creating virtual nodes for 
  each node and place them randomly throughout the ring. In this setup, each node will have K replicas placed around the king.
  This has the effect of increasing the probability of hitting the nodes more evenly. With fewer nodes the "gaps" between 
   the nodes are wider and may lead to some nodes receiving more keys mapped to them than the others. With replicas of nodes we 
   effectively reduce the gap sizes and increase the probability of hitting the nodes higher in a more uniform manner.
     