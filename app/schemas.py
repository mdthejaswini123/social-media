from pydantic import BaseModel, EmailStr
from datetime import datetime

# define pydantic model for post
# it defines the structure of the data that we expect to receive when creating a post
# it has two fields: title and content, both of which are strings

# if the client request body does not match the structure defined in the Post model, FastAPI will automatically return a 422 Unprocessable Entity error response, indicating that the request body is invalid.


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # this field is optional and has a default value of True

    # to make the published field optional, we can set its default value to None, like this:
    # published: Optional[bool] = None


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
