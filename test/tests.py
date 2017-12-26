import unittest

from app.consistent_hashing import ConsistentHasher
from data_structures.bst import BST


class BstTest(unittest.TestCase):
    def test_bst(self):
        numbers = [10, 15, 3, 6, 12, 20, 1, 0]
        bst = BST()
        for num in numbers:
            bst.insert(num)

        ordered_nums = bst.traverse_inorder()

        print(ordered_nums)

        for num in numbers:
            successor = bst.find_next_bigger_elem(num)
            if successor is not None:
                print('Successor of %d is %d' % (num, successor))
            else:
                print('Successor of %d is %s' % (num, 'None'))

            predecessor = bst.find_previous_smaller_elem(num)
            if predecessor is not None:
                print('Predecessor of %d is %d' % (num, predecessor))
            else:
                print('Predecessor of %d is %s' % (num, 'None'))

            print('\n')

        num = -1  # Does not exist in the list
        successor = bst.find_next_bigger_elem(num)
        if successor is not None:
            print('Successor of %d is %d' % (num, successor))
        else:
            print('Successor of %d is %s' % (num, 'None'))

        print('\n')

        num = 1
        removed = bst.remove(num)
        if removed is not None:
            print('%d removed from tree: %s' % (num, " ".join(str(x) for x in bst.traverse_inorder())))
        else:
            print('%d was not found in the tree' % num)

    def test_consistent_hashing(self):
        keys = ["abcd", "xyza", "pqrs", "wxyz", "mnop", "defg", "gred", "ojfew", "wejfnv", "dgerfg", "ierhgj",
                "srgergh", "ojrfi", "podjf", "powe"]
        nodes = ["1.2.3.4", "3.4.5.6", "5.6.7.8", "7.8.9.10"]

        consistent_hasher = ConsistentHasher()
        for node in nodes:
            consistent_hasher.add_node(node)

        for key in keys:
            node_id = consistent_hasher.assign_key_to_node(key)
            print('Key %s was assigned to node %s' % (key, node_id))

        node_to_remove = "5.6.7.8"
        consistent_hasher.remove_node(node_to_remove)
        print('\nRemoved node %s with hashed ID %d\n' % (node_to_remove, consistent_hasher.hash(node_to_remove)))

        for key in keys:
            node_id = consistent_hasher.assign_key_to_node(key)
            print('Key %s was assigned to node %s' % (key, node_id))

        node_to_add = "5.6.7.8"
        consistent_hasher.add_node(node_to_add)
        print('\nAdded node %s with hashed ID %d\n' % (node_to_add, consistent_hasher.hash(node_to_add)))

        for key in keys:
            node_id = consistent_hasher.assign_key_to_node(key)
            print('Key %s was assigned to node %s' % (key, node_id))


if __name__ == '__main__':
    unittest.main()
