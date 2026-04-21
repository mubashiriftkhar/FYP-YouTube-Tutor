from abc import ABC, abstractmethod
from Backend.state import State
class BaseClass(ABC):
    @abstractmethod
    def execute(self,state:State) -> State:
        pass