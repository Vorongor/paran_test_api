from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    date_of_birth: str
