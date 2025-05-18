class BaseCustomException(Exception):
    """基础自定义异常类"""
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class VectorOperationException(BaseCustomException):
    """向量操作相关异常"""
    pass

class FileOperationException(BaseCustomException):
    """文件操作相关异常"""
    pass

class ModelOperationException(BaseCustomException):
    """模型操作相关异常"""
    pass

class IndexOperationException(BaseCustomException):
    """索引操作相关异常"""
    pass 