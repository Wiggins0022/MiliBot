from utils.logger_handler import LoggerHandler
import os
from utils.config_handler import load_prompt_config
from utils.path_tool import get_abs_path

logger = LoggerHandler().get_logger()

def load_main_prompt() -> str:
    """
    加载主提示词
    :return: 主提示词内容字符串，如果加载失败返回空字符串
    """
    # 加载配置文件
    prompt_config = load_prompt_config()
    # 获取主提示词路径
    path = get_abs_path(prompt_config['main_agent_prompt_path'])

    if not os.path.exists(path):
        logger.error(f"【load_main_prompt】加载主提示词失败，文件不存在: {path}")
        return ""

    if os.path.isdir(path):
        logger.error(f"【load_main_prompt】加载主提示词失败，路径是一个目录: {path}")
        return ""

    try:
        with open(path,'r',encoding='utf-8') as f:
            main_prompt = f.read()
            logger.info(f"【load_main_prompt】成功加载主提示词: {path}")
            return main_prompt
    except Exception as e:
        logger.error(f"【load_main_prompt】加载主提示词失败，发生异常: {e}")
        return ""

def load_person_info() -> str:
    """
    加载群聊成员信息提示词
    :return:
    """
    # 加载配置文件
    prompt_config = load_prompt_config()
    # 获取主提示词路径
    path = get_abs_path(prompt_config['person_info_prompt_path'])

    if not os.path.exists(path):
        logger.error(f"【load_person_info】加载群成员信息失败，文件不存在: {path}")
        return ""

    if os.path.isdir(path):
        logger.error(f"【load_person_info】加载群成员信息失败，路径是一个目录: {path}")
        return ""

    try:
        with open(path, 'r', encoding='utf-8') as f:
            main_prompt = f.read()
            logger.info(f"【load_person_info】成功加载群成员信息: {path}")
            return main_prompt
    except Exception as e:
        logger.error(f"【load_person_info】加载群成员信息失败，发生异常: {e}")
        return ""

def load_rag_prompt() -> str:
    """
    加载RAG提示词
    :return: RAG提示词内容字符串，如果加载失败返回空字符串
    """
    # 加载配置文件
    prompt_config = load_prompt_config()
    # 获取RAG提示词路径
    path = get_abs_path(prompt_config['rag_prompt_path'])

    if not os.path.exists(path):
        logger.error(f"【load_rag_prompt】加载RAG提示词失败，文件不存在: {path}")
        return ""

    if os.path.isdir(path):
        logger.error(f"【load_rag_prompt】加载RAG提示词失败，路径是一个目录: {path}")
        return ""

    try:
        with open(path,'r',encoding='utf-8') as f:
            rag_prompt = f.read()
            logger.info(f"【load_rag_prompt】成功加载RAG提示词: {path}")
            return rag_prompt
    except Exception as e:
        logger.error(f"【load_rag_prompt】加载RAG提示词失败，发生异常: {e}")
        return ""

def load_report_prompt() -> str:
    """
    加载报告生成提示词
    :return: 报告生成提示词内容字符串，如果加载失败返回空字符串
    """
    # 加载配置文件
    prompt_config = load_prompt_config()
    # 获取报告生成提示词路径
    path = get_abs_path(prompt_config['report_prompt_path'])

    if not os.path.exists(path):
        logger.error(f"【load_report_prompt】加载报告生成提示词失败，文件不存在: {path}")
        return ""

    if os.path.isdir(path):
        logger.error(f"【load_report_prompt】加载报告生成提示词失败，路径是一个目录: {path}")
        return ""

    try:
        with open(path,'r',encoding='utf-8') as f:
            report_prompt = f.read()
            logger.info(f"【load_report_prompt】成功加载报告生成提示词: {path}")
            return report_prompt
    except Exception as e:
        logger.error(f"【load_report_prompt】加载报告生成提示词失败，发生异常: {e}")
        return ""