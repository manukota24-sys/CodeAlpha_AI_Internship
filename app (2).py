from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

FAQS = [
    {"question": "What are your working hours?", "answer": "Our support hours are Monday to Friday, 9:00 AM to 5:00 PM."},
    {"question": "How can I contact support?", "answer": "You can contact support by emailing support@example.com."},
    {"question": "How do I reset my password?", "answer": "Choose 'Forgot password' on the sign-in page and follow the email instructions."},
    {"question": "How can I create an account?", "answer": "Select 'Sign up', enter the required details, and verify your email address."},
    {"question": "Do you offer refunds?", "answer": "Refund eligibility depends on the purchase terms. Contact support@example.com with your order details."},
    {"question": "Where can I find my order status?", "answer": "Sign in to your account and open the 'Orders' page to view the latest status."},
    {"question": "Can I change my email address?", "answer": "Open account settings, update your email address, and complete any verification steps."},
    {"question": "How do I cancel my order?", "answer": "Open the 'Orders' page and check whether the order still has a cancellation option."},
    {"question": "Is customer support available on weekends?", "answer": "Our regular support hours are Monday to Friday. Email support and we will respond during business hours."},
    {"question": "What payment methods are accepted?", "answer": "Accepted payment methods depend on the checkout options shown for your order."}
]

questions = [item["question"] for item in FAQS]
vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, stop_words="english")
faq_matrix = vectorizer.fit_transform(questions)

def answer_question(user_question):
    user_question = user_question.strip()
    if not user_question:
        return "Please type a question so I can help."
    user_vector = vectorizer.transform([user_question])
    scores = cosine_similarity(user_vector, faq_matrix).flatten()
    best_index = int(scores.argmax())
    # Avoid confidently answering unrelated questions.
    if scores[best_index] < 0.12:
        return "Sorry, I couldn't find a close match in my FAQ list. Please contact support@example.com."
    return FAQS[best_index]["answer"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", ""))[:500]
    return jsonify({"answer": answer_question(question)})

if __name__ == "__main__":
    app.run(debug=True)
