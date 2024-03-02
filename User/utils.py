import pytz
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from setting import setting
from datetime import datetime, timedelta
import logging
logging.basicConfig(filename='./book_store_user.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

def hash_password(raw_password):
    return pbkdf2_sha256.hash(raw_password)


def verify_password(raw_password, hash_password):
    return pbkdf2_sha256.verify(raw_password, hash_password)


class JWT:
    @staticmethod
    def data_encoding(data: dict):
        if 'exp' not in data:
            expire = datetime.now(pytz.utc) + timedelta(minutes=30)
            data.update({'exp': expire})
        return jwt.encode(data, setting.secret_key, algorithm=setting.jwt_algo)

    @staticmethod
    def data_decoding(token):
        try:
            return jwt.decode(token, setting.secret_key, algorithms=setting.jwt_algo)
        except JWTError as ex:
            raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)

