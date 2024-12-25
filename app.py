import gradio as gr
from joblib import load

model = load("best_model_rf.joblib")
vectorizer = load("tfidf_vectorizer.joblib")

def classify(text):
    text_vectorized = vectorizer.transform([text])
    mbti_class = model.predict(text_vectorized)[0]
    return mbti_class

demo = gr.Interface(
    fn=classify,
    inputs=["text"],
    outputs=["text"],
)

demo.launch()
