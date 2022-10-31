from src.models import db
import uuid


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    quote = db.Column(db.Text(), nullable=False)
    movie_or_series = db.Column(db.Text(), nullable=True)

    def __repr__(self) -> str:
        return f"Quote - {self.quote}"