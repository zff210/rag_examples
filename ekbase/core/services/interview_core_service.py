from http.client import HTTPException
import json
import os
from typing import Optional
import uuid
import asyncio
import threading
from common.utils.llm_utils import LLMUtils
from ekbase.config.settings import LLM,STORAGE
from ekbase.database.models.interview import Interview
from ekbase.database.services.interview_service import InterviewService
from ekbase.database.models.candidate import Candidate
from ekbase.database.services.candidate_service import CandidateService
from ekbase.database.models.position import Position
from ekbase.database.services.position_service import PositionService
from ekbase.database.models.interview_question import InterviewQuestion
from ekbase.database.services.interview_question_service import InterviewQuestionService
from ekbase.core.services.generate_interview_questions import GenerateInterviewQuestionsService
import logging
import tempfile
import time
import whisper
import torch
from datetime import datetime
from fastapi import UploadFile
import psutil
import gc
from common.utils.speech_utils import SpeechUtils
from common.utils.vosk_utils import VoskUtils

logger = logging.getLogger(__name__)

class InterviewCoreService:
    def __init__(self):
        self.interview_service = InterviewService()
        self.candidate_service = CandidateService()
        self.position_service = PositionService()
        self.interview_question_service = InterviewQuestionService()
        config = LLM
        self.llm = LLMUtils(config)
        # 初始化两种语音识别工具
        self.whisper_utils = SpeechUtils(os.path.join(STORAGE['temp'], "whisper"))
        self.vosk_utils = VoskUtils(os.path.join(STORAGE['temp'], "vosk-model-cn"))

    async def get_positions(self):
        return await self.position_service.list_all()
    
    async def create_position(self, content: str):
        '''
        调用大模型，从content中提取出name, requirements, responsibilities， recruiter
        '''
        prompt = f"""
        请从以下内容中提取出岗位名称、岗位要求、岗位职责、招聘负责人、职位链接：
        {content}
        请以json格式返回，不要添加任何其他内容。json格式如下：
        {{
            "name": "岗位名称",
            "requirements": "岗位要求",
            "responsibilities": "岗位职责",
            "recruiter": "招聘负责人",
            "link": "职位链接"
        }}
        """
        response = self.llm.chat(
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        response = json.loads(response)
        logger.info(f"解析岗位信息，结果为：{response}")
        name = response.get("name")
        requirements = response.get("requirements")
        responsibilities = response.get("responsibilities")
        recruiter = response.get("recruiter")
        link = response.get("link")
        position = Position(
            name=name,
            requirements=requirements,
            responsibilities=responsibilities,
            quantity=2,
            status=2,
            recruiter=recruiter,
            link=link
        )
        return await self.position_service.create(position)   
    
    async def update_position(self, position: Position):
        return await self.position_service.update(position)
    
    async def delete_position(self, position_id: int):
        '''
        删除岗位，同时删除岗位相关的面试和面试问题
        '''
        res = await self.position_service.delete(position_id)
        if res:
            interview_ids = await self.interview_service.get_interview_ids_by_position_id(position_id)
            res = await self.interview_service.delete_by_position_id(position_id)
            if res:
                return True
            await self.interview_question_service.delete_by_interview_ids(interview_ids)
            return True
        return False
    
    async def get_candidates(self):
        candidates = await self.candidate_service.list_all()
        candidate_list = []
        for candidate in candidates:
            can = candidate.to_dict()
            can['position_id'] = candidate.position_id.split(',')
            candidate_list.append(can)
        return candidate_list
    
    async def create_candidate(self, candidate: Candidate):
        return await self.candidate_service.create(candidate)
    
    async def update_candidate(self, candidate: Candidate):
        candidate_id = candidate.id
        candidate_info = await self.candidate_service.get(candidate_id)
        if not candidate_info:
            raise HTTPException(status_code=404, detail="Candidate not found")
        position_ids = candidate.position_id.split(",")
        position_list = await self.position_service.list_by_ids(position_ids)
        if not position_list:
            raise HTTPException(status_code=404, detail="Position not found")
        candidate_info.position_id = ",".join(position.id for position in position_list)
        candidate_info.email = candidate.email
        candidate_info.resume_type = candidate.resume_type
        candidate_info.resume_content = candidate.resume_content
        return await self.candidate_service.update(candidate_info)
    
    async def delete_candidate(self, candidate_id: int):
        '''
        删除候选人，同时删除候选人相关的面试和面试问题
        '''
        res = await self.candidate_service.delete(candidate_id)
        if res:
            interview_ids = await self.interview_service.get_interview_ids_by_candidate_id(candidate_id)
            res = await self.interview_service.delete_by_candidate_id(candidate_id)
            if res:
                return True
            await self.interview_question_service.delete_by_interview_ids(interview_ids)
            return True
        return False
    
    async def get_resume(self, candidate_id: int) -> Optional[Candidate]:
        """下载候选人简历"""
        candidate = await self.candidate_service.get_resume(candidate_id)
        if not candidate:
            return None
        return candidate
    
    async def get_interviews(self):
        """获取所有面试列表"""
        return await self.interview_service.list_all()

    async def create_interview(self, interview: Interview):
        """创建新面试"""
        interview.status = 0
        interview.token = str(uuid.uuid4())
        # 设置结束时间为开始时间后3天
        if interview.start_time:
            interview.end_time = interview.start_time + (3 * 24 * 60 * 60)  # 3天的秒数
        return await self.interview_service.create(interview)
    
    async def update_interview(self, interview: Interview):
        """更新面试信息"""
        return await self.interview_service.update(interview)
    
    async def delete_interview(self, interview_id: int):
        """删除面试"""
        return await self.interview_service.delete(interview_id)
    
    async def get_interview_report(self, interview_id: int):
        """获取面试报告"""
        return await self.interview_service.get_report(interview_id)
    
    def _run_in_new_event_loop(self, coro):
        """在新的事件循环中运行协程"""
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(coro)
            finally:
                loop.close()
        
        thread = threading.Thread(target=run)
        thread.start()

    async def generate_interview_questions(self, interview_id: int, question_count: int = 10, with_example_answer: bool = False, append: bool = False) -> bool:
        """生成面试题"""
        interview = await self.interview_service.get_by_id(interview_id)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        if interview.status == 1:
            raise HTTPException(status_code=400, detail="试题准备中，请勿重复生成")
        candidate = await self.candidate_service.get_by_id(interview.candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        position = await self.position_service.get_by_id(interview.position_id)
        if not position:
            raise HTTPException(status_code=404, detail="Position not found")
        interview.status = 1
        interview.question_count = question_count if not append else (interview.question_count if interview.question_count else 0) + question_count
        await self.interview_service.update(interview)

        if not append:
            await self.interview_question_service.delete_by_interview_id(interview_id)
        
        # 在新的事件循环中运行面试题生成任务
        self._run_in_new_event_loop(
            self.generate_interview_questions_by_llm(interview, candidate, position, question_count, with_example_answer)
        )
        return True
    
    async def generate_interview_questions_by_llm(self, interview: Interview, candidate: Candidate, position: Position, question_count: int = 10, with_example_answer: bool = False) -> bool:
        '''
        使用大模型生成面试题
        '''
        generate_interview_questions_service = GenerateInterviewQuestionsService()
        questions = await generate_interview_questions_service.generate_questions(candidate.resume_content, candidate.resume_type, position.name, position.requirements, position.responsibilities, question_count)

        # 将问题保存到数据库
        interview_questions = []
        for question in questions:
            interview_question = InterviewQuestion(
                interview_id=interview.id,
                question=question['question'],
                score_standard=question['score_standard']
            )   
            if with_example_answer:
                interview_question.example_answer = await self.get_example_answer_by_llm(interview_question)
            interview_questions.append(interview_question)
        
        # 在新线程中创建新的数据库连接
        interview_question_service = InterviewQuestionService(use_singleton=False)
        await interview_question_service.batch_create(interview_questions)
        
        interview.status = 2
        await self.interview_service.update(interview)
        return True
    
    async def get_interview_info(self, interview_token: str):
        """获取面试信息"""
        interview = await self.interview_service.get_by_token(interview_token)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        interview_info = interview.to_dict()
        interview_info['voice_reading'] = interview.voice_reading
        interview_info['time'] = datetime.fromtimestamp(interview.start_time).strftime("%Y-%m-%d %H:%M:%S")
        position = await self.position_service.get_by_id(interview.position_id)
        interview_info['position'] = position.name
        candidate = await self.candidate_service.get_by_id(interview.candidate_id)
        interview_info['candidate'] = candidate.name
        return interview_info
    
    async def get_question(self, interview_token: str, page: int = 1, page_size: int = 10):
        """获取面试问题
        
        Args:
            interview_token: 面试令牌
            page: 页码，从1开始
            page_size: 每页问题数量，默认10个
        """
        interview = await self.check_token(interview_token)
        if interview.status < 2:
            raise HTTPException(status_code=400, detail="试题未生成，请先生成试题")
        questions = await self.interview_question_service.list_by_interview_id(interview.id, page, page_size)
        return [question.to_dict() for question in questions]
    
    async def check_token(self, interview_token: str) -> Optional[Interview]:
        """检查token是否有效"""
        interview = await self.interview_service.get_by_token(interview_token)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        return interview
    
    async def submit_answer(self, interview_token: str, question_id: int, audio_answer: UploadFile = None, text_answer: str = None):
        """提交面试答案"""
        interview = await self.check_token(interview_token)
        if interview.status < 2:
            raise HTTPException(status_code=400, detail="试题未生成，请先生成试题")
        
        interview_question = await self.interview_question_service.get_by_id(question_id)
        if not interview_question:
            raise HTTPException(status_code=404, detail="问题不存在")
        
        text_answer_content = None
        
        if text_answer:
            # 直接使用文本答案
            text_answer_content = text_answer
        elif audio_answer:
            # 读取音频数据
            audio_data = await audio_answer.read()
            interview_question.answer_audio = audio_data
            
            # 创建临时文件保存音频
            temp_file_path = os.path.join(STORAGE['temp'], f"{interview_question.id}.wav")
            os.makedirs(STORAGE['temp'], exist_ok=True)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
                logger.info(f"写入临时文件路径: {temp_file_path}")
            
            try:
                # 首先尝试使用 Vosk 进行识别
                text_answer_content = self.vosk_utils.transcribe(temp_file_path)
                
                # 如果 Vosk 识别失败，尝试使用 Whisper
                if text_answer_content is None:
                    logger.info("Vosk 识别失败，尝试使用 Whisper...")
                    text_answer_content = self.whisper_utils.transcribe(temp_file_path)
                
                if text_answer_content is None:
                    raise HTTPException(status_code=500, detail="音频转录失败，请重试")
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    logger.info(f"清理临时文件: {temp_file_path}")
                    os.unlink(temp_file_path)
        else:
            raise HTTPException(status_code=400, detail="未提供答案")
        
        # 保存答案
        interview_question.answer_text = text_answer_content
        interview_question.answer_time = int(time.time())
        await self.interview_question_service.update(interview_question)
    
    async def toggle_voice_reading(self, interview_token: str, enabled: int):
        """切换语音朗读状态"""
        interview = await self.check_token(interview_token)
        interview.voice_reading = enabled
        await self.interview_service.update_voice_reading(interview)
        return True

    async def get_example_answer(self, interview_token: str, question_id: int):
        """获取示例答案"""
        interview = await self.check_token(interview_token)
        question = await self.interview_question_service.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        if question.example_answer:
            return question.example_answer
        response = await self.get_example_answer_by_llm(question)
        await self.interview_question_service.update_example_answer(question.id, response)
        return response
    
    async def get_example_answer_by_llm(self, question: InterviewQuestion) -> str:
        '''
        使用大模型生成示例答案
        '''
        prompt = f"""
        请根据以下问题和评分标准，生成一个高分示例答案：
        问题：{question.question}
        评分标准：{question.score_standard}
        """
        return self.llm.chat(
            messages=[
                {"role": "system", "content": "请根据以下问题和评分标准，生成一个高分示例答案"},
                {"role": "user", "content": prompt}],
            stream=False
        )
