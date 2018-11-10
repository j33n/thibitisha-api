from flask import Flask, render_template,request
app = Flask(__name__)


@app.route('/')
def index():
    #returns the landing page
  return render_template("mainSite.html")

@app.route('/name/',methods=['POST'])
def post_me():
  email = request.form['email']
  password = request.form['password']
  #TODO:to check with db if successfull
  return render_template('two.html')


if __name__ == '__main__':
  app.jinja_env.auto_reload =True
  app.config['TEMPLATES_AUTO_RELOAD']=True
  app.run(debug=True)
 
