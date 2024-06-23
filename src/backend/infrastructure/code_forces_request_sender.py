from random import randint
from hashlib import sha512
from time import time
from requests import get


class CodeForcesRequestSender:
    key: str
    secret: str

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def send_request(self, method_name: str, **params: int | str | bool) -> object | None:
        rand = randint(100_000, 1_000_000 - 1)
        hasher = sha512()

        params["time"] = int(time())
        params["apiKey"] = self.key

        params_str = '&'.join(sorted(f"{p[0]}={p[1]}" for p in params.items()))

        hasher.update(f"{rand}/{method_name}?{params_str}#{self.secret}".encode())
        api_sig = str(rand) + hasher.hexdigest()

        resp = get(f"https://codeforces.com/api/{method_name}", params | {"apiSig": api_sig})

        if resp.status_code != 200:
            return None

        return resp.json()["result"]
