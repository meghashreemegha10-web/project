from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.services.parser import ResumeParser
from app.services.analyzer import ResumeAnalyzer
import shutil
import os
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

parser = ResumeParser()
analyzer = ResumeAnalyzer()

@router.get("/")
async def get_upload_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/analyze")
async def analyze_resume(request: Request, file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
         return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "Invalid file type. Only PDF and DOCX are supported."
        })
    
    # Save file temporarily
    filename = f"{uuid.uuid4()}_{file.filename}"
    upload_dir = "/tmp"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse
        parsed_data = await parser.parse_file(file_path, file.filename)
        
        # Analyze
        analysis_result = analyzer.analyze(parsed_data.text)
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "filename": file.filename,
            "score": analysis_result.score,
            "summary": analysis_result.summary,
            "found_skills": analysis_result.found_skills,
            "missing_skills": analysis_result.missing_critical_skills
        })
        
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": f"Error processing resume: {str(e)}"
        })
    finally:
        # Cleanup file after processing
        if os.path.exists(file_path):
            os.remove(file_path)
