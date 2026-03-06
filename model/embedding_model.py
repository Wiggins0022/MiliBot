from model.base_model import BaseModel
from utils.config_handler import load_model_config
from langchain_community.embeddings import DashScopeEmbeddings
import os
from utils.config_handler import load_model_config


class EmbeddingModel(BaseModel):
    def __init__(self,model_name):
        super().__init__(model_name)


    def generator(self):
        """
        创建模型实例
        :return: 嵌入模型
        """
        return DashScopeEmbeddings(
            model=self.model_name,
            dashscope_api_key=os.getenv("ALIYUN_API_KEY")
        )

model_config = load_model_config()
embedding_model = EmbeddingModel(model_config['embedding_model_name']).generator()