from fastapi import FastAPI, File, UploadFile, HTTPException
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import torch
import torch.nn.functional as F
import io
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()
GWDG_API_KEY = os.getenv("GWDG_API_KEY")

app = FastAPI(title="BioBuddy Image Classifier & Lab Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Load pretrained ResNet50 model using the new torchvision weights API
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()

# Use the weights' recommended transforms (resize, crop, normalize)
transform = weights.transforms()

# Directory and file setup
UPLOAD_DIR = "uploads"
HISTORY_FILE = "history.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load existing prediction history or initialize empty
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        try:
            prediction_history = json.load(f)
        except json.JSONDecodeError:
            prediction_history = []
else:
    prediction_history = []

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """Endpoint to upload an image and get prediction from ResNet50."""
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

    # Save uploaded image to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Prepare image tensor using updated transforms
    img_tensor = transform(image).unsqueeze(0)

    # Predict with model
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)
        class_idx = predicted.item()

    # Get class name from weights metadata
    class_name = weights.meta["categories"][class_idx] if "categories" in weights.meta else "Unknown"
    confidence_score = confidence.item()

    # Record the prediction
    record = {
        "filename": file.filename,
        "predicted_class": class_name,
        "confidence_percent": round(confidence_score * 100, 2),
        "timestamp": datetime.now().isoformat()
    }
    prediction_history.append(record)
    with open(HISTORY_FILE, "w") as f:
        json.dump(prediction_history, f, indent=2)

    return record

@app.get("/history/")
def get_prediction_history():
    """Return all previous image classification results."""
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    return history

class Question(BaseModel):
    question: str

class Question(BaseModel):
    question: str

class Question(BaseModel):
    question: str

@app.post("/ask/")
async def ask_lab_question(q: Question):
    question_text = q.question
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
                    {"role": "user", "content": question_text}
                ]
            },
            timeout=15
        )

        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            return {"answer": answer.replace("\n", "<br>")}

        else:
            return {
                "error": f"LLM API error {response.status_code}",
                "details": response.text
            }
    except requests.Timeout:
        return {"error": "Request to LLM API timed out. Try again later."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}



