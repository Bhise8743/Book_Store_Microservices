import pytz
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from User.setting import jwt_algo, secret_key
from datetime import datetime, timedelta


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
        return jwt.encode(data, secret_key, algorithm=jwt_algo)

    @staticmethod
    def data_decoding(token):
        try:
            return jwt.decode(token, secret_key, algorithms=jwt_algo)
        except JWTError as ex:
            raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)

