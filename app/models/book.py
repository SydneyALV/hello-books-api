from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    def to_dict(self):
        book_dict = {}

        book_dict["id"] = self.id
        book_dict["title"] = self.title
        book_dict["description"] = self.description

        return book_dict