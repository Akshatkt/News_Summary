from flask import Flask, render_template, request
from newspaper import Article
from textblob import TextBlob

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    sentiment = ""
    author = ""
    publish_date = ""
    top_image = ""

    if request.method == "POST":
        url = request.form["url"]
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        summary = article.summary
        author = ", ".join(article.authors)
        publish_date = article.publish_date
        top_image = article.top_image
        sentiment_polarity = TextBlob(article.text).sentiment.polarity
        sentiment = (
            "Positive" if sentiment_polarity > 0 else
            "Negative" if sentiment_polarity < 0 else
            "Neutral"
        )

    return render_template("index.html", summary=summary, sentiment=sentiment,
                           author=author, publish_date=publish_date,
                           top_image=top_image)
