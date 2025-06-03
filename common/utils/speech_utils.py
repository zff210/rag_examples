import os
import json
import wave
import logging
from typing import Optional
from vosk import Model, KaldiRecognizer

logger = logging.getLogger(__name__)

class SpeechUtils:
    def __init__(self, model_path: str):
        """
        初始化语音转文字工具类
        
        Args:
            model_path: Vosk 模型路径
        """
        self.model_path = model_path
        self._model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """加载 Vosk 模型"""
        try:
            if not os.path.exists(self.model_path):
                raise RuntimeError(f"模型路径不存在: {self.model_path}")
            
            logger.info("开始加载 Vosk 模型...")
            self._model = Model(self.model_path)
            logger.info("Vosk 模型加载完成")
        except Exception as e:
            logger.error(f"Vosk 模型加载失败: {str(e)}")
    
    def transcribe(self, audio_file_path: str) -> Optional[str]:
        """
        将音频文件转换为文字
        
        Args:
            audio_file_path: 音频文件路径
            
        Returns:
            str: 转换后的文字，如果转换失败则返回 None
        """
        try:
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
            
            # 打开音频文件
            wf = wave.open(audio_file_path, "rb")
            
            # 检查音频格式
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                raise RuntimeError("音频格式错误，需要单声道 16bit PCM 格式")
            
            # 创建识别器
            rec = KaldiRecognizer(self._model, wf.getframerate())
            rec.SetWords(True)  # 启用词级别时间戳
            
            logger.info("开始转录音频...")
            text_parts = []
            
            # 分块读取音频进行识别
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get("text"):
                        text_parts.append(result["text"])
            
            # 处理最后一块数据
            final_result = json.loads(rec.FinalResult())
            if final_result.get("text"):
                text_parts.append(final_result["text"])
            
            # 合并所有文本
            text = " ".join(text_parts)
            logger.info("音频转录完成")
            
            return text if text.strip() else None
            
        except Exception as e:
            logger.error(f"音频转录失败: {str(e)}")
            return None
        finally:
            if 'wf' in locals():
                wf.close() 