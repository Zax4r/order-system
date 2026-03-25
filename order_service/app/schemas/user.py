from pydantic import BaseModel

class SUserBase(BaseModel):
    username: str
    email: str

class SUserAdd(SUserBase):
    pass

class SUserShow(SUserBase):
    pass
