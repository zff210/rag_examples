"""
文件处理工具测试
"""

import os
import pytest
from common.utils import (
    load_documents_from_directory,
    create_example_files,
    get_default_documents
)

@pytest.fixture
def test_dir(tmp_path):
    """创建测试目录"""
    test_dir = tmp_path / "test_docs"
    test_dir.mkdir()
    return test_dir

def test_create_example_files(test_dir):
    """测试创建示例文件"""
    # 创建示例文件
    create_example_files(str(test_dir))
    
    # 验证文件是否创建
    assert os.path.exists(test_dir / "example.txt")
    with open(test_dir / "example.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "界面新闻" in content

def test_load_documents_from_directory(test_dir):
    """测试文档加载"""
    # 创建测试文件
    test_file = test_dir / "test.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("测试文档内容")
    
    # 加载文档
    documents, sources, errors = load_documents_from_directory(
        directory_path=str(test_dir),
        file_types=['.txt']
    )
    
    # 验证结果
    assert len(documents) == 1
    assert len(sources) == 1
    assert len(errors) == 0
    assert "测试文档内容" in documents[0]
    assert str(test_file) in sources[0]

def test_get_default_documents():
    """测试获取默认文档"""
    documents, sources = get_default_documents()
    
    # 验证结果
    assert len(documents) == 3
    assert len(sources) == 3
    assert "界面新闻" in documents[0]
    assert "企业价值观" in documents[1]
    assert "创始人" in documents[2] 