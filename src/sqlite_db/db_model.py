from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SessionData(db.Model):
    __tablename__ = 'session_data'

    session_id = db.Column(db.String, primary_key=True)
    historical_chat = db.Column(db.String, nullable=False)
    historical_embeddings = db.Column(db.PickleType, nullable=False)  # Using PickleType to store list of embeddings

    def __init__(self, session_id, historical_chat, historical_embeddings):
        self.session_id = session_id
        self.historical_chat = historical_chat
        self.historical_embeddings = historical_embeddings

    def __repr__(self):
        return f'<SessionData {self.session_id}>'
