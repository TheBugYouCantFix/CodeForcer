from abc import ABC, abstractmethod


class IContestsProvider(ABC):
    @abstractmethod
    def get_contest(self, contest_id: int, key: str, secret: str):
        pass
