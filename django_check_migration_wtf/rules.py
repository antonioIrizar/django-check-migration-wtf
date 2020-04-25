import re
from abc import ABC, abstractmethod
from typing import Pattern


class AbstractSQLRule(ABC):
    def __init__(self):
        self.regex: Pattern = re.compile(self.pattern)

    @property
    @abstractmethod
    def pattern(self) -> str:
        """Pattern for regex"""

    def is_match(self, sql_sentence: str) -> bool:
        if self.regex.fullmatch(sql_sentence.lower()) is None:
            return False
        else:
            return True

    @property
    @abstractmethod
    def error_info(self) -> str:
        """Give the error info about rule"""
