import sqlite3
from ekbase.database.models.candidate import Candidate
from ekbase.database.models.interview import Interview
from fastapi import APIRouter, HTTPException, Request, File, UploadFile, Form
from typing import List
from ekbase.core.services.interview_core_service import InterviewCoreService
from ekbase.database.models.position import Position
from fastapi.responses import StreamingResponse
from urllib.parse import quote
from ekbase.core.models.generate_questions_request import GenerateQuestionsRequest

router = APIRouter(prefix="/interview", tags=["interview"])

@router.get("/positions")
async def get_positions():
    """获取所有岗位列表"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.get_positions()

@router.post("/positions")
async def create_position(request: Request):
    """创建新岗位"""
    request_data = await request.json()
    content = request_data.get("content")
    interview_core_service = InterviewCoreService()
    return await interview_core_service.create_position(content)

@router.put("/positions/{position_id}")
async def update_position(position_id: int, request: Request):
    """更新岗位信息"""
    request_data = await request.json()
    position = Position.from_dict(request_data)
    position.id = position_id
    interview_core_service = InterviewCoreService()
    return await interview_core_service.update_position(position)

@router.delete("/positions/{position_id}")
async def delete_position(position_id: int):
    """删除岗位"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.delete_position(position_id)

@router.get("/candidates")
async def get_candidates():
    """获取所有候选人列表"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.get_candidates()

@router.post("/candidates")
async def create_candidate(
    name: str = Form(...),
    email: str = Form(...),
    position_id: List[str] = Form(...),
    resume_content: UploadFile = File(...)
):
    """创建新候选人"""
    try:
        resume_content_data = await resume_content.read()
        if not resume_content_data:
            raise HTTPException(status_code=400, detail="简历文件不能为空")
            
        resume_binary = sqlite3.Binary(resume_content_data)
        
        position_ids = [str(pid) for pid in position_id]
        
        candidate = Candidate(
            position_id=",".join(position_ids),
            name=name,
            email=email,
            resume_content=resume_binary,
            resume_type=resume_content.filename.split(".")[-1] if resume_content else None
        )
        interview_core_service = InterviewCoreService()
        return await interview_core_service.create_candidate(candidate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/candidates/{candidate_id}")
async def update_candidate(candidate_id: int, request: Request):
    """更新候选人信息"""
    data = request.form()
    request_file = request.files['resume_content'] if 'resume_content' in request.files else None
    resume_content = request_file.read() if request_file else None
    resume_binary = sqlite3.Binary(resume_content) if resume_content is not None else None
    candidate = Candidate(
        id=candidate_id,
        position_id=",".join(data.getlist("position_id")),
        email=data.get("email"),
        resume_content=resume_binary,
        resume_type=request_file.filename.split(".")[-1] if request_file else None
    )
    interview_core_service = InterviewCoreService()
    return await interview_core_service.update_candidate(candidate)

@router.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int):
    """删除候选人"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.delete_candidate(candidate_id)

@router.get("/candidates/{candidate_id}/resume")
async def get_resume(candidate_id: int):
    """下载候选人简历"""
    interview_core_service = InterviewCoreService()
    candidate = await interview_core_service.get_resume(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    if not candidate.resume_content:
        raise HTTPException(status_code=404, detail="简历内容为空")
    
    # 确保 resume_content 是字节类型
    if isinstance(candidate.resume_content, memoryview):
        resume_content = candidate.resume_content.tobytes()
    else:
        resume_content = candidate.resume_content
    
    filename = f"resume_{candidate.name}.pdf"
    encoded_filename = quote(filename)
    
    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
    }
    return StreamingResponse(
        iter([resume_content]),  # 将字节内容包装在迭代器中
        media_type="application/octet-stream",
        headers=headers
    )

@router.post("/candidates/{interview_id}/generate_interview_questions")
async def generate_interview_questions(interview_id: int, request: GenerateQuestionsRequest):
    """生成面试题"""
    interview_core_service = InterviewCoreService()
    await interview_core_service.generate_interview_questions(
        interview_id, 
        request.question_count, 
        request.with_example_answer,
        request.append
    )
    return True
    

@router.get("/interviews")
async def get_interviews():
    """获取所有面试列表"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.get_interviews()

@router.post("/interviews")
async def create_interview(request: Request):
    """创建新面试"""
    request_data = await request.json()
    interview = Interview.from_dict(request_data)
    interview_core_service = InterviewCoreService()
    return await interview_core_service.create_interview(interview)

@router.put("/interviews/{interview_id}")
async def update_interview(request: Request):
    """更新面试信息"""
    request_data = await request.json()
    interview = Interview(request_data)
    interview_core_service = InterviewCoreService()
    return await interview_core_service.update_interview(interview)

@router.delete("/interviews/{interview_id}")
async def delete_interview(interview_id: int):
    """删除面试"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.delete_interview(interview_id)

@router.get("/interviews/{interview_id}/report")
async def get_interview_report(interview_id: int):
    """下载面试报告"""
    interview_core_service = InterviewCoreService()
    report = await interview_core_service.get_interview_report(interview_id)
    if not report:
        raise HTTPException(status_code=404, detail="面试报告不存在")
    
    headers = {
        "Content-Disposition": f"attachment; filename=report_{interview_id}.pdf"
    }
    return StreamingResponse(report, media_type="application/octet-stream", headers=headers)

@router.get("/interviews/{interview_token}/info")
async def get_interview_info(interview_token: str):
    """获取面试信息"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.get_interview_info(interview_token)

@router.get("/interviews/{interview_token}/get_question")
async def get_question(interview_token: str, page: int = 1, page_size: int = 10):
    """获取面试问题
    
    Args:
        interview_token: 面试令牌
        page: 页码，从1开始
        page_size: 每页问题数量，默认10个
    """
    interview_core_service = InterviewCoreService()
    return await interview_core_service.get_question(interview_token, page, page_size)

@router.get("/interviews/{interview_token}/get_example_answer")
async def get_example_answer(interview_token: str, question_id: int):
    """获取示例答案"""
    interview_core_service = InterviewCoreService()
    return await interview_core_service.get_example_answer(interview_token, question_id)

@router.post("/interviews/{interview_token}/submit_answer")
async def submit_answer(
    interview_token: str,
    question_id: int = Form(...),
    audio_answer: UploadFile = File(None),
    text_answer: str = Form(None)
):
    """
    提交面试答案
    """
    interview_core_service = InterviewCoreService()
    await interview_core_service.check_token(interview_token)
    
    return await interview_core_service.submit_answer(
        interview_token=interview_token,
        question_id=question_id,
        audio_answer=audio_answer,
        text_answer=text_answer
    )

@router.post("/interviews/{interview_token}/toggle_voice_reading")
async def toggle_voice_reading(interview_token: str, request: Request):
    """切换语音朗读状态"""
    interview_core_service = InterviewCoreService()
    request_data = await request.json()
    enabled = request_data.get('enabled')
    return await interview_core_service.toggle_voice_reading(interview_token, enabled)

