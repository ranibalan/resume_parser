ffrom fastapi import FastAPI, UploadFile, File
import os, shutil
from extract_ocr import extract_text, extract_name

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png", ".docx"]


@app.post("/extract-name/")
async def extract_resume_name(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    
    if ext not in ALLOWED_EXTENSIONS:
        return {
            "error": "Only PDF, Image (JPG/PNG), and DOCX files are supported"
        }

    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    text = extract_text(file_path)
    name = extract_name(text)

    return {
        "file_name": file.filename,
        "extracted_name": name
    }