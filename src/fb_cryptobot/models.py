from app import db
from sqlalchemy.dialects.postgresql import JSON

class CryptoCurrency(db.Model):
    __tablename__ = 'cryptocurrencies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique = True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name 
