"""
通用工具函数包

这个包提供了项目中常用的工具函数，包括：
- 文件处理工具 (file_utils)
- 日志工具 (logger)
- 时间处理工具 (time_utils)
- 向量处理工具 (vector_utils)
"""

# 文件处理工具
from .file_utils import (
    clean_text,
    load_text_file,
    load_docx_file,
    load_pdf_file,
    load_markdown_file,
    load_excel_file,
    load_documents_from_directory,
    get_default_documents,
    create_example_files
)

# 日志工具
from .logger import (
    setup_logger,
    get_logger
)

# 时间处理工具
from .time_utils import (
    format_time,
    get_current_time,
    time_str_to_timestamp
)

# 向量处理工具
from .vector_utils import VectorUtils

__all__ = [
    # 文件处理工具
    'clean_text',
    'load_text_file',
    'load_docx_file',
    'load_pdf_file',
    'load_markdown_file',
    'load_excel_file',
    'load_documents_from_directory',
    'get_default_documents',
    'create_example_files',
    
    # 日志工具
    'setup_logger',
    'get_logger',
    
    # 时间处理工具
    'format_time',
    'get_current_time',
    'time_str_to_timestamp',
    
    # 向量处理工具
    'VectorUtils'
]
