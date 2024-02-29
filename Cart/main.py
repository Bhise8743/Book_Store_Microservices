from fastapi import FastAPI, status, Request, Response, Depends, Security, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from Cart.model import get_db, Cart, CartItems
from Cart.schema import CartItemsSchema
from Cart.utils import jwt_authentication
import requests as rq

app = FastAPI(title='Book Store',
              dependencies=[Security(APIKeyHeader(name='authorization')), Depends(jwt_authentication)])


@app.post('/add', status_code=status.HTTP_201_CREATED)
def add_cart(body: CartItemsSchema, request: Request, db: Session = Depends(get_db)):
    try:
        user_data = request.state.user
        # print(request.state.user)

        cart_data = db.query(Cart).filter_by(user_id=user_data['id']).one_or_none()
        if cart_data is None:
            cart_data = Cart(user_id= user_data['id'])
            db.add(cart_data)
            db.commit()
            db.refresh(cart_data)
        response = rq.get(f'http://127.0.0.1:8008/share_book/{body.book_id}',headers={'authorization':request.headers.get('authorization')})
        print(response.json())
        book_data = response.json()['book_data']
        print("\n\n",book_data)
        if book_data is None:
            raise HTTPException(detail='Book Not found', status_code=status.HTTP_404_NOT_FOUND)
        books_price = book_data.price * body.quantity
        cart_items_data = db.query(CartItems).filter_by(book_id=body.book_id, cart_id=cart_data.id).one_or_none()
        if cart_items_data:
            cart_data.total_price -= cart_items_data.price
            cart_data.total_quantity -= cart_items_data.quantity
        else:
            cart_items_data = CartItems({'book_id': body.book_id, 'cart_id': cart_data.id, 'quantity': 0, 'price': 0})
            db.commit()
        cart_items_data.quantity = body.quantity
        cart_items_data.price = books_price
        cart_data.total_price += books_price
        cart_data.total_quantity += body.quantity
        db.commit()
        db.refresh(cart_data)
        db.refresh(cart_items_data)
        return {'message': "Book added in cart successfully", 'status': 200}

    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@app.get('/get', status_code=status.HTTP_200_OK)
def get_cart_data(response: Response, request: Request, db: Session = Depends(get_db)):
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            raise HTTPException(detail="The cart is empty",status_code=status.HTTP_404_NOT_FOUND)
        cart_items_data = db.query(CartItems).filter_by(cart_id=cart_data.id).one_or_none()
        if cart_items_data is None:
            raise HTTPException(detail='User not added any book in the cart items ',status_code=status.HTTP_404_NOT_FOUND)
        return {'message':'Cart and Cart Items are Found ','status':200,'Cart_data':cart_data,'Cart_Items_data':cart_items_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
