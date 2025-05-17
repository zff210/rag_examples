"""
日志工具测试
"""

import os
import logging
import pytest
from common.utils import setup_logger, get_logger

@pytest.fixture
def log_file(tmp_path):
    """创建测试日志文件"""
    log_file = tmp_path / "test.log"
    return str(log_file)

def test_setup_logger(log_file):
    """测试日志配置"""
    # 配置日志
    logger = setup_logger(
        name="test_logger",
        log_file=log_file,
        level=logging.DEBUG
    )
    
    # 记录测试日志
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    
    # 验证日志文件
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "调试信息" in content
        assert "普通信息" in content
        assert "警告信息" in content
        assert "错误信息" in content

def test_get_logger():
    """测试获取日志记录器"""
    # 获取日志记录器
    logger1 = get_logger("test_logger")
    logger2 = get_logger("test_logger")
    
    # 验证是否为同一个实例
    assert logger1 is logger2
    
    # 验证日志级别
    assert logger1.level == logging.WARNING  # 默认级别 