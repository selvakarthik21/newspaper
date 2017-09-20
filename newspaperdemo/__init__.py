from flask import Flask, request, render_template, redirect, url_for,jsonify
from .source import Article
from xml.etree  import ElementTree

app = Flask(__name__)

# Debug logging
import logging
import sys
import twitter
# Defaults to stdout
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
try: 
    log.info('Logging to console')
except:
    _, ex, _ = sys.exc_info()
    log.error(ex.message)

@app.route('/articles/show')
def index():
    return render_template('index.html')

@app.route('/tweets')
def tweets():
    user = 'BCCI'
    api = twitter.Api(consumer_key='FuOSn2nnFQR6mUIgHYqkIghuv',consumer_secret='XdXhmwuAtylnfA9fhptWwlNW8MQopgVExiXpDYjIb1fPDrrcrq',access_token_key='823985712034787328-T3Zb8TPZ9cRkfPngZBqqmAfcLWpVHbR',access_token_secret='9ZcKPB6mvAHD2ZeajZ3wY7ZUY2WUjPYlIE68zOwzzGMUW')
    #print(api.VerifyCredentials())
    statuses = api.GetUserTimeline(screen_name=user)
    #print([s.text for s in statuses])
    statusText = [s.text for s in statuses]
    #print(statusText)
    return statusText

@app.route('/')
def show_article():
    url_to_clean = request.args.get('url')
    if not url_to_clean:
        return jsonify({
         'authors': '', 
         'title': '',
         'text': '',
         'keywords': '',
         'summary': '',
         'contact' : 'karthik21@live.in for further details',
         'publish_date' :''
         })

    article = Article(url_to_clean)
    article.download()
    article.parse()

    #try:
      #html_string = ElementTree.tostring(article.clean_top_node)
    #except:
      #html_string = "Error converting html to string."

    #try:
      #article.nlp()
    #except:
      #log.error("Couldn't process with NLP")

    a = {
         'authors': str(', '.join(article.authors)), 
         'title': article.title,
         'text': article.text,
         'keywords': str(', '.join(article.keywords)),
         'summary': article.summary,
         'publish_date' :article.publish_date
         }
    return jsonify(a)
