from src.models import db
import sqlalchemy.dialects.postgresql as postgresql
import uuid


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    quote = db.Column(db.Text(), nullable=False)
    movie_or_series = db.Column(db.Text(), nullable=True)

    user_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="CASCADE"))
    user = db.relationship("User")

    def __repr__(self) -> str:
        return f"Quote - {self.quote}"