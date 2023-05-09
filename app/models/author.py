from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String)
    books = db.relationship("Book", back_populates="author")

    def to_dict(self):
        author_dict = {}

        author_dict["id"] = self.id
        author_dict["name"] = self.name

        return author_dict

    @classmethod
    def from_dict(cls, author_data):
        
        new_author = Author(
            name=author_data["name"],
        )

        return new_author