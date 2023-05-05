from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.book import Book

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])

def handle_books():
    request_body = request.get_json()
    
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"]
        )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(f"Book '{new_book.title}' has been successfully created."), 201


@books_bp.route("", methods=["GET"])

def get_all_books():    
    title_query = request.args.get("title")   
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    
    books_response = []
    for book in books:
        books_response.append(book.to_dict())

    return jsonify(books_response)


@books_bp.route("/<book_id>", methods=["GET"])

def read_one_book(book_id): 
    book = validate_book(book_id)    
    return book.to_dict()


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"Book ID: {book_id} is invalid. It must be an integer."}, 400))
    
    book = Book.query.get(book_id)    
    if not book:
        abort(make_response({"message":f"Book ID: {book_id} was not found."}, 404))

    return book

@books_bp.route("/<book_id>", methods=["PUT"])
    
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()    
    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(f"Book '{book.title}' has been successfully updated.", 200)

@books_bp.route("/<book_id>", methods=["DELETE"])

def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book '{book.title}' has been successfully deleted.", 200)