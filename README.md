## This is the Cinni-Proto-Backend##

-current infra is the following combination 
-chromadb
-sqlite
-custom clip models 
-custom openai agents[using react paper implementations]
-google_vision for object segmentation [we will ideally build if we can't find a really good clothing segmentation model in order to mask & segment each item on a text or image query ]

-python=3.10
-conda prefered over venv/virtualenv
-pip install -r requirements.txt 
-export OPENAI_API_KEY="yourkey"
-export GOOGLE_API_KEY="yourkey"
-export FLASK_APP=app.py
-python app.py 

## basic socket + werkzeug in flask server to test out the bottlenecks 
we face in optimising search & recommendation for the fashion industry ##





