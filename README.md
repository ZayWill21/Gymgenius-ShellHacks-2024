# 2024 SHELLHACKS COMPETITION
# Gymgenius 🏋️‍♀️💡
Welcome to Gymgenius, the AI-powered fitness app designed to help you meet your gym goals in a personalized and intelligent way. Our app allows users to interact with an AI assistant, offering tailored workout plans and actionable insights to help make the world a healthier place!

# 🚀 About ShellHacks @ FIU
This project was created during ShellHacks, Florida International University’s premier hackathon. At ShellHacks, teams from all over come together to innovate, build, and solve problems. In the spirit of health and technology, we built Gymgenius to make fitness more accessible and personalized for everyone.

# 🌍 Our Mission
Our goal is to make the world a healthier place by giving users easy access to customized workout plans and actionable data on their progress, as well as educating our Users in fitness and healthy habits. Whether you're a fitness enthusiast or just getting started, Gymgenius adapts to your needs and helps you stay on track with your goals.

# 🛠️ Technologies Used
Infrastructure:
Terraform: We used Terraform to provision and manage our cloud infrastructure.
Azure App Services: Gymgenius is deployed using Azure App Services, ensuring scalability and security for our application.
GitHub Actions: Automated CI/CD pipelines were set up using GitHub Actions to run tests and deploy our application seamlessly.

Backend:
Python: The core of Gymgenius is powered by Python.
Flask: We built a lightweight, scalable REST API with Flask.
SQLAlchemy: SQLAlchemy was used to interact with our database and manage user data, workout plans, and performance tracking.
OpenAI API: The AI bot integration allows users to have conversations and receive personalized workout plans based on their goals and fitness levels.

Frontend:
HTML, CSS, and JavaScript: The responsive frontend is built using standard web technologies, ensuring a smooth and interactive user experience across devices.
We designed user-friendly interfaces to display workout plans, progress charts, and interactive chat with the AI assistant.

# ⚙️ How It Works
AI-Powered Fitness Plans: After signing up, users interact with our AI bot, powered by OpenAI API, to define their fitness goals and receive a customized workout plan.
Interactive Charts: Users can track their gym progress through charts and analytics, which update dynamically based on the user's input and workout data.
Seamless Deployment & Testing: Our infrastructure is provisioned using Terraform and deployed on Azure App Services. We use GitHub Actions for automated testing and deployment, ensuring a reliable and smooth development workflow.
# 🚶 Getting Started
To get started with Gymgenius, follow these steps:

Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/gymgenius.git
cd gymgenius
Set up the Python environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
Set up environment variables: Create a .env file in the root of the project with your OpenAI API key and other necessary configurations.

Run the app locally:

# bash
Copy code
flask run
Deployment: Gymgenius is deployed using Terraform and Azure App Services. Ensure you have the necessary credentials and configurations to deploy the app.

or 

Use this link: https://gymgenius-2024-d6a9gacag5fqg2gy.eastus2-01.azurewebsites.net/login

# 🤝 Contributing
We welcome contributions! If you'd like to contribute to Gymgenius, feel free to fork the repository, create a new branch, and submit a pull request. We encourage collaboration to further improve this project and make fitness accessible for all.

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

# 💡 Acknowledgements
ShellHacks @ FIU: For the opportunity to build Gymgenius and be part of an amazing hackathon experience.
Azure: For providing the platform to host and deploy our app.
OpenAI: For powering the AI bot that makes personalized plans possible.
Let’s make the world a healthier place, one gym goal at a time!
