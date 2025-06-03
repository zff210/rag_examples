import json
import io
import PyPDF2
import logging
from common.utils.llm_utils import LLMUtils
from ekbase.config.settings import LLM

logger = logging.getLogger(__name__)

class GenerateInterviewQuestionsService:
    def __init__(self):
        self.llm = LLMUtils(LLM)

    # 从PDF二进制数据中提取文本内容
    def extract_text_from_pdf(self, pdf_content):
        try:
            # 如果输入是None或空值，返回空字符串
            if pdf_content is None or pdf_content == b'':
                return "无简历内容"
                
            # 创建BytesIO对象处理二进制数据
            pdf_file = io.BytesIO(pdf_content)
            
            # 创建PDF阅读器
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # 提取所有页面的文本
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            # 如果没有提取到文本，尝试使用另一种方法
            if not text.strip():
                return "无法从PDF中提取文本内容"
                
            return text
        except Exception as e:
            print(f"PDF文本提取错误: {str(e)}")
            # 如果pdf解析失败，尝试作为纯文本处理
            try:
                if isinstance(pdf_content, bytes):
                    return pdf_content.decode('utf-8', errors='ignore')
                return str(pdf_content)
            except:
                return "无法解析简历内容"


     
    # 从Word文档中提取文本内容
    def extract_text_from_word(self, word_content):
        try:
            # 如果输入是None或空值，返回空字符串
            if word_content is None or word_content == b'':
                return "无简历内容"
            
            # 创建BytesIO对象处理二进制数据
            word_file = io.BytesIO(word_content)
            
            # 使用python-docx库打开文档
            from docx import Document
            doc = Document(word_file)
            
            # 提取所有段落的文本
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
                
            # 如果没有提取到文本，尝试使用另一种方法
            if not text.strip():
                return "无法从Word文档中提取文本内容"
                
            return text
        except Exception as e:
            logger.error("Word文档文本提取错误: %s", str(e), exc_info=True)
            # 如果Word解析失败，尝试作为纯文本处理
            try:
                if isinstance(word_content, bytes):
                    return word_content.decode('utf-8', errors='ignore')
                return str(word_content)
            except:
                return "无法解析简历内容"           

    # 根据简历内容和岗位信息生成面试问题
    async def generate_questions(self, resume_content, resume_type, position_name, requirements, responsibilities, question_count):
        # 解析简历内容 : 抽取pdf中resume_content的文本内容
        try:
            #根据简历类型，来提取数据
            if(resume_type=='pdf'):
                resume_text = self.extract_text_from_pdf(resume_content)
            elif(resume_type=='word'):
                resume_text = self.extract_text_from_word(resume_content)
            else:
                resume_text = resume_content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error("解析简历内容时出错: %s", str(e), exc_info=True)
            resume_text = "无法解析简历内容"
        
        logger.debug("resume_text: %s", resume_text)

        # 返回json格式参考
        json_format = [
            {"question": "请介绍一下你的专业背景和技能", "score_standard": "清晰度5分，相关性5分，深度5分"},
            {"question": "你认为自己最适合这个岗位的原因是什么？", "score_standard": "匹配度5分，自我认知5分，表达5分"},
            {"question": "描述一个你解决过的技术挑战", "score_standard": "复杂度5分，解决方案5分，结果5分"},
            {"question": "你如何看待团队合作？", "score_standard": "协作能力5分，沟通能力5分，角色意识5分"},
            {"question": "你对这个行业的未来趋势有什么看法？", "score_standard": "了解程度5分，前瞻性5分，分析能力5分"}
        ]
        # 调用OpenAI API生成面试问题
        try:
            response = self.llm.chat(
                messages=[
                    {"role": "system", "content": "你是一名专业的招聘面试官，请根据岗位要求和候选人简历生成10个针对性的技术面试问题，每个问题附带评分标准,返回标准的json格式。"},
                    {"role": "user", "content": f"岗位名称: {position_name}\n岗位要求: {requirements}\n岗位职责: {responsibilities}\n候选人简历: {resume_text}\n\n请生成{question_count}个面试问题和评分标准，JSON格式参考 {json_format} ，每个问题满分10分。"}
                ],
                response_format={"type": "json_object"},
                stream = False
            )
            
            # 解析响应内容
            if isinstance(response, str):
                questions_json = response
            else:
                questions_json = response.content
            questions = json.loads(questions_json)
            logger.debug("questions: %s", questions)
            
            return questions

        except Exception as e:
            logger.error("生成面试问题时出错: %s", str(e), exc_info=True)
            raise e