-- 创建聊天会话表，用于存储聊天会话的基本信息
CREATE TABLE IF NOT EXISTS chat_sessions (
        id TEXT PRIMARY KEY,                    -- 会话唯一标识符
        summary TEXT,                           -- 会话摘要
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 更新时间
    );

-- 创建聊天消息表，用于存储具体的聊天消息内容
CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,                    -- 消息唯一标识符
        session_id TEXT,                        -- 关联的会话ID
        role TEXT,                              -- 消息发送者角色（如：user, assistant等）
        content TEXT,                           -- 消息内容
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 更新时间
    );

-- 创建文档表，用于存储上传的文档信息
CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,                    -- 文档唯一标识符
        file_name TEXT,                         -- 文件名
        file_path TEXT,                         -- 文件路径
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间
    );