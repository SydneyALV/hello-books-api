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

def test_get_all_books_with_title_query_matching_none(client, two_books):
    # Arrange 
    data = {'title': 'Desert Book'}

    # Act
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

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