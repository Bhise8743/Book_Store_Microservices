from pydantic import BaseModel


class BookSchema(BaseModel):
    book_name: str
    author: str
    price: int
    quantity: int
    user_id : int
