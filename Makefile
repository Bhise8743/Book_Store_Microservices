ifeq ($(OS), Windows_NT)
init:
	@pip install -r requirements.txt
user:
	@uvicorn User.main:app --reload
book:
	@uvicorn Book.main:app --reload
cart:
	@uvicorn Cart.main:app --reload
celery:
	@celery -A task.celery worker -l info --pool=solo -E
test_all:
	@pytest
test_book:
	@pytest Test/test_books_apis.py
test_cart:
	@pytest Test/test_cart_apis.py
test_user:
	@pytest Test/test_user_apis.py

endif