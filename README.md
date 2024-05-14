# Cinni-Proto-Backend

This is the Cinni-Proto-Backend which uses a combination of technologies tailored for optimizing search and recommendation in the fashion industry.

## Current Infrastructure
![Cinni Flow](/cinni-flow.jpg)

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
   export GOOGLE_API_KEY="yourkey"
   export FLASK_APP=app.py

3. Test :
   ```sh
   python app.py


## References

### Articles and Papers

- **Exploring CLIP: Bridging Text and Images**  
  [Read more on arXiv](https://arxiv.org/abs/2202.02757)  
  A comprehensive study on how CLIP models bridge the gap between text descriptions and image content, enabling new ways to handle multimodal tasks.

- **Advancements in Neural Networks for Fashion**  
  [Read more on arXiv](https://arxiv.org/abs/2404.14396)  
  Discusses recent neural network advancements specifically applied to the fashion industry, enhancing capabilities in image recognition and recommendation systems.

### Tools and Libraries

- **OpenAI CLIP**  
  [Visit OpenAI](https://openai.com/index/clip/)  
  OpenAI's CLIP is a neural network trained on a variety of (image, text) pairs. It learns visual concepts from natural language supervision.

- **FashionML**  
  [Visit GitHub repository](https://github.com/federicoB/fashionML)  
  A GitHub repository showcasing machine learning techniques applied to fashion datasets. Useful for developers looking into fashion-related ML projects.

