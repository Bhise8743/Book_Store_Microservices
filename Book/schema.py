from pydantic import BaseModel


class Book(BaseModel):
    book_name : str
    author : str
    quantity : int
    price : int
    user_id : int
