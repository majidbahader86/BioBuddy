# 🧬 BioBuddy — AI Lab Assistant for Molecular Biology and HPC

## Project Description


**BioBuddy** is an interactive lab assistant built with FastAPI and Streamlit. It supports researchers and students in biology and HPC environments by:

- Answering lab-specific and HPC-related questions using a GWDG-hosted LLM
- Providing experimental protocols in detail (e.g., gel electrophoresis, PCR), reagent calculations, safety checks, and troubleshooting
- Classifying biological images using ResNet50
- Supporting newcomers to Professor Julian Kunkel’s group and GWDG

---

This version focuses on text-based assistance and optional document upload — no image classification is included in this version.

---

## 🚀 Features

- 🔬 **AI-Powered Q&A** — Get detailed responses for bio lab protocols and HPC usage
- 🧠 **LLM Integration** — Uses `meta-llama-3.1-8b-instruct` via the GWDG API
- 🖼️ **Image Classification** — Classify uploaded images using ResNet50 (ImageNet-trained)
- 📂 **Streamlit Frontend** — Simple, responsive UI with chat and history
- ⚙️ **FastAPI Backend** — Robust backend for both text and image endpoints

---

## 📂 Folder Structure

biobuddy/
├── backend/
│ └── main.py # FastAPI app
├── frontend/
│ └── app.py # Streamlit interface
├── static/ # Screenshots & media
├── requirements.txt # Project dependencies
├── .env # API keys (not committed)
├── README.md # Project documentation


## ## 📸 Example Results

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


## 🧪 Technologies Used

| Component     | Description                             |
|---------------|-----------------------------------------|
| **FastAPI**   | Backend API with image and text routes  |
| **Streamlit** | Frontend UI for question input + upload |
| **PyTorch**   | ResNet50 image classification           |
| **GWDG API**  | LLM-based Q&A model (meta-llama-3.1)    |
| **httpx**     | Async HTTP client for model calls       |
| **PIL**       | Image processing for uploads            |




---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- GWDG API Key

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/majidbahader86/BioBuddy
cd biobuddy

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # For Linux

# Install dependencies
pip install -r requirements.txt

Configure Environment Variables

Create a .env file in the root folder:

GWDG_API_KEY=gwdg_api_key

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


Contributing

    Fork the repository

    Create a new branch: git checkout -b feature-branch

    Make your changes

    Commit: git commit -m "Add feature"

    Push: git push origin feature-branch

    Open a Pull Request

👤 Author

Majid Bahader
Python Backend Developer | Molecular Biologist
Intern at GWDG Göttingen
Mentored by Prof. Julian Kunkel


🙏 Acknowledgments

    Professor Julian Kunkel — for domain guidance and mentorship

    GWDG Academic Cloud — for providing LLM access and infrastructure

    All open-source libraries that power this project