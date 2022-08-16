from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@cluster0.zk7c2.mongodb.net/dbKinder?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def login():
  return render_template('login.html')



if __name__ == "__main__":
  app.run(debug=True, port=5000)