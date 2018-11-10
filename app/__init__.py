"""
	 Initialize the app
"""
import json
import os
import datetime
from flask import Flask, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, db

from firebase import firebase

from flask import Flask, abort, request
from bs4 import BeautifulSoup

from dotenv import load_dotenv

# Load Environment variables
load_dotenv()

# Authenticate Firebase
cred = credentials.Certificate(os.getenv("GOOGLE_KEY_PATH"))
firebase_admin.initialize_app(cred)

firebase = firebase.FirebaseApplication('https://thibitisha-36660.firebaseio.com', None)

app = Flask(__name__, instance_relative_config=True)

@app.route('/', methods=['GET'])
def home():
  return "Welcome"

@app.route('/scrape', methods=['POST'])
def create_post():
  if not request.json:
    abort(400)
  url = request.json['url']
  page = requests.get(url)
  # Create a BeautifulSoup object
  soup = BeautifulSoup(page.text, 'html.parser')
  
  # Pull text from all instances of <meta> tag within BodyText div
  get_metadata = soup.find_all('meta')

  fb_obj = {}
  twitter_obj = {}
  # Get possible metadata and add them to their specific objects
  # TODO: Change to using a central point function
  for datum in get_metadata:
    # Case Facebook
    if datum.get("property", None) == "og:url":
      fb_obj.update({'url': datum.get("content", None)})
    elif datum.get("property", None) == "og:title":
      fb_obj.update({'title': datum.get("content", None)})
    elif datum.get("property", None) == "og:description":
      fb_obj.update({'description': datum.get("content", None)})
    elif datum.get("property", None) == "og:image":
      fb_obj.update({'image': datum.get("content", None)})
    # Case Twitter
    elif datum.get("name", None) == "twitter:url":
      twitter_obj.update({'url': datum.get("content", None)})
    elif datum.get("name", None) == "twitter:title":
      twitter_obj.update({'title': datum.get("content", None)})
    elif datum.get("name", None) == "twitter:description":
      twitter_obj.update({'description': datum.get("content", None)})
    elif datum.get("name", None) == "twitter:image":
      twitter_obj.update({'image': datum.get("content", None)})

  # Check Which object is more solid
  def which_is_better(fb_obj, twitter_obj):
    if(len(twitter_obj) > len(fb_obj)):
      return twitter_obj
    else:
      return fb_obj
  
  new_post = which_is_better(fb_obj, twitter_obj)

  timestamp = str(datetime.datetime.now())
  new_post.update({'time': timestamp})

  # save_in_firebase
  firebase.post('/posts', new_post, params={'print': 'pretty'})

  return json.dumps(new_post)

@app.route('/posts', methods=['GET'])
def fetch_posts():
  result = firebase.get('/posts', None)
  return json.dumps(result)

@app.route('/sign_up', methods=['POST'])
def sign_up():
  if not request.json:
    abort(400)
  new_user = request.json
  # save_in_firebase
  result = firebase.post('/users', new_user, params={'print': 'pretty'})
  return json.dumps(result), 201

@app.route('/login', methods=['POST'])
def login():
  if not request.json:
    abort(400)
  email = request.json['email']
  password = request.json['password']
  result = firebase.get('/users', None)
  print(">>>>>>>>>>>>>>", result)
  return True

@app.route('/upvote', methods=['POST'])
def upvote():

  return "upvote"

@app.route('/downvote', methods=['POST'])
def downvote():
  return "downvote"

@app.route('/comment', methods=['POST'])
def comment():
  return "comment"

app.config.from_object('config')