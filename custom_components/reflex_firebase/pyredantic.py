from typing import ClassVar

from pydantic import BaseModel

from .auth_state import AuthState
from .config import db


class PyrebaseModel(BaseModel):
    __key__: ClassVar[str] = ""

    def save(self, auth_state: AuthState) -> str:
        if not auth_state.is_logged_in:
            raise Exception("User is not logged in.")
        data = self.model_dump(by_alias=True)
        res = db.child(self.__key__).child(auth_state.user["localId"]).set(data)
        return res

    @classmethod
    def get(cls, auth_state: AuthState) -> "PyrebaseModel":
        if auth_state.is_logged_in:
            data = db.child(cls.__key__).child(auth_state.user["localId"]).get()
            data = data.val()
            return cls(**data)
        return None
