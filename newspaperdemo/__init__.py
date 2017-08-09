from flask import Flask, request, render_template, redirect, url_for, Response
from newspaper import Article
from xml.etree  import ElementTree

app = Flask(__name__)

# Debug logging
import logging
import sys
# Defaults to stdout
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
try: 
    log.info('Logging to console')
except:
    _, ex, _ = sys.exc_info()
    log.error(ex.message)


def index():
    return render_template('index.html')

@app.route('/')
def show_article():
    url_to_clean = request.args.get('url_to_clean')
    if not url_to_clean:
        a= {
	    'authors': '', 
	    'title': '',
	    'text': '',
	    'keywords': '',
	    'summary': ''
	  }
	Response(json.dumps(a),  mimetype='application/json')

    article = Article(url_to_clean)
    article.download()
    article.parse()

    try:
      html_string = ElementTree.tostring(article.clean_top_node)
    except:
      html_string = "Error converting html to string."

    try:
      article.nlp()
    except:
      log.error("Couldn't process with NLP")

    a = {
	 'authors': str(', '.join(article.authors)), 
	 'title': article.title,
	 'text': article.text,
	 'keywords': str(', '.join(article.keywords)),
	 'summary': article.summary
	 }
    return Response(json.dumps(a),  mimetype='application/json')
