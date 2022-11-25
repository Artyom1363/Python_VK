from collections import defaultdict


class Node:
    def __init__(self, value, pref=None, nref=None):
        self.value = value
        self.nref = nref
        self.pref = pref


class CustomList:
    def __init__(self) -> None:
        self.list_start = None
        self.size = 0
        self.list_end = None

    def push_front(self, value) -> Node:
        node = Node(value, None, self.list_start)

        if self.list_start is not None:
            self.list_start.pref = node
        else:
            self.list_end = node

        self.list_start = node
        self.size += 1
        return self.list_start

    def move_up(self, node: Node) -> None:
        if node == self.list_start:
            return

        if node.nref is not None:
            node.nref.pref = node.pref
        else:
            if node.pref is not None:
                self.list_end = node.pref

        if node.pref is not None:
            node.pref.nref = node.nref

        node.pref = None
        node.nref = self.list_start
        self.list_start.pref = node
        self.list_start = node

    def pop_back(self) -> Node:
        if self.list_end is None:
            raise Exception("Try to pop from free list")

        deleting = self.list_end

        if self.size == 1:
            self.list_start = None
            self.list_end = None
        else:
            self.list_end.pref.nref = None
            self.list_end = self.list_end.pref

        self.size -= 1
        return deleting


class LRUCache:
    def __init__(self, max_size=1):
        if max_size < 1:
            raise Exception("Too small max_size in LRU_cache")
        self.max_size = max_size
        self.size = 0
        self.list_storage = CustomList()
        self.dict_storage = defaultdict(None)

    def get(self, key):
        return self[key]

    def set(self, key, value):
        self[key] = value

    def __setitem__(self, key, value):
        if key in self.dict_storage:
            node = self.dict_storage[key]
            node.value = (key, value)
            self.list_storage.move_up(node)
            return

        node = self.list_storage.push_front((key, value))
        self.dict_storage[key] = node

        if self.size == self.max_size:
            node = self.list_storage.pop_back()
            del self.dict_storage[node.value[0]]
        else:
            self.size += 1

    def __getitem__(self, key):
        if key not in self.dict_storage:
            return None

        self.list_storage.move_up(self.dict_storage[key])
        return self.dict_storage[key].value[1]
