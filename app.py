## This is a demo app built by Yahya Ghani to prototype ideas & bottlenecks for Cinni AI  ###


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import uuid

import os
from werkzeug.utils import secure_filename
from src.google_vision import detect_labels
# from src.object_segment import localize_objects
import time 

# custom module imports
from src.sqlite_db.db_model import db
from src.sqlite_db.db_ops import add_or_update_session, get_session_data
from src.google_vision import call_vision_chain
from src.open_calls.instruction_calls import basic_shopping_prompt


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'src', 'sqlite_db', 'sessions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for SocketIO


@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        file = request.files['image']
        session_id = request.form['session_id']  # Retrieve sessionID from form data
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join('uploads', filename)
            file.save(save_path)

            # # Proceed with your vision chain processing
            # final_dict_received = call_vision_chain(save_path, session_id)

            # Assuming final_dict_received is a list of image URLs
            return jsonify({"message": "Image saved", "status": "success", "image_urls": final_dict_received})
        else:
            return jsonify({"message": "File not acceptable", "status": "error"})
    else:
        return jsonify({"message": "No file received", "status": "error"})


@app.route('/api/fetch-pins', methods=['POST'])
def fetch_pins():
    data = request.get_json()
    image_url = data.get('image')
    session_id = data.get('session_id')

    if image_url:
        # Process the image URL as needed, here just simulating
        # Mock response URLs for new pins
        new_pins_urls = [
            "https://storage.yandexcloud.net/clothes-and-wildberries/clothes-parsing-dataset/shein/2023/01/11/167340049193f732321fe3276a6cdf15eec222516e_thumbnail_600x.webp",
            "https://storage.yandexcloud.net/clothes-and-wildberries/clothes-parsing-dataset/shein/2020/12/04/1607063823f37b13da36d7899a3d85804fbe0a6190_thumbnail_600x.webp",
            "https://storage.yandexcloud.net/clothes-and-wildberries/clothes-parsing-dataset/shein/2022/09/14/16631405446974d94a00df821f0a7f48a4c1e33b31_thumbnail_600x.webp"
        ]
        return jsonify({"urls": new_pins_urls})
    else:
        return jsonify({"message": "No image URL provided", "status": "error"})



@socketio.on('connect')  # Define a handler for WebSocket connections
def handle_connect():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    emit('session_id', {'session_id': session_id})  # Emit the session ID back to the client
    print('Client connected with session ID:', session_id)

    print('Client connected')

@socketio.on('disconnect')  # Define a handler for WebSocket disconnections
def handle_disconnect():
    print('Client disconnected')

@socketio.on('chat-query')  # Define a handler for chat queries
def handle_chat_query(data):
    session_id = data.get('session_id')
    message = data.get('message')
    print('Received message from session:', session_id, 'Message:', message)
    add_or_update_session(session_id, message, None,user=True)


    ## we need to parse the query and store it in a table utilising the session id for key, aswell as continue with other processes
     
    # # You can emit a response back to the client if required
    ## Finaly store the embeddings and system response
    # add_or_update_session(session_id, system_answer, new_embedding,user=False)

    emit('chat-response', {'message': 'Response to chat query','placeholders':'how can i decide my size,what else is there in a similar style'})  # Emit a response to the client

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
