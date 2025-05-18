from common.utils.llm_utils import LLMUtils

# 初始化配置
config = {
    'model_name': 'doubao-1-5-thinking-pro-250415',  # 豆包模型名称
    'api_key': '470b532c-0a5d-4713-92f1-e3eb2d3dafee',  # 豆包API密钥
    'base_url': 'https://ark.cn-beijing.volces.com/api/v3',  # 豆包API地址
    'temperature': 0.7,
    'max_length': 2048,
    'top_p': 0.9
}

# 创建LLMUtils实例
llm_utils = LLMUtils(config)

# 示例1：普通对话
messages = [
    {"role": "system", "content": "你是人工智能助手"},
    {"role": "user", "content": "你好，请介绍一下你自己"}
]

# 方式1：使用默认模型
# response = llm_utils.chat(messages)
# print("普通对话响应：", response)

# # 方式2：指定模型名称
# response = llm_utils.chat(messages, model_name='doubao-1-5-thinking-pro-250415')
# print("指定模型响应：", response)

# 示例2：流式对话
print("\n流式对话响应：")
for chunk in llm_utils.chat(messages, stream=True):
    print(chunk, end="")

# 示例3：文本生成
prompt = "请用中文写一首关于春天的诗"
response = llm_utils.generate_text(prompt)
print("\n\n生成的诗歌：", response)

# 示例4：获取文本嵌入
# text = "这是一个测试文本"
# embeddings = llm_utils.get_embeddings(text)
# print("\n文本嵌入维度：", len(embeddings))

# # 示例5：更新配置
# llm_utils.update_config(temperature=0.8)
# response = llm_utils.chat(messages)
# print("\n更新温度后的响应：", response)