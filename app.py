from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from api.api import API
from api.requests.gg_request import gg_Request, gg_Datatype
from api.requests.gg_programmer import Programmer
from api.requests.gg_personalizer import Personalizer
from flask_socketio import SocketIO, emit

import threading

# library to plot graph don't know if using yet

# importing BMI calculation functions
from fitness_utils import height_to_meters, weight_to_kg, calculate_bmi, generate_weight_graph 

app = Flask(__name__)

# Set up the SQLite database URI and disable track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Needed for flash messages
socketio = SocketIO(app, async_mode='threading')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
openai_api = API()

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Route for login page

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.String(5), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
# Define a Conversation model for storing AI conversation history
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation = db.Column(db.Text, nullable=False)  # Storing conversation data

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Conversation {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the database
with app.app_context():
    db.create_all()


# Define a route to handle the root URL
@app.route('/')
def home():
    return "Welcome to AI Fitness Tracker"

# Define a route to register new users and log them in automatically
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in. No need to register again.', 'info')
        return redirect(url_for('personalize'))  # Redirect to the personalize page or wherever you want

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']

        # Split height into feet and inches
        try:
            height_parts = height.split("'")
            feet = int(height_parts[0])
            inches = int(height_parts[1].replace('"', ''))
        except (IndexError, ValueError):
            flash("Invalid height format. Please select from the dropdown.", 'danger')
            return redirect(url_for('register'))
        

        weight = float(weight)

        try:
            bmi = calculate_bmi(weight, feet, inches)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('register'))



        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            name=name,
            age=age,
            height=height,
            weight=weight,
            gender=gender,
            email=email,
            password=password  # In a real app, make sure to hash passwords
        )
        db.session.add(new_user)
        db.session.commit()

        # Automatically log the user in
        login_user(new_user)
        
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('personalize'))

    return render_template('registration.html')

# Define a route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. No need to login again.', 'info')
        return redirect(url_for('personalize'))  # Redirect to the personalize page or wherever you want

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query for the user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:  # In a real app, you should verify hashed passwords
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('personalize'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    
    return render_template('login.html')

# Define a route for logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Define a protected route that requires login
@app.route('/personalize-experience', methods=['GET'])
@login_required
def personalize():
    return render_template('gymgeniusai.html')

@app.route('/converse', methods=['POST'])
@login_required
def process_input():
    data = request.get_json()
    
    user_question = data.get('question', '').strip()  # Strip whitespace

    if not user_question:  # Check for empty input
        return jsonify({'answer': 'Please enter a question.'}), 400

    try:
        # Initialize Personalizer instance for the AI request
        gg_personalizer = Personalizer(user_question, gg_Datatype.conversation, openai_api)

        # Make the AI request synchronously (wait for response)
        ai_response = gg_personalizer.make_request("Gain muscle, lose weight, get stronger, defend yourself")
        print(ai_response)
        # Return the AI response to the user
        return jsonify({'answer': ai_response}), 200

    except Exception as e:
        # Handle any potential exceptions
        return jsonify({'answer': f"An error occurred: {str(e)}"}), 500
    
# Define a route to add user data (API)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        age=data['age'],
        height=data['height'],
        weight=data['weight'],
        bmi = data['bmi'],
        gender=data['gender'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# Define a route to get user data (API)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "age": user.age, "height": user.height, "weight": user.weight} for user in users]
    return jsonify(users_list), 200

# Define a route to add a new conversation (API)
@app.route('/add_conversation', methods=['POST'])
def add_conversation():
    data = request.get_json()
    conversation_text = data.get('conversation')
    user_id = data.get('user_id') #Expecting the User_id in the request data

    # Find the user associated with the provided user_id
    user = User.query.filter_by(user_id).first()

    if not user:
        return jsonify({'error':'User not found'}), 404 

    # Create and save new conversation to the database
    new_conversation = Conversation(conversation=conversation_text)
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({'message': 'Conversation added successfully'}), 201

# Define a route to get all conversations (API)
@app.route('/conversations', methods=['GET'])
def get_conversations(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    conversations = Conversation.query.filter_by(user_id=user_id).all()
    conversations_list = [{"id": conv.id, "conversation": conv.conversation} for conv in conversations]
    return jsonify(conversations_list), 200

# Define a route to render the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(
            name=name,
            age=age,
            height=height,
            weight=weight,
            gender=gender,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    
    return render_template('registration.html')

if __name__ == "__main__":
    app.run(debug=True)