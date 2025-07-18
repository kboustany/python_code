class _DoublyLinkedBase:

    class _Node:
        __slots__ = '_item', '_previous', '_next'

        def __init__(self, item, previous, next):
            self._item = item
            self._previous = previous
            self._next = next

    def __init__(self):
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._previous = self._header
        self._length = 0
    
    def __len__(self):
        return self._length
    
    def is_empty(self):
        return self._length == 0
        
    def _insert(self, item, previous, next):
        new_node = self._Node(item, previous, next)

        previous._next = new_node
        next._previous = new_node
        self._length += 1

        return new_node
    
    def _remove(self, node):
        previous = node._previous
        next = node._next
        previous._next = next
        next._previous = previous
        self._length -= 1
        
        removed = node._item
        node._item = node._previous = node._next = None

        return removed


class PositionalList(_DoublyLinkedBase):

    class Position:
        __slots__ = '_container', '_node'

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node
        
        def __ne__(self, other):
            return not (self == other)
        
        def item(self):
            return self._node._item
        
    def first(self):
        return self._wrap(self._header._next)
    
    def last(self):
        return self._wrap(self._trailer._previous)
    
    def before(self, position):
        return self._wrap(self._unwrap(position)._previous)
    
    def after(self, position):
        return self._wrap(self._unwrap(position)._next)
    
    def __iter__(self):
        current = self.first()

        while current is not None:
            yield current.item()
            current = self.after(current)

    def add_first(self, item):
        return self._insert(item, self._header, self._header._next)
    
    def add_last(self, item):
        return self._insert(item, self._trailer._previous, self._trailer)
    
    def add_before(self, position, item):
        node = self._unwrap(position)

        return self._insert(item, node._previous, node)
    
    def add_after(self, position, item):
        node = self._unwrap(position)

        return self._insert(item, node, node._next)
    
    def remove(self, position):
        return self._remove(self._unwrap(position))
    
    def replace(self, position, item):
        node = self._unwrap(position)

        old_item = node._item
        node._item = item

        return old_item
    
    def _unwrap(self, position):
        if not isinstance(position, self.Position):
            raise TypeError("Object is not a position.")

        if position._container is not self:
            raise ValueError("Position does not belong to list.")

        if position._node._next is None:
            raise ValueError("Position is no longer valid.")
        
        return position._node
    
    def _wrap(self, node):
        if node is self._header or node is self._trailer:
            return None
        
        return self.Position(self, node)
    
    def _insert(self, item, previous, next):
        return self._wrap(super()._insert(item, previous, next))