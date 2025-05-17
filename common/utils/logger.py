"""
日志工具模块

提供统一的日志配置和获取函数
"""

import logging
import os
from datetime import datetime

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    设置并返回一个配置好的logger
    
    Args:
        name (str): logger的名称
        log_file (str, optional): 日志文件路径。如果为None，则只输出到控制台
        level (int, optional): 日志级别，默认为INFO
    
    Returns:
        logging.Logger: 配置好的logger实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 如果logger已经有处理器，直接返回
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name):
    """
    获取一个logger实例
    
    Args:
        name (str): logger的名称
    
    Returns:
        logging.Logger: logger实例
    """
    return logging.getLogger(name)
