## How to run
```bash
    docker-compose up
```
vist : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



### `POST /create_embedded_pdf`

**Description**  
Embeds one or more files into a container PDF.

**Request Parameters**
- `container_pdf` (UploadFile) — The main PDF file to embed files into.
- `files` (List[UploadFile]) — Files to be embedded.
- `descriptions` (Optional[List[str]]) — Optional descriptions for the embedded files.

**Response**
- `StreamingResponse`: A new PDF file with embedded attachments.

**Errors**
- `400 Bad Request`: Returned if the PDF is corrupted or unsupported.

---

### `POST /extract_embedded_pdf`

**Description**  
Extracts embedded files from a PDF.

**Request Parameters**s
- `container_pdf` (UploadFile) — The PDF file containing embedded files.

**Response**
- `StreamingResponse`: A ZIP (or similar) file containing the extracted files.

**Errors**
- `400 Bad Request`: Returned if the PDF is corrupted or unsupported.
