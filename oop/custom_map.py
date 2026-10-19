from logics import BaseFormatter
class KeyValueItem:
    def __init__(self, key: str, value: BaseFormatter):
        self._key = key
        self._value = value
    @property
    def key(self) -> str:
        return self._key
    @key.setter
    def key(self, new_key: str):
        self._key = new_key
    @property
    def value(self) -> BaseFormatter:
        return self._value
    @value.setter
    def value(self, new_value: BaseFormatter):
        self._value = new_value
class MyCustomMap:
    def __init__(self):
        self._items = []
    def put(self, key: str, value: BaseFormatter):
        for item in self._items:
            if item.key == key:
                item.value = value
                return
        self._items.append(KeyValueItem(key, value))
    def get(self, key: str) -> BaseFormatter:
        for item in self._items:
            if item.key == key:
                return item.value
        return None
