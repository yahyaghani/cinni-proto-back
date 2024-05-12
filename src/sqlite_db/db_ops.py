from src.sqlite_db.db_model import db, SessionData
from flask import Flask

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# with app.app_context():
#     db.create_all()



def add_or_update_session(session_id, new_chat, keywords, new_embedding, user=False):
    session = SessionData.query.filter_by(session_id=session_id).first()
    prefix = "User: " if user else "Cinni AI: "
    formatted_chat = f"{prefix}{new_chat}"

    if session:
        # Append formatted chat and keywords to the existing session
        session.historical_chat += f"\n{formatted_chat}"
        if keywords:
            session.keywords.extend(keywords)  # Append new keywords to the existing list
    else:
        # If the session does not exist, create a new one
        initial_message = "Cinni AI: Hey, what's the special occasion we are looking to dress for..."
        formatted_chat = f"{initial_message}\n{formatted_chat}"
        embeddings = [new_embedding] if new_embedding is not None else []
        session = SessionData(session_id, formatted_chat, embeddings, keywords)

    # Add new embedding if provided
    if new_embedding is not None:
        session.historical_embeddings.append(new_embedding)

    db.session.commit()

def get_session_data(session_id):
    session = SessionData.query.filter_by(session_id=session_id).first()
    if session:
        return session.historical_chat, session.historical_embeddings,session.keywords
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
