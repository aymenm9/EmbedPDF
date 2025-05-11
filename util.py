import pikepdf
from io import BytesIO
import hashlib
from fastapi import UploadFile
from typing import List
from fastapi.responses import StreamingResponse
import mimetypes
import zipfile
async def create_embedded_pdf_func(main_pdf:UploadFile,files:List[UploadFile],descriptions:List[str]=None)->StreamingResponse:
    pdf_content = await main_pdf.read()
    with pikepdf.open(BytesIO(pdf_content)) as pdf:

        for i,file in enumerate(files):
            file_data = await file.read()
            checksum = clc_checksum(file_data)
            file_spec = pikepdf.AttachedFileSpec(pdf,file_data,mime_type=file.content_type)
            pdf.attachments[file.filename] = file_spec
            if '/EF' in file_spec.obj and '/F' in file_spec.obj['/EF']:
                embedded_file = file_spec.obj["/EF"]["/F"]
                if '/Params' not in embedded_file:
                    embedded_file['/Params'] = pikepdf.Dictionary()
                embedded_file['/Params']['/Checksum'] = pikepdf.String(f'sha256:{checksum}')
            
        output = BytesIO()
        pdf.save(output)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={main_pdf.filename}.pdf"}
        )

async def extract_embedded_pdf_func(container_pdf:UploadFile):
    pdf_content = await container_pdf.read()
    files = []
    zip_buffer = BytesIO()
    zip_filename = f'{container_pdf.filename.strip('.pdf')}_attachments.zip'
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        with pikepdf.open(BytesIO(pdf_content)) as pdf:
            for file_name,file_spec in pdf.attachments.items():
                embedded_file = file_spec.obj["/EF"]["/F"]
                file_data = embedded_file.read_bytes()
                try:
                    print(str(embedded_file['/Params'].get('/Checksum')).split(':')[1],'\n',clc_checksum(file_data))
                    if str(embedded_file['/Params'].get('/Checksum')).split(':')[1] == clc_checksum(file_data):
                        print('appandin file :',file_name)
                        zip_file.writestr(file_name,file_data)
                except:
                    pass
    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={zip_filename}",
            "Content-Type": "application/zip"
        }
        )
def clc_checksum(data:bytes)->str:
    h = hashlib.new('sha256')
    h.update(data)
    return h.hexdigest()