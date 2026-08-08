
from pydantic import BaseModel, RootModel, Field
from enum import StrEnum

class LiteratureGenres(StrEnum):
    fantasy = "Fantasy"
    science_fiction = "Science Fiction"
    crime = "Crime"
    romance = "Romance"

class BookAddSchema(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)


class BookUpdateSchema(BookAddSchema):
    pass


class BookResponseSchema(BookAddSchema):
    pass

