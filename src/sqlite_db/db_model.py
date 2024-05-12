# db_model.py
from src.sqlite_db.extensions import db

class SessionData(db.Model):
    __tablename__ = 'session_data'

    session_id = db.Column(db.String, primary_key=True)
    historical_chat = db.Column(db.String, nullable=False)
    historical_embeddings = db.Column(db.PickleType, nullable=False)
    keywords = db.Column(db.PickleType, nullable=True)

    def __init__(self, session_id, historical_chat, historical_embeddings, keywords=None):
        self.session_id = session_id
        self.historical_chat = historical_chat
        self.historical_embeddings = historical_embeddings
        self.keywords = keywords if keywords else []

    def __repr__(self):
        return f'<SessionData {self.session_id}>'
