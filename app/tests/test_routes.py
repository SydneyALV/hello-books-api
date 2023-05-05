from werkzeug.exceptions import HTTPException
from app.routes import validate_book
import pytest 

# Get All Books Tests
def test_get_all_books_returns_an_empty_list(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()
    
    # Assert
    assert response_body == []
    assert response.status_code == 200

def test_get_all_books_returns_list_of_books(client, two_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()
    
    # Assert
    assert response_body == [
        {
        "id": 1,
        "title": "Test",
        "description": "Testing description"
        },
        {
        "id": 2,
        "title": "Test 2",
        "description": "Testing description"
        }
    ]
    assert response.status_code == 200

def test_get_all_books_with_title_query_matching_one(client, two_books):
    # Arrange 
    data = {'title': 'Test'}

    # Act
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
        "id": 1,
        "title": "Test",
        "description": "Testing description"
        }]

def test_get_all_books_with_title_query_matching_none(client, two_books):
    # Arrange 
    data = {'title': 'Desert Book'}

    # Act
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# Get One Book Tests
def test_get_one_book(client, two_books):
    # Act
    response = client.get("/books/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "title": "Test 2",
        "description": "Testing description"
    }

def test_status_code_404_for_book_not_found(client):
    # Act
    response = client.get("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": f"Book ID: 3 was not found."
        }

def test_status_code_400_for_invalid_book_id(client):
    # Act
    response = client.get("/books/T")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "message":f"Book ID: T is invalid. It must be an integer."
        }

# Create Book Tests
def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "New book description"
    })
    response_body = response.get_json()

    # Assert
    assert response_body == "Book 'New Book' has been successfully created."
    assert response.status_code == 201

def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act & Assert
    with pytest.raises(KeyError, match='title'):
        response = client.post("/books", json=test_data)

def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act & Assert
    with pytest.raises(KeyError, match = 'description'):
        response = client.post("/books", json=test_data)

def test_create_one_book_with_extra_keys(client, two_books):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book 'New Book' has been successfully created."

# Update Book Tests
def test_update_book_successfully(client, two_books):
    # Arrange
    test_data = {
        "title": "Updated Book Title",
        "description": "Updated Book Description"
    }
    # Act
    response = client.put("/books/1", json=test_data)
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response_body == "Book 'Updated Book Title' has been successfully updated."

def test_update_book_successfully_with_extra_keys(client, two_books):
    # Arrange
    test_data = {
        "title": "Updated Book Title",
        "description": "Updated Book Description",
        "extra": "Extra information"
    }
    # Act
    response = client.put("/books/1", json=test_data)
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response_body == "Book 'Updated Book Title' has been successfully updated."

def test_update_book_response_404_for_book_not_found(client, two_books):
    # Arrange
    test_data = {
        "title": "Updated Book Title",
        "description": "Updated Book Description",
        "extra": "Extra information"
    }
    # Act
    response = client.put("/books/3", json=test_data)
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book ID: 3 was not found."}

def test_update_book_response_400_for_invalid_id(client, two_books):
    # Arrange
    test_data = {
        "title": "Updated Book Title",
        "description": "Updated Book Description",
        "extra": "Extra information"
    }
    # Act
    response = client.put("/books/T", json=test_data)
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book ID: T is invalid. It must be an integer."}

# Delete Book Tests
def test_delete_book_successfully(client, two_books):
    # Arrange
    # Act
    response = client.delete("/books/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response_body == "Book 'Test' has been successfully deleted."

def test_delete_book_response_404_for_book_not_found(client, two_books):
    # Arrange
    # Act
    response = client.delete("/books/3")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book ID: 3 was not found."}

def test_delete_book_response_400_for_invalid_id(client, two_books):
    # Arrange
    # Act
    response = client.delete("/books/T")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book ID: T is invalid. It must be an integer."}

# Validate Book Tests
def test_validate_book(two_books):
    # Act
    result_book = validate_book(1)

    # Assert
    assert result_book.id == 1
    assert result_book.title == "Test"
    assert result_book.description == "Testing description"

def test_validate_book_missing_record(two_books):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_book("3")
    
def test_validate_book_invalid_id(two_books):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_book("cat")