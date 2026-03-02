from model.base_model import BaseModel
from utils.config_handler import load_model_config
from langchain_community.embeddings import DashScopeEmbeddings
import os


class EmbeddingModel(BaseModel):
    def __init__(self):
        self.model_config = load_model_config()

    def generator(self):
        """
        创建模型实例
        :return: 嵌入模型
        """
        return DashScopeEmbeddings(
            model=self.model_config['embedding_model_name'],
            dashscope_api_key=os.getenv("ALIYUN_API_KEY")
        )

embedding_model = EmbeddingModel().generator()