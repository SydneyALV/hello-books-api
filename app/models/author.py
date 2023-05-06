from app import db

class Author(db.Model):
    id = db.Colummn(db.Integer, primary_key=True)
    name = db.Column(db.String)