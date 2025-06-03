class PromptProcessModel:

    # 当前的prompt
    prompt: str

    # 是否结束; true：已经结束，拿到结果；false：未结束，需要根据prompt继续请求大模型获取最终结果
    is_end: bool

    # 最终结果
    final_result: str

    def __init__(self, json_data: dict):
        self.prompt = json_data.get("prompt")
        self.is_end = json_data.get("is_end")
        self.final_result = json_data.get("final_result")
