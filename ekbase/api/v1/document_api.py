from http.client import HTTPException
from fastapi import APIRouter, UploadFile, File
from ekbase.core.services.document_core_service import DocumentCoreService

router = APIRouter(prefix="/documents", tags=["documents"])

# 上传文档
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档"""
    try:
        document_service = DocumentCoreService()
        document = await document_service.upload_document(file)
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 重建索引
@router.post("/reload_index")
async def reload_index():
    """重建索引"""
    try:    
        document_service = DocumentCoreService()
        document_service.reload_index()
        return {"message": "索引重建成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_all")
async def list_documents():
    """列出所有文档"""
    try:
        document_service = DocumentCoreService()
        documents = document_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """删除文档"""
    try:
        document_service = DocumentCoreService()
        document_service.delete_document(document_id)
        return {"message": "文档删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_index_status")
async def get_index_status():
    """获取索引状态"""
    try:
        document_service = DocumentCoreService()
        return document_service.get_index_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset_index/{document_id}")
async def reset_index(document_id: str):
    """重置索引"""
    try:
        document_service = DocumentCoreService()
        document_service.reset_index(document_id)
        return {"message": "索引重置成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
