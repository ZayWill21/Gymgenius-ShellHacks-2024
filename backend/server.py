from flask import Flask, render_frontend

app = Flask(__name__)


# Route to connect the homepage
def home():
   return render_frontend('')

if __name__ == '__main__':
    app.run(debug=True)