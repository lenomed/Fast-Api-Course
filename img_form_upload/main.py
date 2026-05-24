from genericpath import exists
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil

from jinja2.utils import htmlsafe_json_dumps

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')
UPLOAD_DIR = 'static/uploads/'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get('/', response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post('/uploads', response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer) 
    
    file_info = {
        'filename': file.filename,
        'content_type': file.content_type,
        'image_url': f"/static/uploads/{file.filename}"
    }

    return templates.TemplateResponse("result_img.html", {"request": request, "file_info": file_info})
