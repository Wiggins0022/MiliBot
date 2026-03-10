from utils.config_handler import load_model_config
from model.model_factory import ModelFactory

model_config = load_model_config()

# 获取模型名称
model_name = model_config.get('chat_model_name', model_config['default_chat_model_name'])

if model_name is None:
    raise ValueError("模型名称未在配置文件中指定，请检查模型配置。")

model_wrapper = ModelFactory.create_model(model_name)

# 创建模型实例
chat_model = model_wrapper.generator()