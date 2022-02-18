from abc import ABC, abstractmethod
import pickle


class INode(ABC):
    def __eq__(self, other) -> bool:
        return isinstance(
            other,
            self.__class__) and pickle.dumps(self) == pickle.dumps(other)

    @abstractmethod
    def accept(self, visitor) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass