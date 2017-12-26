import hashlib
import zlib

from data_structures.bst import BST


class ConsistentHasher:
    def __init__(self):
        self.nodes = BST()
        self.id_to_node = dict()

    # Note: we need a deterministic hash function. Python hashlib's hash() is not deterministic, and will return
    # a different hash value on different runs.
    def hash(self, item, limit=4294967295):
        id_hash = hashlib.sha512(item.encode())
        id_hash_int = int.from_bytes(id_hash.digest(), 'big')  # Uses explicit byteorder for system-agnostic reproducibility
        final_id = id_hash_int % limit

        return final_id

    def hash2(self, item):
        return zlib.adler32(str.encode(item)) & 0xffffffff

    def add_node(self, node_name):
        hash_id = self.hash(node_name)
        self.nodes.insert(hash_id)
        self.id_to_node[hash_id] = node_name

    def remove_node(self, node_name):
        hash_id = self.hash(node_name)
        removed = self.nodes.remove(hash_id)
        print('Removed %s: %r' % (node_name, removed))
        return self.id_to_node.pop(hash_id, None)

    def assign_key_to_node(self, key):
        key_hash_id = self.hash(key)
        assigned_node_id = self.nodes.find_next_bigger_elem(key_hash_id)
        if assigned_node_id is None:
            print('Failed to assign key %s (hash = %d) to any node!' % (key, key_hash_id))
            return
        # print('Key %s was hashed to value %d, and was assigned to node %s with id %d' % (key, key_hash_id, self.id_to_node[assigned_node_id], assigned_node_id))
        return self.id_to_node[assigned_node_id]




