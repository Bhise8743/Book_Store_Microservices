import jwt
from fastapi import HTTPException,Depends, status,Request
from Book.setting import setting
import requests as rq
import logging
logging.basicConfig(filename='./book_store_cart.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

class JWT:
    @staticmethod
    def data_decoding(token):
        try:
            return jwt.decode(token, setting.secret_key, algorithms=setting.jwt_algo)
        except Exception as ex:
            raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)


def jwt_authentication(request:Request):
    token = request.headers.get('authorization')
    data = JWT.data_decoding(token)
    user_id = data.get('user_id')
    if user_id is None:
        raise HTTPException(detail="Not valid data ",status_code=status.HTTP_404_NOT_FOUND)

    response = rq.get(f'http://127.0.0.1:8080/auth_user?token={token}')

    if response is None:
        raise HTTPException(detail="User Not return anythings ",status_code=status.HTTP_404_NOT_FOUND)
    request.state.user = response.json()['user_data']