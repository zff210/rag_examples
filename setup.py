from setuptools import setup, find_packages

setup(
    name="rag_examples",
    version="1.0.0",
    description="通用工具包，提供文件处理、日志处理和时间处理等功能",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "sqlalchemy>=1.4.0",
        "python-docx>=0.8.11",
        "PyPDF2>=3.0.0",
        "pandas>=2.0.0",
        "markdown>=3.4.0",
        "beautifulsoup4>=4.12.0",
        "python-dateutil>=2.8.2",
        "tqdm>=4.65.0",
        "uvicorn>=0.25.0",
        "numpy>=1.24.0,<2.0.0",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.0",
        "torch>=2.0.0",
        "openai>=1.0",
        "anthropic>=0.35.0",
        "python-multipart>=0.0.10",
        "fastmcp>=2.2.5",
        "openai-whisper>=1.0.0",
        "psutil>=6.0.0",
        "vosk>=0.3.4"
    ],
    python_requires=">=3.8",
    # 支持本地开发
    package_data={
        "rag_examples": ["*"],  # 包含所有文件，具体排除规则在 MANIFEST.in 中定义
    },
    include_package_data=True,
    # 开发依赖
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 