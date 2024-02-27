from os import getenv
from dotenv import load_dotenv

load_dotenv()

postgresSQL_password=getenv('postgresSQL_password')
user_database_name=getenv('user_database_name')
redis_url=getenv('redis_url')
email_sender=getenv('email_sender')
email_password=getenv('email_password')
super_key=getenv('super_key')
secret_key=getenv('secret_key')  # import secrets.token_hex(32)
jwt_algo=getenv('jwt_algo')