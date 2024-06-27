from dataclasses import dataclass


@dataclass
class StudentData:
    email: str
    handle: str

    def lower_data(self) -> 'StudentData':
        return StudentData(email=self.email.lower(), handle=self.handle.lower())
