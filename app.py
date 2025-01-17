import gradio as gr
from joblib import load
import numpy as np

# Load model and vectorizer
model = load("best_model_rf.joblib")
vectorizer = load("tfidf_vectorizer.joblib")

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
