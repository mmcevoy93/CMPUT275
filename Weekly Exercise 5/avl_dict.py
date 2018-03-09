import bstviz


class AVLNode:
    """
    Same as BSTNode from before, except we now maintain a height.

    In our implementation of AVL trees, we use "empty" nodes
    (nodes without keys)
    instead of None child pointers. It simplifies a few steps.
    """

    def __init__(self):
        """
        Only for initializing an empty node, which will have height -1.
        """

        self.key = None
        self.item = None
        self.left = None
        self.right = None
        self.height = -1

    def _recalc_height(self):
        """
        Recalculates the height of this node, assuming the heights
        of the children are correct.
        """

        self.height = 1 + max(self.left.height, self.right.height)

    def _rotate_left(self):
        """
        Performs a left rotation.
        Assumes the right child of this node is not empty.
        Recalculates heights of the two nodes that are rotated.

        Returns the node that was rotated above this one.
        """

        right = self.right
        right.left, self.right = self, right.left

        self._recalc_height()  # important that this is first
        right._recalc_height()

        return right

    def _rotate_right(self):
        """
        Performs a right rotation.
        Assumes the left child of this node is not empty.
        Recalculates heights of the two nodes that are rotated.

        Returns the node that was rotated above this one.
        """

        left = self.left
        left.right, self.left = self, left.right

        self._recalc_height()  # important that this is first
        left._recalc_height()

        return left

    def _check_and_fix_imbalance(self):
        """
        Checks the height (after recalculating).
        If imbalanced, will perform rotations to rebalance this node.
        Returns the root of the new subtree (may no longer be this node).

        Assumes the heights of the children are correct and that they differ
        by at most 2 (which will be the case if used properly with the AVL
        rebalancing procedures).
        """

        self._recalc_height()
        balance = self.left.height - self.right.height

        if abs(balance) <= 1:
            # no imbalance, so no rotation
            return self
        elif balance == 2:
            # left subtree is higher
            left = self.left
            if left.left.height < left.right.height:
                self.left = left._rotate_left()
            return self._rotate_right()
        else:  # balance == -2, right subtree is higher
            right = self.right
            if right.right.height < right.left.height:
                self.right = right._rotate_right()
            return self._rotate_left()


class AVLDict:
    """
    A dictionary whose keys are comparable items where the comparison forms
    a total ordering. The underlying data structure is an AVL tree whose nodes
    are ordered by the keys they hold. This guarantees insertion, finding, and
    removal take O(log n) time.

    Note, in this implementation we represent a empty child as a node that has
    None for a key. This differs with the TreeDict implementation, which just
    used None pointers.
    """
    def __init__(self):
        """
        Initialize an empty dictionary.
        """

        self.root = AVLNode()
        self.len = 0

    def _find_and_fix(self, key):
        """
        Find the node with the given key, and call _check_and_fix_imbalance()
        on the nodes on this search path in reverse order of depth.
        """

        def recursive_fix(node):
            if node.key is None:
                raise KeyError(key)
            elif key < node.key:
                node.left = recursive_fix(node.left)
            elif key > node.key:
                node.right = recursive_fix(node.right)

            return node._check_and_fix_imbalance()

        self.root = recursive_fix(self.root)

    def _find(self, key):
        """
        Find the node with the given key.

        Returns node, parent where parent is the parent node on the search.

        If the key is not found, it returns the empty node that would have
        received the key.
        """

        node, parent = self.root, None

        while node.key is not None and node.key != key:
            if key < node.key:
                node, parent = node.left, node
            else:
                node, parent = node.right, node

        return node, parent

    def get(self, key):
        """
        Gets the item stored at the key.
        Returns None if the key is not found.
        """
        node, _ = self._find(key)
        if node.key is None:
            return None
        else:
            return node.item

    def popitem(self, key):
        """
        Removes the entry with the given key.
        Raises a key error if not found.
        """

        # first find the key
        node, parent = self._find(key)

        if node.key is None:
            raise KeyError(key)

        self.len -= 1

        # if no left child
        if node.left.key is None:
            if parent is None:
                self.root = node.right
            elif key < parent.key:
                parent.left = node.right
            else:
                parent.right = node.right
            if parent is not None:
                self._find_and_fix(parent.key)
        else:
            # find the maximum key in the subtree under node.left
            max_node, max_parent = node.left, node
            while max_node.right.key is not None:
                max_node, max_parent = max_node.right, max_node

            # move its key/item to node
            node.key, node.item = max_node.key, max_node.item

            # now remove this node
            if max_node == max_parent.left:
                max_parent.left = max_node.left
            else:
                max_parent.right = max_node.left
            self._find_and_fix(max_parent.key)

    def items(self):
        """
        Get a list of the (key, item) pairs, sorted by the key value.
        """

        out = []

        def rec_build(node):
            if node.key is None:
                return
            rec_build(node.left)
            out.append((node.key, node.item))
            rec_build(node.right)

        rec_build(self.root)
        return out

    def update(self, key, item):
        """
        Updates the dictionary to store the item at the given key.
        If the key was not already present, it is added.
        """

        node, parent = self._find(key)

        if node.key is not None:
            node.item = item
            self.num(key)
            return

        self.len += 1
        node.key = key
        node.item = item
        node.left = AVLNode()
        node.right = AVLNode()
        node.height = 0

        # now fix the AVL property on the nodes between this new node and root
        self._find_and_fix(key)

    def ith_key(self, index: int):
        """
        Returns the key that would be at the given index in the sorted list of
        all keys of the tree. Raises an IndexError if the index is out of
        range (i.e. < 0 or >= len(self)).

        Running time: O(log n) where the tree has n items.
        """
        # TODO
        pass

    def num(self, key):
        """
        TODO Fix this to work
        """
        # TODO
        index = len(self.items())
        node, parent = self._find(key)

        if node.key is not None:
            node.num = index
            return

    def __len__(self):
        return self.len

    def __setitem__(self, key, item):
        self.update(key, item)

    def __getitem__(self, key):
        node, _ = self._find(key)
        if node.key is None:
            raise KeyError(key)
        else:
            return node.item

    def __delitem__(self, key):
        self.popitem(key)

    def __str__(self):
        return str(self.items())


if __name__ == "__main__":
    tree = AVLDict()

    # Insert nodes from 0 to 14.
    # Notice how the resulting tree is balanced! If this were a standard
    # binary search tree, it look like a long path.
    for i in range(15):
        tree[i] = i

    bstviz.bstviz(tree, padding=0.7).render(view=True)

    while tree:
        key = int(input("Enter a key to delete: "))
        del tree[key]
        bstviz.bstviz(tree, padding=0.7).render(view=True)
