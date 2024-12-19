from pathlib import Path

from pydantic import BaseModel


import json


class TokenConfig(BaseModel):
    token: str

    @staticmethod
    def get_token(file="token.json"):
        data = json.loads(Path(file).read_text())
        return TokenConfig(**data)


token_conf = TokenConfig.get_token()
