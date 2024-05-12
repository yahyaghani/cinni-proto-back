from src.sqlite_db.db_model import db, SessionData
from flask import Flask

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# with app.app_context():
#     db.create_all()

def add_or_update_session(session_id, new_chat, new_embedding, user=False):
    session = SessionData.query.filter_by(session_id=session_id).first()
    # Decide the prefix based on who is speaking
    prefix = "User's Question: " if user else "Cinni AI Answer: "
    # Format the chat with the appropriate prefix
    formatted_chat = f"{prefix}{new_chat}"
    if session:
        # Append formatted chat to the existing string with a newline for separation
        session.historical_chat += f"\n{formatted_chat}"
        if new_embedding is not None:
            session.historical_embeddings.append(new_embedding)  # Only append if not None
    else:
        # If the session does not exist, create a new one
        embeddings = [new_embedding] if new_embedding is not None else []
        session = SessionData(session_id, formatted_chat, embeddings)
        db.session.add(session)
    db.session.commit()

def get_session_data(session_id):
    session = SessionData.query.filter_by(session_id=session_id).first()
    if session:
        return session.historical_chat, session.historical_embeddings
    return None, None

# # Example usage
# if __name__ == '__main__':
#     # Adding/updating sessions
#     add_or_update_session('session1', 'Hello, how can I help you?', [0.5, 0.5, 0.5])
#     add_or_update_session('session1', 'I need assistance with my account.', [0.6, 0.6, 0.6])

#     # Retrieving session data
#     chat, embeddings = get_session_data('session1')
#     print(f"Chat: {chat}")
#     print(f"Embeddings: {embeddings}")
