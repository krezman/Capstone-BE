# Getting the backend framework set up
from flask import Flask, jsonify, after_this_request

# Dependency for .env file
import os
from dotenv import load_dotenv

# Setting up CORS dependency
from flask_cors import CORS

# Retrieving the models
import models

# Blueprint import
from resources.users import users
from resources.posts import posts


load_dotenv()
DEBUG =True
PORT = os.environ.get("PORT")

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET")



# Auth dependencies
from flask_login import LoginManager
login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None
    
CORS(users, origins=['http://localhost:3000', 'https://yourday.herokuapp.com/'])
CORS(posts, origins=['http://localhost:3000', 'https://yourday.herokuapp.com/'])


app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(posts, url_prefix='/api/v1/posts')


@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("Opened DB CONNECTION") # 
    models.DATABASE.connect()

    @after_this_request 
    def after_request(response):
        """Close the db connetion after each request"""
        print("Closed DB CONNECTION")
        models.DATABASE.close()
        return response
    
@app.route('/', methods=['GET'])
def home():
    return 'hi'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()