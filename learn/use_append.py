class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        try:
            return self._items.pop()
        except IndexError:
            print("Empty stack")

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"In Stack class, it has -> ({self._items})"

stack = Stack()
stack.push(1)
stack.push(2)
print(stack)