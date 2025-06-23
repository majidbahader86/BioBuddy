# 🧬 BioBuddy — AI Lab Assistant for Molecular Biology and HPC

## 🧾 Project Description

**BioBuddy** is an interactive lab assistant built with FastAPI and Streamlit. It supports researchers and students in biology and HPC environments by:

- Answering lab-specific and HPC-related questions using a GWDG-hosted LLM
- Providing experimental protocols in detail (e.g., gel electrophoresis, PCR), reagent calculations, safety checks, and troubleshooting
- Classifying biological images using ResNet50
- Supporting newcomers to Professor Julian Kunkel’s group and GWDG

> 🔎 **Note:** This version focuses on text-based assistance and optional document upload — the image classification feature is experimental.

---

## 🚀 Features

- 🔬 **AI-Powered Q&A** — Get detailed responses for lab protocols and HPC usage
- 🧠 **LLM Integration** — Uses `meta-llama-3.1-8b-instruct` via the GWDG API
- 🖼️ **Image Classification** — Identify uploaded lab-related images using ResNet50
- 📂 **Streamlit Frontend** — Clean UI with chat history and image upload
- ⚙️ **FastAPI Backend** — Handles both text questions and image classification

---

## 📂 Folder Structure

biobuddy/
├── backend/ # FastAPI app (main.py)
├── frontend/ # Streamlit app (app.py)
├── static/ # Screenshots & uploaded media
├── history.json # Chat history log
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── .env # API key file (not tracked)
└── venv/ # Virtual environment (optional)


---

## 🧪 Technologies Used

| Component     | Description                             |
|---------------|-----------------------------------------|
| **FastAPI**   | Backend API with image and text routes  |
| **Streamlit** | Frontend UI for Q&A and uploads         |
| **PyTorch**   | ResNet50 model for image classification |
| **GWDG API**  | LLM-based Q&A model (LLaMA 3.1)         |
| **httpx**     | Async HTTP requests to LLM API          |
| **PIL**       | Image pre-processing and handling       |

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- GWDG API Key

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/majidbahader/biobuddy.git
cd biobuddy

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
# .\venv\Scripts\activate   # For Windows

# Install dependencies
pip install -r requirements.txt

Configure Environment Variables

Create a .env file in the root folder:

GWDG_API_KEY=your_gwdg_api_key

▶️ How to Use
1. Run the backend:

uvicorn backend.main:app --reload

2. In a new terminal, run the frontend:

streamlit run frontend/app.py

3. Open your browser at:

http://localhost:8501

    Enter a lab-related or HPC question

    Optionally upload a lab-related image

    Get answers or predictions in real time


    ## 📸 Example Results

These are real screenshots of BioBuddy responses and predictions:

### 1. 1X TAE Buffer Preparation  
📄 Protocol steps for preparing 1X TAE buffer for electrophoresis  
![1X TAE Buffer Protocol](static/1X_TAE_buffer_protocol.png)


---

### 2. DNA Extraction Protocol  
📄 Step-by-step guide for performing DNA extraction  
![DNA Extraction Protocol](static/DNA_extraction_protocol.png)

---

### 3. Lustre in HPC  
📄 Explanation of the Lustre file system for high-performance computing  
![Lustre HPC](static/Lustre_HPC.png)

---

### 4. SLURM Job Submission  
📄 BioBuddy explains how to submit jobs using SLURM with example scripts  
![SLURM Job Submission](static/SLURM_job_submission.png)

---

### 5. Agarose Gel Electrophoresis  
📄 Detailed lab protocol for performing gel electrophoresis  
![Agarose Gel Electrophoresis](static/agarose_gel_electrophoresis.png)

---

### 6. Cell Culture Media Classification  
🧪 Image classification using ResNet50 — predicted media flask from uploaded image  
![Cell Culture Media Image Upload](static/cell_culture_media_imageUpload.png)

---

### 7. Key Skills for HPC  
📄 Overview of skills required for a successful HPC career path  
![Key Skills for HPC World](static/key_skills_for_HPC_World.png)

---

### 8. PCR (Polymerase Chain Reaction) Protocol  
📄 Step-by-step explanation of PCR setup and cycling conditions  
![Polymerase Chain Reaction](static/polymerase_chain_reaction.png)

---