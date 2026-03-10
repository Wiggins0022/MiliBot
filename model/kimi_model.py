import os


from model.base_model import BaseModel
from langchain_openai import ChatOpenAI

class KimiModel(BaseModel):
    def __init__(self, model_name):
        super().__init__(model_name)

    def generator(self):
        return ChatOpenAI(
            model=self.model_name,
            openai_api_key=os.getenv("KIMI_API_KEY"),
            openai_api_base="https://api.moonshot.cn/v1",
            max_retries=3
        )