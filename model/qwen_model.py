from model.base_model import BaseModel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class QWenModel(BaseModel):
    def __init__(self,model_name):
        super().__init__(model_name)

    def generator(self):
        return ChatOpenAI(
            model=self.model_name,
            api_key=os.getenv("ALIYUN_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            max_tokens=2048
        )