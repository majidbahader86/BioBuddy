# BioBuddy 🧬

## Project Description

**BioBuddy** is a virtual lab assistant designed to support newcomers in biology labs. It helps with experimental protocols, reagent calculations, safety checks, and troubleshooting — all through a natural language interface powered by an LLM (Language Model).

This version focuses on text-based assistance and optional document upload — no image classification is included in this version.

---

## Features

- 🔬 Ask lab-related questions and get immediate responses
- 🧠 Powered by a language model (LLM API)
- 📎 Optional upload of lab-related files for future context
- 🖥️ Simple, clean frontend using Streamlit
- ⚙️ FastAPI backend for LLM interaction

---

## Project Structure



/backend # FastAPI backend code
/frontend # Streamlit frontend code
/uploads # Folder for future file support
.env # Environment variables (not in repo)
README.md # Project documentation
.gitignore # Git ignore rules


---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/majidbahader86/BioBuddy.git

cd BioBuddy

#Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies

pip install -r requirements.txt

Set up environment variables

Create a .env file in the root folder and add:

OPENAI_API_KEY=your_key_here

Usage
1. Run Backend

uvicorn backend.main:app --reload

2. Run Frontend

streamlit run frontend/app.py

How to Use

    Open the Streamlit app in your browser.

    Type your lab-related question.

    Optionally upload a file to support your query.

    Get real-time answers from the assistant.

Contributing

    Fork the repository

    Create a new branch: git checkout -b feature-branch

    Make your changes

    Commit: git commit -m "Add feature"

    Push: git push origin feature-branch

    Open a Pull Request

Future Plans

    🔄 Integrate lab document parsing (PDFs, protocols)

    🔐 Add user login and session-based history

    📊 Support for reagent and buffer calculators

    🧪 Protocol templates and visualization