import gradio as gr
from joblib import load
import zipfile
import os

# Path to the zip file
MODEL_ZIP_PATH = "best_model_rf.zip"
MODEL_FILE_NAME = "best_model_rf.joblib"

# Extract and load the model
def load_model_from_zip(zip_path, model_file_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract the model file
        zip_ref.extract(model_file_name, path=".")
    # Load the model
    return load(model_file_name)

# Load model and vectorizer
model = load_model_from_zip(MODEL_ZIP_PATH, MODEL_FILE_NAME)
vectorizer = load("tfidf_vectorizer.joblib")

# Define the classify function
def classify(text):
    # Vectorize the input text
    text_vectorized = vectorizer.transform([text])
    
    # Predict the class
    mbti_class = model.predict(text_vectorized)[0]
    
    # Get probabilities for each class
    probabilities = model.predict_proba(text_vectorized)[0]
    class_probabilities = sorted(
        zip(model.classes_, probabilities),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Format probabilities as a string
    prob_text = "\n".join([f"{cls}: {prob:.2%}" for cls, prob in class_probabilities])
    
    return f"Predicted Class: {mbti_class}\n\nClass Probabilities:\n{prob_text}"

# Create the Gradio interface
demo = gr.Interface(
    fn=classify,
    inputs=["text"],
    outputs=["text"],
)

# Launch the app
demo.launch(share=False)
