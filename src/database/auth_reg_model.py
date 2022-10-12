from src.database import db

class User(db.Model):
    id = db.Column(db.Integer, nullable=False, unique=True)
    user_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text(), nullable=False)


    def __repr__(self) -> str:
        return f'email - {self.email}'