from flask import Flask, request, render_template
from newspaper import Article
from textblob import TextBlob

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            return render_template("index.html", error="Please enter a valid URL.")

        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            summary = article.summary

            blob = TextBlob(article.text)
            polarity = blob.sentiment.polarity

            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            return render_template("index.html", title=article.title, summary=summary, sentiment=sentiment, url=url)

        except Exception as e:
            return render_template("index.html", error=f"Failed to process article: {str(e)}")

    return render_template("index.html")

