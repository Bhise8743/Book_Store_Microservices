from fastapi import FastAPI, status, Response, Depends, Path, HTTPException
from Book.schema import BookSchema
from sqlalchemy.orm import Session
from Book.model import Book, get_db
import requests as rq
app = FastAPI(title='Book Store ')


@app.post('/add', status_code=status.HTTP_200_OK)
def add_book(body: BookSchema, response: Response, db: Session = Depends(get_db)):
    try:
        response=rq.get('http://127.0.0.1:8080/auth_user')
        print(response.json())
        data = body.model_dump()
        book_data = Book(**data)
        db.add(book_data)
        db.commit()
        db.refresh(book_data)
        return {'message': 'Book added successfully ', 'status': 201}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/{book_id}', status_code=status.HTTP_200_OK)
def get_book_using_id(response: Response, db: Session = Depends(get_db),
                      book_id=Path(..., description="Enter the book id ")):
    try:
        book_data = db.query(Book).filter_by(id=book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail='This book id is not present', status_code=status.HTTP_404_NOT_FOUND)
        return {'message': 'Book Found successfully', 'status': 200, 'data': book_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/get_all/{user_id}', status_code=status.HTTP_200_OK, tags=["Book"])
def get_all_books(response: Response, db: Session = Depends(get_db),user_id : int = Path(...,description="Enter the user id ")):
    try:
        books_data = db.query(Book).filter_by(user_id=user_id).all()
        if books_data is None:
            raise HTTPException(detail='User Not Added any book', status_code=status.HTTP_400_BAD_REQUEST)

        return {'message': 'Books Found', 'status': 200, 'data': books_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.put('/update/{book_id}', status_code=status.HTTP_200_OK)
def update_book(body: BookSchema, response: Response, db: Session = Depends(get_db),
                book_id=Path(..., description="Enter the book id ")):
    try:
        book_data = db.query(Book).filter_by(id=book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail="This book is not present", status_code=status.HTTP_404_NOT_FOUND)
        [setattr(book_data, key, value) for key, value in body.model_dump().items()]
        db.commit()
        db.refresh(book_data)
        return {'message': "Book Updated successfully ", 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.delete('/del/{book_id}', status_code=status.HTTP_200_OK)
def delete_book(response: Response, db: Session = Depends(get_db), book_id=Path(..., description="Enter the book id")):
    try:
        book_data = db.query(Book).filter_by(id=book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail='Book not found', status_code=status.HTTP_404_NOT_FOUND)
        db.delete(book_data)
        db.commit()
        return {'message': "Book Deleted Successfully", 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
