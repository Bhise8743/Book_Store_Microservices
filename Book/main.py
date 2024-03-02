"""
@Author: Omkar Bhise

@Date: 2024-02-27 11:30:00

@Last Modified by: Omkar Bhise

@Last Modified time: 2024-02-29 11:30:00

@Title :  Book Microservices
"""
from fastapi import FastAPI, Security, status, Response, Depends, Path, HTTPException, Request
from Book.schema import BookSchema
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from Book.model import Book, get_db
from Book.utils import jwt_authentication, logger

app = FastAPI(title='Book Store ',
              dependencies=[Security(APIKeyHeader(name='authorization')), Depends(jwt_authentication)])


@app.post('/add', status_code=status.HTTP_201_CREATED, tags=["Book"])
def add_book(body: BookSchema, request: Request, response: Response, db: Session = Depends(get_db)):
    """
       Description: This function is used to add the book in the database
       Parameter: body : BookSchema  => Schema of the Book
                  request : Request of the user
                  response : Response  it response to the user
                  db: Session = Depends on the get_db  i.e. he yield the database
       Return: message and status code in JSON format
   """
    try:
        print(request.state.user)
        user_data = request.state.user
        if not user_data['is_super_user']:
            raise HTTPException(detail="You are not SuperUser", status_code=status.HTTP_400_BAD_REQUEST)
        if not user_data['is_verified']:
            raise HTTPException(detail='You are not verified user', status_code=status.HTTP_400_BAD_REQUEST)

        data = body.model_dump()
        data.update({'user_id': user_data['id']})
        book_data = Book(**data)
        db.add(book_data)
        db.commit()
        db.refresh(book_data)
        return {'message': 'Book added successfully ', 'status': 201}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/get/{book_id}', status_code=status.HTTP_200_OK, tags=["Book"])
def get_book_using_id(request: Request, response: Response, db: Session = Depends(get_db),
                      book_id=Path(..., description="Enter the book id ")):
    """
       Description: This function is used to get the book data using book id
       Parameter: body : LoginSchema  => Schema of the login
                  request : Request of the user
                  response : Response  it response to the user
                  db: Session = Depends on the get_db  i.e. he yield the database
       Return: message and status code in JSON format
   """
    try:
        if not request.state.user['is_verified']:
            raise HTTPException(detail='Not a verified user', status_code=status.HTTP_400_BAD_REQUEST)

        book_data = db.query(Book).filter_by(id=book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail='This book id is not present', status_code=status.HTTP_404_NOT_FOUND)
        return {'message': 'Book Found successfully', 'status': 200, 'data': book_data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/get', status_code=status.HTTP_200_OK, tags=["Book"])
def get_all_books(request: Request, response: Response, db: Session = Depends(get_db)):
    """
       Description: This function is used to get the all books of the store
       Parameter: body : LoginSchema  => Schema of the login
                  response : Response  it response to the user
                  db: Session = Depends on the get_db  i.e. he yield the database
       Return: message and status code in JSON format
   """
    try:
        if not request.state.user['is_verified']:
            raise HTTPException(detail='User is not verified ', status_code=status.HTTP_400_BAD_REQUEST)
        books_data = db.query(Book).all()
        if books_data is None:
            raise HTTPException(detail='User Not Added any book', status_code=status.HTTP_400_BAD_REQUEST)
        print(books_data)
        return {'message': 'Books Found', 'status': 200, 'data': books_data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.put('/update/{book_id}', status_code=status.HTTP_200_OK, tags=["Book"])
def update_book(body: BookSchema, request: Request, response: Response, db: Session = Depends(get_db),
                book_id=Path(..., description="Enter the book id ")):
    """
       Description: This function is used to update book data using book id
       Parameter: body : BookSchema  => Schema of the book
                  request : Request of user
                  response : Response  it response to the user
                  db: Session = Depends on the get_db  i.e. he yield the database
       Return: message and status code in JSON format
   """
    try:
        if not request.state.user['is_verified']:
            raise HTTPException(detail='User is Not verified ', status_code=status.HTTP_400_BAD_REQUEST)
        if not request.state.user['is_super_user']:
            raise HTTPException(detail='You are not super user', status_code=status.HTTP_400_BAD_REQUEST)

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


@app.delete('/del/{book_id}', status_code=status.HTTP_200_OK, tags=["Book"])
def delete_book(request: Request, response: Response, db: Session = Depends(get_db),
                book_id=Path(..., description="Enter the book id")):
    """
       Description: This function is used to delete the book using book id
       Parameter: book_id : Book id
                  response : Response  it response to the user
                  db: Session = Depends on the get_db  i.e. he yield the database
       Return: message and status code in JSON format
   """
    try:
        if not request.state.user['is_verified']:
            raise HTTPException(detail='You are not verified user', status_code=status.HTTP_400_BAD_REQUEST)
        if not request.state.user['is_super_user']:
            raise HTTPException(detail='You are not Super user', status_code=status.HTTP_400_BAD_REQUEST)

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


@app.get('/share_book/{book_id}', status_code=status.HTTP_200_OK)
def share_book(book_id: int, response: Response, db: Session = Depends(get_db)):
    """
       Description: This function is used to share book to the cart
       Parameter: book id  : Book id
                  request : Request of the user
                  response : Response  it response to the user
                  db: Session = Depends on the get_db  i.e. he yield the database
       Return: message and status code in JSON format
   """
    try:
        book_data = db.query(Book).filter_by(id=book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail='Book not found', status_code=status.HTTP_404_NOT_FOUND)
        print("Hi I am in the share book ")
        return {'message': "Book Found successful", 'status': 200, 'book_data': book_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
