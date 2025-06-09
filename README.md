# BioBuddy

## Project Description
BioBuddy is a virtual assistant application designed to help newcomers in biology labs. It integrates image analysis using deep learning (ResNet50) and provides helpful information through a language model API to guide users through lab protocols and experiments efficiently.

## Features
- Image upload and analysis for biological samples using ResNet50.
- Virtual assistant powered by a language model to answer lab-related queries.
- User-friendly frontend with backend API integration.
- Keeps a history of predictions and interactions.
- Supports file uploads and image management.

## Project Structure


/backend - FastAPI backend code
/frontend - Frontend application code
/uploads - Uploaded images and user files
/images - Static images used in the app
/static - Static frontend resources like HTML
.env - Environment variables (not included in repo)
history.json - Log file for predictions and interactions
.gitignore - Git ignore rules
README.md - Project documentation



## Installation and Setup

1. Clone the repository:
git clone https://github.com/majidbahader86/BioBuddy.git
cd BioBuddy


2. Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate   # Linux

3. Install required packages:
pip install -r requirements.txt


4. Set up environment variables:
Create a .env file in the root directory.
Add necessary keys such as API tokens or configuration variables.

**Usage

**
Run Backend
uvicorn backend.main:app --reload

**
Run Frontend
python frontend/app.py

**
How to Use

Open the frontend app in your browser.

Upload images to analyze.

Ask questions to the virtual assistant.

View history of interactions.


**
API Documentation (Later)

**
Contributing

Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes (git commit -m "Add feature").

Push to your branch (git push origin feature-branch).

Open a Pull Request.

**
Known Issues / TODO

Improve model accuracy.

Add more detailed API docs.

Enhance frontend UI.

Implement user authentication.