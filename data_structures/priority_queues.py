class _PriorityQueueBase:

    class _Item:
        __slots__ = '_key', '_value'

        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __lt__(self, other):
            return self._key < other._key
        
    def __len__(self):
        raise NotImplementedError
    
    def min(self):
        raise NotImplementedError

    def add(self, key, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError


class HeapPQ(_PriorityQueueBase):

    def __init__(self, contents=()):
        self._data = [self._Item(key, value) for key, value in contents]

        if len(self._data) > 1:
            self._heapify()

    def __len__(self):
        return len(self._data)

    def min(self):
        if len(self._data) == 0:
            raise Exception("Queue is empty.")
        
        return self._data[0]._key, self._data[0]._value
        
    def add(self, key, value):
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def pop(self):
        if len(self._data) == 0:
            raise Exception("Queue is empty.")
        
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)

        return item._key, item._value

    def _upheap(self, i):
        parent = self._parent(i)

        if i > 0 and self._data[i] < self._data[parent]:
            self._swap(i, parent)
            self._upheap(parent)

    def _downheap(self, i):
        if self._has_left(i):
            left = self._left(i)
            small_child = left

            if self._has_right(i):
                right = self._right(i)

                if self._data[right] < self._data[left]:
                    small_child = right
            
            if self._data[small_child] < self._data[i]:
                self._swap(i, small_child)
                self._downheap(small_child)

    def _heapify(self):
        start = self._parent(len(self) - 1)

        for i in range(start, -1, -1):
            self._downheap(i)

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return (2 * i) + 1

    def _right(self, i):
        return (2 * i) + 2

    def _has_left(self, i):
        return self._left(i) < len(self._data)

    def _has_right(self, i):
        return self._right(i) < len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]


class AdaptablePQ(HeapPQ):

    class Item(HeapPQ._Item):
        __slots__ = '_index'

        def __init__(self, key, value, index):
            super().__init__(key, value)
            self._index = index

    def add(self, key, value):
        item = self.Item(key, value, len(self._data))
        self._data.append(item)
        self._upheap(len(self._data) - 1)

        return item

    def update(self, item, key, value):
        i = item._index

        if not (0 <= i < len(self) and self._data[i] is item):
            raise ValueError("Item does not belong to queue.")
        
        item._key = key
        item._value = value
        self._bubble(i)

    def remove(self, item):
        i = item._index

        if not (0 <= i < len(self) and self._data[i] is item):
            raise ValueError("Item does not belong to queue.")
        
        if i == len(self) - 1:
            self._data.pop()
        else:
            self._swap(i, len(self) - 1)
            self._data.pop()
            self._bubble(i)

        return item._key, item._value

    def _bubble(self, i):
        if i > 0 and self._data[i] < self._data[self._parent(i)]:
            self._upheap(i)
        else:
            self._downheap(i)

    def _swap(self, i, j):
        super()._swap(i, j)
        self._data[i]._index = i
        self._data[j]._index = j