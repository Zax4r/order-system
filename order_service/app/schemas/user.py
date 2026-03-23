from pydantic import BaseModel

class SUserBase(BaseModel):
    username: str
    email: str

