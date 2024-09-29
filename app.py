from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from api.api import API
from api.requests.gg_request import gg_Request, gg_Datatype
from api.requests.gg_programmer import Programmer
from api.requests.gg_personalizer import Personalizer
from flask_socketio import SocketIO, emit
from icalendar import Calendar, Event
import datetime
import os
import re
import threading
import json
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
    user_question = db.Column(db.Text, nullable=False)  # Storing user question
    ai_response = db.Column(db.Text, nullable=False)  # Storing AI response
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Conversation {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Initialize the database
with app.app_context():
    db.create_all()

# Define a route to register new users and log them in automatically
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in. No need to register again.', 'info')
        return redirect(url_for('personalize'))

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
        if (existing_user):
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            name=name,
            age=age,
            height=height,
            weight=weight,
            bmi=bmi,
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
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. No need to login again.', 'info')
        return redirect(url_for('personalize'))

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
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Define a protected route that requires login
@app.route('/personalize-experience', methods=['GET'])
@login_required
def personalize():
    conversations = Conversation.query.filter_by(user_id=current_user.id).all()
    return render_template('gymgeniusai.html', conversations=conversations)

from io import BytesIO
@app.route('/download/<filename>')
def download(filename):
    try:
        with open("schedules/"+filename, 'rb') as file:
            file_data = file.read()
        return send_file(BytesIO(file_data), download_name=filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/converse', methods=['POST'])
@login_required
def process_input():
    data = request.get_json()
    
    user_question = data.get('question', '').strip()

    if not user_question:
        return jsonify({'answer': 'Please enter a question.'}), 400
    conversations = Conversation.query.filter_by(user_id=current_user.id).all()


        # Manually creating a list of dictionaries
    conversations_list = []
    for conversation in conversations:
        conversations_list.append({
            'id': conversation.id,
            'user_question': conversation.user_question,
            'ai_response': conversation.ai_response,
            'user_id': conversation.user_id
        })

    # Convert the list of dictionaries to a JSON string
    conversations_json = json.dumps(conversations_list)

    if "program" in user_question or "calendar" in user_question:
        try:
            programmer = Programmer(user_question, gg_Datatype.table, openai_api)
            # Generate the workout routine from AI
            # Save the conversation to the database
            workout_schedule = programmer.make_request(conversations_json, current_user.id)
            download_link = url_for('download', filename=programmer.file.name)

            new_conversation = Conversation(
                user_question=user_question,
                ai_response='Sorry, this download link is now inactive.',
                user_id=current_user.id
            )
            db.session.add(new_conversation)
            db.session.commit()
            
            return jsonify({'answer': f'Your workout schedule is ready. Download it <a href="{download_link}">here</a>.'}), 200
        
        
        except Exception as e:
            print(f"Error in process_input: {e}")
            return jsonify({'error': str(e)}), 500

    else:
        try:
            # For non-workout questions, handle the AI's conversational response
            gg_personalizer = Personalizer(user_question, gg_Datatype.conversation, openai_api)
            ai_response = gg_personalizer.make_request(conversations_json)

            # Save the conversation to the database
            new_conversation = Conversation(
                user_question=user_question,
                ai_response=ai_response,
                user_id=current_user.id
            )
            db.session.add(new_conversation)
            db.session.commit()

            return jsonify({'answer': ai_response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)