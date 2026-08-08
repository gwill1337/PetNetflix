from datetime import datetime

from pydantic import BaseModel, ConfigDict

class NewMovie(BaseModel):
    name: str
    title: str
    image: str
    rating: float
    year: str
    description: str

class EditMovie(BaseModel):
    name: str
    title: str
    image: str
    rating: float
    year: str
    description: str

class NewMovieOut(BaseModel):
    name: str
    title: str
    image: str
    rating: float
    year: str

    model_config = ConfigDict(from_attributes=True)

class AddFavorite(BaseModel):
    movie_id: int

class AddFavoriteOut(BaseModel):
    movie_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class LoginUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUserOut(BaseModel):
    username: str
    email: str

class CreateUser(BaseModel):
    username: str
    email: str
    password: str

class CreateUserOut(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    username: str
    user_id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class NewComment(BaseModel):
    movie_id: int
    text: str

class CommentOut(BaseModel):
    id: int
    user_id: int
    user_username: str
    movie_id: int
    comment_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)