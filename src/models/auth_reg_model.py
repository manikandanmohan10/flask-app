from src.models import db
import uuid
from sqlalchemy.dialects import postgresql

class User(db.Model):
    # id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return f'email - {self.email}'