from utils.path_tool import get_abs_path
import yaml

def load_prompt_config(config_path: str = get_abs_path('resources/prompts.yml'), encoding: str = 'utf-8') -> dict:
    """
    加载提示词配置文件
    :param config_path: 配置文件路径，默认为'./resources/prompts.yml'
    :param encoding: 配置文件编码，默认为'utf-8'
    :return: 返回加载的提示词配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.safe_load(f)
    return config

def load_model_config(config_path: str = get_abs_path('resources/model.yaml'), encoding: str = 'utf-8') -> dict:
    """
    加载模型配置文件
    :param config_path: 配置文件路径，默认为'./resources/model.yml'
    :param encoding: 配置文件编码，默认为'utf-8'
    :return: 返回加载的模型配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.safe_load(f)
    return config

def load_chroma_config(config_path: str = get_abs_path('resources/chroma.yml'), encoding: str = 'utf-8') -> dict:
    """
    加载chroma配置文件
    :param config_path: 配置文件路径，默认为'./resources/chroma.yml'
    :param encoding: 配置文件编码，默认为'utf-8'
    :return: 返回加载的chroma配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.safe_load(f)
    return config

def load_tools_config(config_path: str = get_abs_path('resources/tools.yml'), encoding: str = 'utf-8') -> dict:
    """
    加载工具配置文件
    :param config_path: 配置文件路径，默认为'./resources/tools.yml'
    :param encoding: 配置文件编码，默认为'utf-8'
    :return: 返回加载的工具配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.safe_load(f)
    return config