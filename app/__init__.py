"""
	 Initialize the app
"""
from flask import Flask
app = Flask(__name__, instance_relative_config=True)

@app.route('/', methods=['GET'])
def home():
  return "Welcome"
app.config.from_object('config')