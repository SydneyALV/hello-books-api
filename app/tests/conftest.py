import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_books(app):
    book1 = Book(
        title="Test",
        description="Testing description"
    )
    
    book2 = Book(
        title="Test 2",
        description="Testing description"
    )

    db.session.add_all([book1, book2])
    db.session.commit()