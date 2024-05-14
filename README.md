# Cinni-Proto-Backend

This is the Cinni-Proto-Backend which uses a combination of technologies tailored for optimizing search and recommendation in the fashion industry.

## Current Infrastructure

- **ChromaDB**
- **SQLite**
- **Custom CLIP models**
- **Custom OpenAI agents** (using React paper implementations)
- **Google Vision for object segmentation**: We will build this if we can't find a satisfactory clothing segmentation model to mask & segment each item on a text or image query.

## Environment Setup

- Python version: `3.10`
- **Conda** is preferred over venv/virtualenv

### Installation

1. Install the required Python packages:
   ```sh
   pip install -r requirements.txt

2. Environment variables:
   ```sh
   export OPENAI_API_KEY="yourkey"
      ```sh
   export GOOGLE_API_KEY="yourkey"
   ```sh
   export FLASK_APP=app.py

3. Test :
   ```sh
   python app.py

