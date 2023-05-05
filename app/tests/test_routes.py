def test_get_all_books_returns_an_empty_list(client):
    # Arrange
    # Act
    response = client.get("/books")
    response_body = response.get_json()
    
    # Assert
    assert response_body == []
    assert response.status_code == 200

# def test_get_all_books_returns_an_empty_list(client):
    # Arrange
    # Act
    # Assert