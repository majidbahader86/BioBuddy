from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from PIL import Image
import logging
import io
import os
import httpx
import torch
from torchvision import models, transforms

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
GWDG_API_KEY = os.getenv("GWDG_API_KEY")
GWDG_API_URL = os.getenv("GWDG_API_URL", "https://chat-ai.academiccloud.de/v1/chat/completions")

if not GWDG_API_KEY:
    raise RuntimeError("GWDG_API_KEY not found in environment variables or .env file")

# Initialize FastAPI app
app = FastAPI(title="BioBuddy Lab Assistant")

# ✅ Mount static folder (from parent directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Load and prepare ResNet50 model
resnet50 = models.resnet50(pretrained=True)
resnet50.eval()

# Load ImageNet class names
imagenet_path = os.path.join(os.path.dirname(__file__), "imagenet_classes.txt")
with open(imagenet_path, "r") as f:
    imagenet_classes = [line.strip() for line in f.readlines()]

# Define preprocessing steps
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Pydantic model for question input
class Question(BaseModel):
    question: str

# ✅ Endpoint: Upload and classify image using ResNet50
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        tensor = preprocess(image).unsqueeze(0)

        with torch.no_grad():
            output = resnet50(tensor)
        probs = torch.nn.functional.softmax(output[0], dim=0)
        confidence, idx = torch.max(probs, 0)
        label = imagenet_classes[idx]

        return {
            "predicted_class": label,
            "confidence_percent": round(confidence.item() * 100, 2)
        }
    except Exception as e:
        logging.error(f"Image classification error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Endpoint: Ask GWDG API a question
@app.post("/ask/")
async def ask_lab_question(q: Question):
    logging.info(f"User asked: {q.question}")

    system_prompt = (
        "You are BioBuddy, an expert assistant for Professor Julian Kunkel's lab at GWDG Göttingen. "
        "You can answer detailed questions about high-performance computing (HPC), storage systems like Lustre, SLURM job scheduling, "
        "lab protocols in molecular biology, bioinformatics workflows, and general science topics. "
        "For lab-specific questions, provide step-by-step guidance; for general questions, be clear and concise."
    )

    payload = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q.question}
        ],
        "max_tokens": 1500,
        "temperature": 0.5
    }

    headers = {
        "Authorization": f"Bearer {GWDG_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(GWDG_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as exc:
        logging.error(f"GWDG API HTTP error: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as exc:
        logging.error(f"Unexpected error: {str(exc)}")
        raise HTTPException(status_code=500, detail=str(exc))

    try:
        answer = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        logging.error(f"Response parsing error: {data}")
        raise HTTPException(status_code=502, detail="Invalid response format from GWDG API")

    return {"answer": answer}
