from typing import ClassVar

from pydantic import BaseModel

from .config import db


class PyrebaseModel(BaseModel):
    __key__: ClassVar[str] = ""

    def save(self, id: str) -> str:
        data = self.model_dump(by_alias=True)
        res = db.child(self.__key__).child(id).set(data)
        return res

    @classmethod
    def get(cls, id: str) -> "PyrebaseModel":
        if bool(id):
            data = db.child(cls.__key__).child(id).get()
            data = data.val()
            return cls(**data)
        return None
