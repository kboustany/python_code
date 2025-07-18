from collections import deque


class _TreeBase:

    class Position:

        def __eq__(self, other):
            raise NotImplementedError
        
        def __ne__(self, other):
            return not (self == other)

        def item(self):
            raise NotImplementedError
        
    def root(self):
        raise NotImplementedError
    
    def parent(self, position):
        raise NotImplementedError
    
    def num_children(self, position):
        raise NotImplementedError
    
    def children(self, position):
        raise NotImplementedError
    
    def __len__(self):
        raise NotImplementedError

    def is_root(self, position):
        return self.root() == position
    
    def is_leaf(self, position):
        return self.num_children(position) == 0
    
    def is_empty(self):
        return len(self) == 0
    
    def depth(self, position):
        if self.is_root(position):
            return 0
        
        return 1 + self.depth(self.parent(position))

    def height(self, position=None):
        if position is None:
            position = self.root()
        
        return self._height(position)

    def _height(self, position):
        if self.is_leaf(position):
            return 0
        
        return 1 + max(self._height(child) for child in self.children(position))

    def preorder(self):
        if not self.is_empty():
            for position in self._subtree_preorder(self.root()):
                yield position

    def postorder(self):
        if not self.is_empty():
            for position in self._subtree_postorder(self.root()):
                yield position

    def _subtree_preorder(self, position):
        yield position
        for child in self.children(position):
            for other in self._subtree_preorder(child):
                yield other

    def _subtree_postorder(self, position):
        for child in self.children(position):
            for other in self._subtree_postorder(child):
                yield other
        yield position

    def breadthfirst(self):
        if not self.is_empty():
            fringe = deque()
            fringe.append(self.root())

            while len(fringe) > 0:
                position = fringe.popleft()
                yield position
                for child in self.children(position):
                    fringe.append(child)


class _BinaryTreeBase(_TreeBase):

    def left(self, position):
        raise NotImplementedError
    
    def right(self, position):
        raise NotImplementedError
    
    def children(self, position):
        if self.left(position) is not None:
            yield self.left(position)
        if self.right(position) is not None:
            yield self.right(position)

    def sibling(self, position):
        parent = self.parent(position)

        if parent is None:
            return None
        
        if position == self.left(parent):
            return self.right(parent)
        
        return self.left(parent)

    def inorder(self):
        if not self.is_empty():
            for position in self._subtree_inorder(self.root()):
                yield position
    
    def _subtree_inorder(self, position):
        if self.left(position) is not None:
            for other in self._subtree_inorder(self.left(position)):
                yield other
        yield position
        if self.right(position) is not None:
            for other in self._subtree_inorder(self.right(position)):
                yield other


class LinkedBinaryTree(_BinaryTreeBase):

    class _Node:
        __slots__ = '_item', '_parent', '_left', '_right'

        def __init__(self, item, parent=None, left=None, right=None):
            self._item = item
            self._parent = parent
            self._left = left
            self._right = right

    class Position(_BinaryTreeBase.Position):
        __slots__ = '_container', '_node'

        def __init__(self, container, node):
            self._container = container
            self._node = node
        
        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node
        
        def item(self):
            return self._node._item
    
    def __init__(self):
        self._root = None
        self._length = 0

    def __len__(self):
        return self._length
    
    def root(self):
        return self._wrap(self._root)
    
    def parent(self, position):
        return self._wrap(self._unwrap(position)._parent)
    
    def left(self, position):
        return self._wrap(self._unwrap(position)._left)
    
    def right(self, position):
        return self._wrap(self._unwrap(position)._right)
    
    def num_children(self, position):
        node = self._unwrap(position)
        count = 0

        if node._left is not None:
            count += 1

        if node._right is not None:
            count += 1
        
        return count
        
    def add_root(self, item):
        if self._root is not None:
            raise ValueError("Root exists.")
        
        self._length = 1
        self._root = self._Node(item)

        return self._wrap(self._root)
    
    def add_left(self, position, item):
        node = self._unwrap(position)

        if node._left is not None:
            raise ValueError("Left child exists.")
        
        self._length += 1
        node._left = self._Node(item, node)

        return self._wrap(node._left)
    
    def add_right(self, position, item):
        node = self._unwrap(position)

        if node._right is not None:
            raise ValueError("Right child exists.")
        
        self._length += 1
        node._right = self._Node(item, node)

        return self._wrap(node._right)
    
    def replace(self, position, item):
        node = self._unwrap(position)

        old_item = node._item
        node._item = item

        return old_item
    
    def remove(self, position):
        node = self._unwrap(position)

        if self.num_children(position) == 2:
            raise ValueError("Position has two children.")
        
        child = node._left if node._left else node._right

        if child is not None:
            child._parent = node._parent

        if node is self._root:
            self._root = child
        else:
            parent = node._parent

            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        
        self._length -= 1
        node._parent = node

        return node._item
    
    def attach(self, position, tree1, tree2):
        node = self._unwrap(position)

        if not self.is_leaf(position):
            raise ValueError("Position must be leaf.")

        if not type(self) is type(tree1) is type(tree2):
            raise TypeError("Tree types must match.")
        
        self._length += len(tree1) + len(tree2)

        if not tree1.is_empty():
            tree1._root._parent = node
            node._left = tree1._root
            tree1._root = None
            tree1._size = 0

        if not tree2.is_empty():
            tree2._root._parent = node
            node._right = tree2._root
            tree2._root = None
            tree2._size = 0

    def _unwrap(self, position):
        if not isinstance(position, self.Position):
            raise TypeError("Object is not a position.")

        if position._container is not self:
            raise ValueError("Position does not belong to tree.")
        
        if position._node._parent is position._node:
            raise ValueError("Position is no longer valid.")
        
        return position._node
    
    def _wrap(self, node):
        return self.Position(self, node) if node is not None else None