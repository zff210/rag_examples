# 通用工具包使用说明

本工具包提供了一系列常用的工具函数，包括文件处理、日志处理和时间处理等功能。

## 1. 安装依赖

使用前请确保安装以下依赖：

```bash
pip install python-docx PyPDF2 pandas markdown beautifulsoup4
```

## 2. 快速开始

### 2.1 导入工具包

```python
from common.utils import (
    # 文件处理工具
    load_documents_from_directory,
    # 日志工具
    setup_logger,
    # 时间处理工具
    format_time
)
```

## 3. 功能模块说明

### 3.1 文件处理工具 (file_utils)

#### 3.1.1 主要功能
- 支持多种文件格式读取（txt、docx、pdf、markdown、excel）
- 文档批量加载
- 文本清理和格式化

#### 3.1.2 使用示例
```python
# 加载指定目录下的文档
documents, sources, errors = load_documents_from_directory(
    directory_path="path/to/documents",
    file_types=['.txt', '.docx', '.pdf']
)

# 创建示例文件
create_example_files("path/to/output")
```

### 3.2 日志工具 (logger)

#### 3.2.1 主要功能
- 统一的日志配置
- 支持控制台和文件输出
- 自动创建日志目录

#### 3.2.2 使用示例
```python
# 配置日志记录器
logger = setup_logger(
    name="my_app",
    log_file="logs/app.log",
    level=logging.INFO
)

# 使用日志记录器
logger.info("这是一条信息日志")
logger.error("这是一条错误日志")
```

### 3.3 时间处理工具 (time_utils)

#### 3.3.1 主要功能
- 时间戳格式化
- 获取当前时间
- 时间字符串转换

#### 3.3.2 使用示例
```python
# 格式化时间戳
formatted_time = format_time(timestamp=1234567890)

# 获取当前时间
current_time = get_current_time()

# 时间字符串转时间戳
timestamp = time_str_to_timestamp("2023-01-01 12:00:00")
```

## 4. 完整示例

```python
from common.utils import (
    load_documents_from_directory,
    setup_logger,
    format_time,
    get_current_time
)

# 配置日志
logger = setup_logger("my_app", "logs/app.log")

try:
    # 加载文档
    logger.info("开始加载文档...")
    documents, sources, errors = load_documents_from_directory("docs")
    
    # 记录处理时间
    current_time = get_current_time()
    logger.info(f"文档加载完成，时间：{current_time}")
    
    # 处理文档
    for doc, source in zip(documents, sources):
        logger.info(f"处理文档：{source}")
        # 处理逻辑...
        
except Exception as e:
    logger.error(f"处理失败：{str(e)}")
```

## 5. 注意事项

### 5.1 文件处理
- 处理大文件时注意内存使用
- 确保有足够的磁盘空间
- 检查文件权限

### 5.2 日志处理
- 日志文件会随时间增长，需要定期清理
- 生产环境建议使用日志轮转
- 注意日志级别设置

### 5.3 时间处理
- 注意时区问题
- 时间格式字符串要符合标准格式
- 处理时间戳时注意精度

## 6. 常见问题

### 6.1 文件读取失败
- 检查文件路径是否正确
- 确认文件权限
- 验证文件格式是否支持

### 6.2 日志不输出
- 检查日志级别设置
- 确认日志目录权限
- 验证日志配置是否正确

### 6.3 时间转换错误
- 检查时间格式字符串
- 确认时间字符串格式正确
- 注意时区差异

## 7. 更新日志

### v1.0.0 (2024-03-21)
- 初始版本发布
- 包含文件处理、日志处理和时间处理功能

## 8. 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个工具包。

## 9. 许可证

MIT License 