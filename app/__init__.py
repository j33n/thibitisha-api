"""
	 Initialize the app
"""
from flask import Flask
import json
import requests
import firebase_admin
from firebase_admin import credentials, db

from flask import Flask, abort, request
from bs4 import BeautifulSoup

# Authenticate Firebase
cred = credentials.Certificate("../firebase_creds.json")
firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://thibitisha-36660.firebaseio.com'
})

app = Flask(__name__, instance_relative_config=True)

@app.route('/', methods=['GET'])
def home():
  return "Welcome"

@app.route('/scrape', methods=['POST'])
def scrape():
  if not request.json:
    abort(400)
  url = request.json['url']
  page = requests.get(url)
  # Create a BeautifulSoup object
  soup = BeautifulSoup(page.text, 'html.parser')
  
  # Pull text from all instances of <meta> tag within BodyText div
  get_metadata = soup.find_all('meta')
  
  for datum in get_metadata:
    if datum.get("property", None) == "og:title":
      print(datum.get("content", None))
    elif datum.get("property", None) == "og:url":
      print(datum.get("content", None))
  return url

app.config.from_object('config')