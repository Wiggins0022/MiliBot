import os
from utils.config_handler import load_model_config
from model.base_model import BaseModel
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv

load_dotenv()

class ChatModel(BaseModel):
    def __init__(self):
        self.model_config = load_model_config()

    def generator(self):
        """
        创建模型实例
        :return:
        """
        return ChatTongyi(
            model=self.model_config['chat_model_name'],
            api_key=os.getenv("ALIYUN_API_KEY"),
        )

chat_model = ChatModel().generator()