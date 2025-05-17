"""
时间处理工具模块

提供常用的时间处理函数
"""

from datetime import datetime
import time

def format_time(timestamp=None, format_str="%Y-%m-%d %H:%M:%S"):
    """
    格式化时间戳为指定格式的字符串
    
    Args:
        timestamp (float, optional): 时间戳。如果为None，使用当前时间
        format_str (str, optional): 时间格式字符串，默认为"%Y-%m-%d %H:%M:%S"
    
    Returns:
        str: 格式化后的时间字符串
    """
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime(format_str)

def get_current_time(format_str="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间的格式化字符串
    
    Args:
        format_str (str, optional): 时间格式字符串，默认为"%Y-%m-%d %H:%M:%S"
    
    Returns:
        str: 当前时间的格式化字符串
    """
    return datetime.now().strftime(format_str)

def time_str_to_timestamp(time_str, format_str="%Y-%m-%d %H:%M:%S"):
    """
    将时间字符串转换为时间戳
    
    Args:
        time_str (str): 时间字符串
        format_str (str, optional): 时间格式字符串，默认为"%Y-%m-%d %H:%M:%S"
    
    Returns:
        float: 时间戳
    """
    dt = datetime.strptime(time_str, format_str)
    return time.mktime(dt.timetuple())
