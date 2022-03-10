import json
import os
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends
from PyPDF2 import PdfFileReader
from backend.app import oauth2

router = APIRouter()


@router.post("/highlights")
async def create_upload_file(
    file: UploadFile = File(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    def checkFile(fullfile):
        with open(fullfile, "rb") as f:
            try:
                pdf = PdfFileReader(f)
                info = pdf.getDocumentInfo()
                return bool(info)
            except Exception:
                return False

    filename = "".join(c for c in file.filename if c.isalpha())

    with open(f"{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if checkFile(filename) is False:
        os.remove(filename)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This file is not a pdf or it is corrupted",
        )
    extract = os.system(f"pdfannots {filename} --f json -o {filename}.json")
    if extract != 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="extraction failed"
        )

    with open(f"{filename}.json", "r") as j:
        contents = json.load(j)
    os.remove(f"{filename}.json")
    os.remove(f"{filename}")

    return contents
