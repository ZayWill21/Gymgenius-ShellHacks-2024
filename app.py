from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Set up the SQLite database URI and disable track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Needed for flash messages
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.String(5), nullable=False)  # Changed to String for height
    weight = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
# Define a Conversation model for storing AI conversation history
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation = db.Column(db.Text, nullable=False)  # Storing conversation data

    user_id = db.Column(db.Intger, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Conversation {self.id}>'

# Initialize the database
with app.app_context():
    db.create_all()

# Define a route to handle the root URL
@app.route('/')
def home():
    return "Welcome to AI Fitness Tracker"

# Define a route to add user data (API)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        age=data['age'],
        height=data['height'],
        weight=data['weight'],
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
    user = User.query.get(user_id)

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

# Logic to link the conversation database ID to User ID


#Collect input from Login page
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    else:  
        return jsonify({'error': 'User not found'}), 404


if __name__ == "__main__":
    app.run(debug=True)