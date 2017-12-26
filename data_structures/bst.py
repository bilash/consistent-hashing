class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val


class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self.insert_node(val, self.root)

    def insert_node(self, val, root):
        if val <= root.val:
            if root.left:
                self.insert_node(val, root.left)
            else:
                root.left = Node(val)
                root.left.parent = root
        else:
            if root.right:
                self.insert_node(val, root.right)
            else:
                root.right = Node(val)
                root.right.parent = root

    def exists(self, val):
        return self.find_node(self.root, val) is not None

    def find(self, val):
        return self.find_node(self.root, val)

    def find_node(self, root, val):
        if root is None:
            return root

        if val == root.val:
            return root
        elif val < root.val:
            return self.find_node(root.left, val)
        else:
            return self.find_node(root.right, val)

    def traverse_inorder(self):
        inorder_nodes = []
        self.inorder(self.root, inorder_nodes)

        return inorder_nodes

    def inorder(self, root, inorder_nodes):
        if root.left:
            self.inorder(root.left, inorder_nodes)
        inorder_nodes.append(root.val)
        if root.right:
            self.inorder(root.right, inorder_nodes)

    def find_next_bigger_elem(self, val):
        node = self.find(val)

        if node:
            next_bigger_node = self.successor(node)
            if next_bigger_node:
                return next_bigger_node.val
        else:
            next_bigger_node = self.successor2(val)
            if next_bigger_node:
                return next_bigger_node.val

        return None

    def successor(self, node):
        if node.right:
            # curr_node = node.right
            # while curr_node.left:
            #     curr_node = curr_node.left
            # return curr_node
            return self.find_minimum(node.right)
        else:
            if not node.parent:
                return node # Wrap around to itself. "node" is the only need in the tree?

            curr_node = node
            parent = curr_node.parent
            while parent and parent.right is curr_node:
                curr_node = parent
                parent = curr_node.parent

            if parent and parent.left is curr_node:
                return parent

        return self.find_minimum(self.root) # Wrap around, and return the minimum value

    def successor2(self, val):
        # Find successor when the value does not exist
        node = self.root
        prev_node = node

        while node:
            prev_node = node
            if node.val < val:
                node = node.right
            elif node.val > val:
                node = node.left
            else:
                return self.successor(node)

        if val < prev_node.val:
            return prev_node

        return self.successor(prev_node)

    def find_previous_smaller_elem(self, val):
        node = self.find(val)

        if node:
            previous_smaller_node = self.predecessor(node)
            if previous_smaller_node:
                return previous_smaller_node.val
            else:
                return node.val # Wrap around to itself. "node" is the only need in the tree?

        return None

    def predecessor(self, node):
        # The predecessor is the maximum node rooted at the left sub-tree of the provided "node".
        # If there is no left child available, then the predecessor is the parent of the provided node where the node
        # is the right child of the parent.
        if node.left:
            return self.find_maximum(node.left)

        if node.parent and node.parent.right is node:
            return node.parent

        return None

    def find_maximum(self, root):
        # The maximum node is the right-most node of the tree rooted at the provided "root".
        # If no right child is present than the provided "root" itself is the maximum node.
        max_node = root
        while max_node.right:
            max_node = max_node.right

        return max_node

    def find_minimum(self, root):
        min_node = root
        while min_node.left:
            min_node = min_node.left

        return min_node

    def remove(self, val):
        # First find the node containing this val
        node = self.find(val)

        if not node:
            return False # No removal was done.

        # Now, there are 3 cases to consider:
        # 1: node has no children
        if node.left is None and node.right is None:
            # Simply remove the node by setting parent-child field to None
            if node.parent:
                if node.parent.left is node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                # This was the only node in the tree
                self.root = None
        elif node.left is not None and node.right is not None:
            # node has both left and right children. Replace the node's value with it's successor node's value.
            successor = self.successor(node)

            # Remove the successor from it's parent
            succ_parent = successor.parent
            if succ_parent.left is successor:
                succ_parent.left = None
            else:
                succ_parent.right = None

            # Now replace "node" val with successor val
            node.val = successor.val
        else:
            # The node has only one child: either left or right
            child = node.left
            if not child:
                child = node.right

            parent = node.parent
            if parent.left is node:
                parent.left = child
            else:
                parent.right = child

            child.parent = parent

        return True # The removal was successful

