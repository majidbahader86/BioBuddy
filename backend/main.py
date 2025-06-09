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

# Load .env variables
load_dotenv()
GWDG_API_KEY = os.getenv("GWDG_API_KEY")

if not GWDG_API_KEY:
    raise RuntimeError("GWDG_API_KEY not found in .env file or environment variables!")

app = FastAPI(title="BioBuddy Image Classifier & Lab Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load ResNet50 model
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
transform = weights.transforms()

UPLOAD_DIR = "uploads"
HISTORY_FILE = "history.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load or initialize history
try:
    with open(HISTORY_FILE, "r") as f:
        prediction_history = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    prediction_history = []

# Upload and predict image endpoint
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # ✅ Check if uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

    # Save image
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Transform and predict
    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)
        class_idx = predicted.item()

    class_name = weights.meta["categories"][class_idx] if "categories" in weights.meta else "Unknown"
    confidence_score = confidence.item()

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

# Return prediction history
@app.get("/history/")
def get_prediction_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

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
                "messages": [{"role": "user", "content": q.question}]
            },
            timeout=20  # More time, just in case
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
