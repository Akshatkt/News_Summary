from flask import Flask, request, render_template, flash, redirect, url_for
import nltk
from textblob import TextBlob
from newspaper import Article
from datetime import datetime
from urllib.parse import urlparse
import validators
import requests

nltk.download('punkt')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not validators.url(url):
            flash('Please enter a valid URL.')
            return redirect(url_for('index'))

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            flash('Failed to download the content of the URL.')
            return redirect(url_for('index'))

        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title = article.title
        authors = ', '.join(article.authors) or get_website_name(url)
        publish_date = article.publish_date.strftime('%B %d, %Y') if article.publish_date else "N/A"
        article_text = article.text
        sentences = article_text.split('.')
        summary = '.'.join(sentences[:5])  # First 5 sentences
        top_image = article.top_image

        analysis = TextBlob(article.text)
        polarity = analysis.sentiment.polarity

        sentiment = 'neutral 😐'
        if polarity > 0:
            sentiment = 'happy 😊'
        elif polarity < 0:
            sentiment = 'sad 😟'

        return render_template('index.html', title=title, authors=authors,
                               publish_date=publish_date, summary=summary,
                               top_image=top_image, sentiment=sentiment)

    return render_template('index.html')
