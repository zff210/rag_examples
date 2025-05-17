from fastapi import APIRouter, HTTPException, UploadFile, File
from ekbase.core.services.document_service import DocumentCoreService

router = APIRouter(prefix="/documents", tags=["documents"])

# 上传文档
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档"""
    document_service = DocumentCoreService()
    document = await document_service.upload_document(file)
    return document