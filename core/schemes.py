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
    user_id: int

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