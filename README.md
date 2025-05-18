# RAG Examples

一个基于 RAG (Retrieval-Augmented Generation) 技术的智能问答系统示例项目。

## 功能特点

- 📚 文档管理：支持 PDF、TXT 等格式文档的上传和管理
- 🔍 智能检索：基于向量数据库的语义检索
- 💬 智能对话：支持上下文理解和多轮对话
- 🎯 精确回答：基于文档内容的准确回答
- 🔄 实时更新：支持文档索引的实时更新
- 🌐 网络搜索：支持联网搜索补充信息
- 🤖 Agent 模式：支持工具调用和任务规划
- 🔊 语音交互：支持语音输入和语音合成

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- LangChain
- ChromaDB
- SQLAlchemy
- PyPDF2

### 前端
- Vue 3
- TailwindCSS
- Vite
- TypeScript

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 8+

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/rag_examples.git
cd rag_examples
```

2. 安装后端依赖
```bash
1. 创建虚拟环境<br> 
    ``` python -m venv .venv ```
2. 激活环境<br> 
    ``` source .venv/bin/activate ```
4. 安装必要的依赖<br> 
    ``` cd .. && pip install -e ".[dev]" ```
```

3. 安装前端依赖
```bash
cd web
npm install
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的环境变量
```

5. 启动服务
```bash
# 启动后端服务
python main.py

# 启动前端服务
cd web
npm run dev
```

## 使用指南

1. 文档管理
   - 上传文档：支持 PDF、TXT 格式
   - 管理文档：查看、删除、重置索引
   - 批量操作：支持批量上传和管理

2. 对话功能
   - 新建对话：开始新的对话会话
   - 历史记录：查看和管理历史对话
   - 导出对话：支持导出对话记录
   - 语音交互：支持语音输入和输出

3. MCP 服务器管理
   - 添加服务器：配置 MCP 服务器信息
   - 管理工具：查看和刷新服务器工具
   - 认证配置：支持多种认证方式

## 开发指南

### 项目结构
```
rag_examples/
├── api/            # API 接口定义
├── core/           # 核心功能实现
├── models/         # 数据模型
├── services/       # 业务逻辑
├── utils/          # 工具函数
├── web/            # 前端代码
└── tests/          # 测试用例
```

### 开发规范
- 遵循 PEP 8 Python 代码规范
- 使用 TypeScript 进行前端开发
- 提交代码前进行代码格式化
- 编写必要的单元测试

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目维护者：[Your Name]
- 邮箱：[your.email@example.com]
- 项目链接：[https://github.com/yourusername/rag_examples]

#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
