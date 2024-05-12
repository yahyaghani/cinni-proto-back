## This is a demo app built by Yahya Ghani to prototype ideas & bottlenecks for Cinni AI  ###

import os
import uuid
import json
import random
import requests
import time 

##
from werkzeug.utils import secure_filename
from src.google_vision import detect_labels
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit,join_room
from threading import Thread


from src.sqlite_db.extensions import db, migrate
from src.sqlite_db.db_model import SessionData

from src.google_vision import pin_image_received_chain,call_vision_chain
from src.open_calls.instruction_calls import *
from src.parser_helpers import extract_list_from_string

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'src', 'sqlite_db', 'sessions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set the configuration in Flask

db.init_app(app)
migrate.init_app(app, db)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")


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

    if not image_url or not session_id:
        return jsonify({"message": "Image URL or session ID missing", "status": "error"}), 400

    # Retrieve session data
    historical_chat, historical_embeddings,historical_keyword_list = get_session_data(session_id)
    # if not historical_chat:  # If no session found, initialize it
    #     add_or_update_session(session_id, "Initial session start", None)

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            filename = secure_filename(image_url.split('/')[-1])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Process image and generate response based on historical context
            final_dict, list_of_objects_in_crop,final_pin_list = call_vision_chain(
                file_path,historical_keyword_list, historical_context=historical_chat, historical_embeddings=historical_embeddings
            )
            # print('final_dict',final_dict)
            response = no_context_request_more_context(list_of_objects_in_crop)
            options_placeholders = extract_list_from_string(davinci_results_sentence(response))

            # ### for random pin send testing
            # with open('./data/products.json', 'r') as file:
            #     products = json.load(file)
            # product_ids = random.sample(list(products.keys()), 3)

            product_ids=final_pin_list

            system_default_response = "Check out these pins!"
            default_placeholder = ['how can i decide my size', 'what else is there in a similar style']
            if response:
                system_default_response = response

            if isinstance(options_placeholders, list):
                default_placeholder = options_placeholders
            
            # Emit response to the client
            socketio.emit('chat-response', {
                'message': system_default_response,
                'placeholders': default_placeholder
            }, room=session_id)

            # Update session with new chat and embeddings
            add_or_update_session(session_id, system_default_response,list_of_objects_in_crop, None)

            return jsonify({"productIds": product_ids}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred: " + str(e), "status": "error"}), 500


@socketio.on('connect')  # Define a handler for WebSocket connections
def handle_connect():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    join_room(session_id)  # The client joins a room named after their session ID.
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
    system_default_response="Response to chat query"
    add_or_update_session(session_id, system_default_response, [0.14241412441],user=False)
    if session_id:
        emit('chat-response', {'message': system_default_response,'placeholders':['how can i decide my size', 'what else is there in a similar style']}, room=session_id)  # Emit a response to the client




if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
