import uvicorn
from fastapi import FastAPI, UploadFile, File
from typing import List, Optional
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from pikepdf import PdfError
from util import create_embedded_pdf_func, extract_embedded_pdf_func

app = FastAPI()


@app.get('/')
async def root():
    return {'msg':'hello,world!'}


@app.post('/create_embedded_pdf')
async def create_embedded_pdf(
    container_pdf:UploadFile = File(...),
    files:List[UploadFile]=File(...), 
    descriptions: Optional[List[str]]=None
    )->StreamingResponse:
    try:
        return await create_embedded_pdf_func(container_pdf,files,descriptions)
    except PdfError:
        raise HTTPException(status_code=400, detail="Corrupted or unsupported PDF.")

@app.post('/extract_embedded_pdf')
async def extract_embedded_pdf(container_pdf:UploadFile = File(...))->StreamingResponse:
    try:
        return await extract_embedded_pdf_func(container_pdf)
    except PdfError:
        raise HTTPException(status_code=400, detail="Corrupted or unsupported PDF.")

