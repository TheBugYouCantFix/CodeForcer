import sqlite3
from typing import Tuple
from singleton_meta import SingletonMeta


class DBContext(metaclass=SingletonMeta):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def execute_command(self, command: str, parameters=()) -> sqlite3.Cursor:
        print(parameters, type(parameters))
        return self.cursor.execute(command, parameters)
