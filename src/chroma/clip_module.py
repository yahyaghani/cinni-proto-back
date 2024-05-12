import os
import clip
import torch
from PIL import Image
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize



def load_clip_model(model_name='ViT-B/32', device=None):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load(model_name, device=device)
    return model, preprocess, device

def preprocess_image(image_path, preprocess):
    image = Image.open(image_path)
    return preprocess(image).unsqueeze(0)

def tokenize_descriptions(descriptions, device):
    return clip.tokenize(descriptions).to(device)

def predict_similarity(model, image_tensor, text_tokens):
    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        text_features = model.encode_text(text_tokens)

        # Calculate the cosine similarity and convert to probabilities
        logits_per_image, logits_per_text = model(image_tensor, text_tokens)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
    return probs


def predict_two_images(model, image_tensor1, image_tensor2):
    with torch.no_grad():
        # Encode images
        image_features1 = model.encode_image(image_tensor1)
        image_features2 = model.encode_image(image_tensor2)

        # Normalize features to compute cosine similarities
        image_features1 = image_features1 / image_features1.norm(dim=-1, keepdim=True)
        image_features2 = image_features2 / image_features2.norm(dim=-1, keepdim=True)

        # Compute cosine similarity as dot product of normalized vectors
        similarity = (image_features1 * image_features2).sum(dim=-1)
        return similarity.cpu().numpy()


# Example Usage in Flask Route
def analyze_image_with_text(image_path, descriptions):
    model, preprocess, device = load_clip_model()
    image_tensor = preprocess_image(image_path, preprocess).to(device)
    text_tokens = tokenize_descriptions(descriptions, device)
    
    probabilities = predict_similarity(model, image_tensor, text_tokens)
    return probabilities

def analyze_image_with_images(image_path, image_path2):
    model, preprocess, device = load_clip_model()
    image_tensor = preprocess_image(image_path, preprocess).to(device)
    # text_tokens = tokenize_descriptions(descriptions, device)
    image_tensor2 = preprocess_image(image_path2, preprocess).to(device)

    probabilities = predict_two_images(model, image_tensor, image_tensor2)
    return probabilities

def get_image_tensor(image_path):
    image_tensor = preprocess_image(image_path, preprocess).to(device)
    return image_tensor

def predict_three_images( image_tensor1, image_tensor2, image_tensor3):
    with torch.no_grad():
        # Encode images
        image_tensor1=get_image_tensor(image_tensor1)
        image_tensor2=get_image_tensor(image_tensor2)
        image_tensor3=get_image_tensor(image_tensor3)

        image_features1 = model.encode_image(image_tensor1)
        image_features2 = model.encode_image(image_tensor2)
        image_features3 = model.encode_image(image_tensor3)

        # Normalize features to compute cosine similarities
        image_features1 = image_features1 / image_features1.norm(dim=-1, keepdim=True)
        image_features2 = image_features2 / image_features2.norm(dim=-1, keepdim=True)
        image_features3 = image_features3 / image_features3.norm(dim=-1, keepdim=True)

        # Compute cosine similarity as dot product of normalized vectors for each pair
        similarity12 = (image_features1 * image_features2).sum(dim=-1)
        similarity13 = (image_features1 * image_features3).sum(dim=-1)
        similarity23 = (image_features2 * image_features3).sum(dim=-1)

        return {
            "similarity12": similarity12.cpu().numpy(), 
            "similarity13": similarity13.cpu().numpy(), 
            "similarity23": similarity23.cpu().numpy()
        }

model, preprocess, device = load_clip_model()

# Additional utility functions or further processing can be added here
