# Task 2 — FAQ Chatbot using NLP

## Features
- FAQ dataset of sample customer-support questions and answers
- Text preprocessing/vectorization with scikit-learn TF-IDF
- Cosine similarity to find the closest FAQ
- Web chat interface and suggested questions
- Fallback response when a question does not match

## Run
From this folder:
```bash
pip install -r ../requirements.txt
python app.py
```
Open the local address printed by Flask (usually http://127.0.0.1:5000).

## Customize before submitting
- Replace the sample FAQs with a topic relevant to you (college FAQs, library FAQs, or a product).
- Replace `support@example.com` with a suitable placeholder or your project's contact.
- Test spelling variations and unrelated questions.
- Add screenshots to your report and record a demo.

## How matching works
TF-IDF converts each FAQ question into a numerical vector. Cosine similarity compares the user's question with those vectors. The answer belonging to the closest match is returned if its similarity exceeds a small threshold. This is a retrieval-based FAQ bot, not a generative AI model.
