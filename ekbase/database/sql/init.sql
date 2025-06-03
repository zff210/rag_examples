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

-- 创建mcp服务器表，用于存储mcp服务器信息
CREATE TABLE IF NOT EXISTS mcp_servers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,                     -- 服务器名称
        url TEXT NOT NULL,                      -- 服务器URL
        description TEXT,                       -- 服务器描述
        auth_type TEXT,                         -- 认证类型
        auth_value TEXT,                        -- 认证值
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- 创建mcp服务器工具表，用于存储mcp服务器工具信息
CREATE TABLE IF NOT EXISTS mcp_tools (
        id TEXT PRIMARY KEY,
        server_id TEXT NOT NULL,                 -- 服务器ID
        name TEXT NOT NULL,                     -- 工具名称
        description TEXT,                       -- 工具描述
        input_schema TEXT,                      -- 工具输入参数
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- 创建岗位表，用于存储岗位信息
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 岗位ID，唯一标识
    name TEXT NOT NULL, -- 岗位名称
    requirements TEXT, -- 岗位要求
    responsibilities TEXT, -- 岗位职责
    quantity INTEGER, -- 需求人数
    status INTEGER, -- 招聘状态：0=未启动，1=进行中，2=已完成
    created_at INTEGER DEFAULT (strftime('%s', 'now')), -- 岗位发布时间，Unix时间戳
    recruiter TEXT -- 招聘负责人
);

-- 创建候选人表，用于存储候选人信息
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 候选人ID，唯一标识
    position_id TEXT NOT NULL, -- 申请的岗位ID列表
    name TEXT NOT NULL, -- 候选人姓名
    email TEXT, -- 候选人邮件
    resume_type INTEGER, -- 简历类型：0=PDF，1=Word
    resume_content BLOB -- 简历文件二进制内容
);

-- 创建面试表，用于存储面试信息
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 面试ID，唯一标识
    candidate_id INTEGER NOT NULL, -- 候选人ID
    position_id INTEGER NOT NULL, -- 岗位ID
    interviewer TEXT, -- 面试官
    start_time INTEGER, -- 面试开始时间，Unix时间戳
    end_time INTEGER, -- 面试结束时间，Unix时间戳
    status INTEGER, -- 面试状态：0=未开始，1=试题已备好 2 =面试进行中  3 =面试完毕 4 =面试报告已生成
    question_count INTEGER, -- 面试问题数量
    is_passed INTEGER, -- 面试结果：0=未通过，1=通过
    voice_reading INTEGER, -- 是否开启语音朗读：0=关闭，1=开启
    report_content BLOB, -- 面试报告二进制内容
    token TEXT -- 面试链接验证令牌
);

-- 创建面试问题表，用于存储面试问题信息
CREATE TABLE IF NOT EXISTS interview_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 问题ID，唯一标识
    interview_id INTEGER NOT NULL, -- 面试ID
    question TEXT NOT NULL, -- 面试问题内容
    score_standard TEXT, -- 评分标准或分值说明
    answer_audio BLOB, -- 回答录音二进制内容
    answer_text TEXT, -- 回答文本内容
    created_at INTEGER DEFAULT (strftime('%s', 'now')), -- 问题创建时间，Unix时间戳
    answered_at INTEGER, -- 回答时间，Unix时间戳
    example_answer TEXT -- 示例答案
);