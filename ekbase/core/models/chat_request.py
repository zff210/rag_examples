class ChatRequest:
    """聊天请求模型类"""
    
    # 用户输入的查询内容
    query: str
    
    # 会话ID,用于关联历史对话
    session_id: str
    
    # 是否启用联网搜索功能
    web_search: bool
    
    # 是否启用Agent模式
    agent_mode: bool
    
    # 入参为json，从json中解析并初始化
    def __init__(self, json_data: dict):
        self.query = json_data.get("query")
        self.session_id = json_data.get("session_id")
        self.web_search = json_data.get("web_search")
        self.agent_mode = json_data.get("agent_mode")
        
