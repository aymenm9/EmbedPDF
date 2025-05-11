import pikepdf
from io import BytesIO
import hashlib
from fastapi import UploadFile
from typing import List
from fastapi.responses import StreamingResponse
import mimetypes
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


def clc_checksum(data:bytes)->str:
    h = hashlib.new('sha256')
    h.update(data)
    return h.hexdigest()