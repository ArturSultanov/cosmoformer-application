from fastapi import HTTPException, UploadFile, status
from config import settings

def validation(file: UploadFile):
    
    if file.content_type not in settings.ACCEPTED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Supported types: {settings.ACCEPTED_MIME_TYPES}"
        )
