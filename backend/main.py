from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
import requests


# Load .env variables
load_dotenv()
GWDG_API_KEY = os.getenv("GWDG_API_KEY")

if not GWDG_API_KEY:
    raise RuntimeError("GWDG_API_KEY not found in .env file or environment variables!")

app = FastAPI(title="BioBuddy Lab Assistant")

# Define model for lab assistant question
class Question(BaseModel):
    question: str

# Ask the LLM
@app.post("/ask/")
async def ask_lab_question(q: Question):
    try:
        response = requests.post(
            "https://chat-ai.academiccloud.de/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GWDG_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama-3.1-8b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are BioBuddy, a smart assistant for biology and computer science researchers. "
                            "You can answer general questions in science, HPC, storage systems, lab procedures, programming, and Linux. "
                            "When the question is related to Professor Julian Kunkel’s lab at GWDG, provide accurate, lab-specific guidance on HPC tools, SLURM, Lustre, or documentation tools used in the lab. "
                            "Be helpful, precise, and always explain step-by-step if needed."
                        )
                    },
                    {"role": "user", "content": q.question}
                ]
            },
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            return {"answer": data['choices'][0]['message']['content'].replace("\n", "<br>")}
        else:
            return {"error": f"LLM error {response.status_code}", "details": response.text}

    except requests.Timeout:
        return {"error": "LLM API timeout. Please try again later."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

