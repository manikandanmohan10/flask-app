from src.models import db
from sqlalchemy.dialects import postgresql
import uuid

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    user_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey("user.id", ondelete='CASCADE'))
    user = db.relationship("User")

    def __repr__(self):
        return f"Task - {self.content}"