from flask import Flask, render_frontend
from main import main

app = Flask(__name__)



# Route to connect the homepage
def home():
   return render_frontend('/frontend/index.html')

if __name__ == '__main__':
    app.run(debug=True)