"""
时间处理工具测试
"""

import time
from datetime import datetime
import pytest
from common.utils import (
    format_time,
    get_current_time,
    time_str_to_timestamp
)

def test_format_time():
    """测试时间戳格式化"""
    # 测试当前时间
    current_time = time.time()
    formatted = format_time(current_time)
    
    # 验证格式
    assert isinstance(formatted, str)
    assert len(formatted) == 19  # YYYY-MM-DD HH:MM:SS
    
    # 测试自定义格式
    custom_format = "%Y/%m/%d"
    formatted = format_time(current_time, custom_format)
    assert len(formatted) == 10  # YYYY/MM/DD

def test_get_current_time():
    """测试获取当前时间"""
    # 获取当前时间
    current_time = get_current_time()
    
    # 验证格式
    assert isinstance(current_time, str)
    assert len(current_time) == 19  # YYYY-MM-DD HH:MM:SS
    
    # 验证时间格式
    try:
        datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        assert True
    except ValueError:
        assert False, "时间格式不正确"

def test_time_str_to_timestamp():
    """测试时间字符串转时间戳"""
    # 测试标准格式
    time_str = "2024-03-21 12:00:00"
    timestamp = time_str_to_timestamp(time_str)
    
    # 验证结果
    assert isinstance(timestamp, float)
    assert timestamp > 0
    
    # 测试自定义格式
    time_str = "2024/03/21"
    timestamp = time_str_to_timestamp(time_str, "%Y/%m/%d")
    assert isinstance(timestamp, float)
    assert timestamp > 0 