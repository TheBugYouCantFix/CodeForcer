from abc import ABC, abstractmethod

from domain.contest import Contest


class IContestsProvider(ABC):
    @abstractmethod
    def get_contest_results(self, contest_id: int, api_key: str, api_secret: str):
        pass

    @abstractmethod
    def get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
        pass
