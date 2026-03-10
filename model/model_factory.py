from model.base_model import BaseModel
from model.qwen_model import QwenModel
from model.kimi_model import KimiModel
from model.deepseek_model import DeepSeekModel


class ModelFactory:
    @staticmethod
    def create_model(model_name: str) -> BaseModel:
        model_name_lower = model_name.lower()

        # 根据模型名称前缀或关键字来判断使用哪个类
        if "qwen" in model_name_lower:
            return QwenModel(model_name)
        elif "moonshot" in model_name_lower or "kimi" in model_name_lower:
            return KimiModel(model_name)
        elif "deepseek" in model_name_lower:
            return DeepSeekModel(model_name)
        else:
            raise ValueError(f"不支持的模型类型: {model_name}")