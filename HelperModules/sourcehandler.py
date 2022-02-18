import io
import linecache
from abc import ABC, abstractmethod


class SourceHandler(ABC):
    @abstractmethod
    def __init__(self, file) -> None:
        self._file = file

        # position of the current char in input
        self._column = 0
        self._line = 1

    def get_next_char(self) -> str:
        self._currentChar = self._file.read(1)

        if self._currentChar != '':
            self._column += 1
        if self._currentChar == '\n':
            self._column = 0
            self._line += 1

        return self._currentChar

    def get_current_char(self) -> str:
        return self._currentChar

    def get_position(self) -> tuple:
        return (self._line, self._column)

    @abstractmethod
    def get_line(self) -> str:
        pass


class FileHandler(SourceHandler):
    def __init__(self, filename: str):
        self._filename = filename
        try:
            super().__init__(open(self._filename, 'r'))
        except IOError:
            raise IOError

    def __del__(self):
        try:
            self._file.close()
        except AttributeError:
            #means that super object wasn't fully initialized and _file atribute is not defined.
            pass
        except IOError:
            raise IOError

    def get_line(self) -> str:
        return linecache.getline(self._filename, self._line)


class DirectInputHandler(SourceHandler):
    def __init__(self, directInput: str):
        super().__init__(io.StringIO(directInput))

    def get_line(self) -> str:
        return self._file.getvalue().splitlines()[self._line - 1]