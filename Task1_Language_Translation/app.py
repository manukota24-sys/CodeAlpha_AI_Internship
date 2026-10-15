from flask import Flask, render_template, request
import requests

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Arabic": "ar",
    "Chinese": "zh"
}

@app.route("/", methods=["GET", "POST"])
def index():
    translated = ""
    error = ""
    source_text = ""
    source_lang = "en"
    target_lang = "hi"

    if request.method == "POST":
        source_text = request.form.get("text", "").strip()
        source_lang = request.form.get("source_lang", "en")
        target_lang = request.form.get("target_lang", "hi")

        if not source_text:
            error = "Please enter some text to translate."
        elif source_lang == target_lang:
            translated = source_text
        else:
            try:
                # MyMemory public translation API; verify its current usage limits before deployment.
                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={"q": source_text, "langpair": f"{source_lang}|{target_lang}"},
                    timeout=15
                )
                response.raise_for_status()
                data = response.json()
                translated = data.get("responseData", {}).get("translatedText", "")
                if not translated:
                    error = data.get("responseDetails") or "No translation was returned. Try again."
            except requests.RequestException:
                error = "Could not reach the translation service. Check your internet connection and try again."
            except (ValueError, TypeError):
                error = "The translation service returned an unexpected response."

    return render_template(
        "index.html", languages=LANGUAGES, translated=translated, error=error,
        source_text=source_text, source_lang=source_lang, target_lang=target_lang
    )

if __name__ == "__main__":
    app.run(debug=True)
