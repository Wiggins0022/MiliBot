from typing import Callable
from langchain.agents.middleware import wrap_tool_call, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command
from utils.logger_handler import logger
from utils.load_prompts import load_main_prompt
from utils.load_prompts import load_report_prompt



@wrap_tool_call
def monitor_tool(request: ToolCallRequest,
                 handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command:
    logger.info(f"【monitor_tool】工具调用监控: {request.tool_call['name']}")

    # 如果模型调用了触发报告的空工具，就在上下文中打上标记
    if request.tool_call['name'] == "report_tool":
        request.runtime.context['is_report_mode'] = True
        logger.info("已在运行时上下文中注入 is_report_mode = True")

    return handler(request)


@dynamic_prompt
def report_prompt_switch(request: ModelRequest):
    """根据上下文动态切换 Prompt"""
    is_report_mode = request.runtime.context.get('is_report_mode', False)

    if is_report_mode:
        logger.info("检测到报告生成标记，已切换至【QQ群聊数据分析师】提示词")
        return load_report_prompt()

    # 默认返回正常的“米粒”群助手提示词
    return load_main_prompt()