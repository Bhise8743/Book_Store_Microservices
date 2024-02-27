from os import getenv
from dotenv import load_dotenv

load_dotenv()

postgresSQL_password=getenv('postgresSQL_password')
book_database_name=getenv('book_database_name')