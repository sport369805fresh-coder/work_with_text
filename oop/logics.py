from abc import ABC, abstractmethod
import re
class BaseFormatter(ABC):
    def __init__(self, name: str):
        self.name = name
        self._symbols_count = 0
    @property
    def symbols_count(self) -> int:
        return self._symbols_count
    @symbols_count.setter
    def symbols_count(self, value: int):
        self._symbols_count = value
    @abstractmethod
    def format_text(self, text: str, param: str = "") -> str:
        pass
    @staticmethod
    def count_words(text: str) -> int:
        return len(text.split())
    def __str__(self):
        return f"Режим: {self.name}"
    def __repr__(self):
        return f"BaseFormatter(name='{self.name}', symbols={self._symbols_count})"
    def __eq__(self, other):
        if not isinstance(other, BaseFormatter):
            return False
        return self.name == other.name
    def __lt__(self, other):
        return self.symbols_count < other.symbols_count
class SnakeCaseFormatter(BaseFormatter):
    def format_text(self, text: str, param: str = "") -> str:
        self.symbols_count += len(text)
        return "_".join(text.lower().split())
class CleanSpaceFormatter(BaseFormatter):
    def format_text(self, text: str, param: str = "") -> str:
        self.symbols_count += len(text)
        return " ".join(text.split())
class SwapCaseFormatter(BaseFormatter):
    def format_text(self, text: str, param: str = "") -> str:
        self.symbols_count += len(text)
        return text.swapcase()
class CipherFormatter(BaseFormatter):
    def format_text(self, text: str, param: str = "") -> str:
        self.symbols_count += len(text)
        if not param.isdigit():
            return text
        shift = int(param)
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        res = []
        for ch in text:
            is_upper = ch.isupper()
            ch_lower = ch.lower()
            if ch_lower in alphabet:
                idx = alphabet.index(ch_lower)
                new_idx = (idx + shift) % len(alphabet)
                new_ch = alphabet[new_idx]
                res.append(new_ch.upper() if is_upper else new_ch)
            else:
                res.append(ch)
        return "".join(res)
class CensorFormatter(BaseFormatter):
    def format_text(self, text: str, param: str = "") -> str:
        self.symbols_count += len(text)
        if not param:
            return text
        letters = [l.strip() for l in param.split(",") if l.strip()]
        for letter in letters:
            pattern = re.escape(letter)
            text = re.sub(pattern, "*", text, flags=re.IGNORECASE)
        return text
