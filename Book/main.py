from fastapi import FastAPI,Security, status, Response, Depends, Path, HTTPException,Request
from Book.schema import BookSchema
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from Book.model import Book, get_db
from Book.utils import jwt_authentication,logger

app = FastAPI(title='Book Store ',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])


@app.post('/add', status_code=status.HTTP_200_OK)
def add_book(body: BookSchema,request:Request, response: Response, db: Session = Depends(get_db)):
    try:
        print(request.state.user)
        user_data = request.state.user
        if not user_data['is_super_user']:
            raise HTTPException(detail="You are not SuperUser",status_code=status.HTTP_400_BAD_REQUEST)
        if not request.state.user.is_verified:
            raise HTTPException(detail='You are not verified user',status_code=status.HTTP_400_BAD_REQUEST)

        data = body.model_dump()
        data.update({'user_id':request.state.user.id})
        book_data = Book(**data)
        db.add(book_data)
        db.commit()
        db.refresh(book_data)
        return {'message': 'Book added successfully ', 'status': 201}
    except Exception as ex:
        logger.exception(ex)
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
        logger.exception(ex)
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
        logger.exception(ex)
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
        logger.exception(ex)
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
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
