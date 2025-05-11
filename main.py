import uvicorn
from fastapi import FastAPI, UploadFile, File
from typing import List, Optional
from fastapi.responses import StreamingResponse
from io import BytesIO
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

    return await create_embedded_pdf_func(container_pdf,files,descriptions)

@app.post('/extract_embedded_pdf')
async def extract_embedded_pdf(container_pdf:UploadFile = File(...)):
    return await extract_embedded_pdf_func(container_pdf)

