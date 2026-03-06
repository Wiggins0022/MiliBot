import os
from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
from rag.rag_service import RAGService
from datetime import datetime
from schema.weather_input import WeatherInput
from utils.config_handler import load_tools_config

rag_service = RAGService()
tools_config = load_tools_config()
load_dotenv()

@tool(return_direct=True,description="""
【历史记忆聊天工具 / 核心闲聊工具】
当用户和你进行日常闲聊、对喷、打招呼、提问，或者抛出任何不属于查询天气和生成报告的话题时，你【必须】调用此工具。
此工具会直接返回一句已经模仿好“米粒”性格的最终回复。
-> 传入参数：请直接将用户的原话作为 query 传入。
-> 传入参数 sender：当前和你说话的群友名字（你可以从当前任务上下文中获取）
""")
def chat_with_memory_tool(query: str, sender: str) -> str:
    """
    使用带有记忆功能的工具进行聊天
    :param query: 用户输入的查询字符串
    :return: 模型生成的回复字符串
    """
    return rag_service.rag_answer(query,sender)



@tool(args_schema=WeatherInput,description="""
【天气查询工具】
当群友询问某个地方的天气时，调用此工具获取真实天气。
-> 传入参数 (city_name) 必须且只能是纯粹的城市名称，例如：“北京”、“郑州”。
-> 传入参数 (relative_day) 是用户想要查询的时间，必须且只能从以下四个词中选一个：'今天'、'明天'、'后天'、'大后天'。如果没有明确说明，默认填'今天'。
""")
def weather_tool(city_name: str,relative_day: str) -> str:
    """获取天气信息的工具"""
    try:

        print(f"[Tool Calling] 获取 {city_name} {relative_day}的天气...")
        amap_key=os.getenv("WEATHER_API_KEY")
        #新的天气api
        url = tools_config['weather_api_url']

        day_index_map = {"今天": 0, "明天": 1, "后天": 2, "大后天": 3}

        if relative_day not in day_index_map:
            return f"米粒只能查询'今天'、'明天'、'后天'、'大后天'的天气"

        # 默认查询今天的天气
        target_index = day_index_map.get(relative_day, 0)

        if target_index == 0:
            params = {"key": amap_key, "city": city_name, "extensions": "base"}
            resp = requests.get(url, params=params, timeout=5).json()
            if not resp.get('lives'):
                return f"找不到 {city_name} 的天气信息哦。"
            live = resp['lives'][0]
            weather, temp = live['weather'], int(live['temperature'])
            return f"{city_name}现在是【{weather}】，气温 {temp}℃。"
        else:
            params = {"key": amap_key, "city": city_name, "extensions": "all"}
            resp = requests.get(url, params=params, timeout=5).json()
            if not resp.get('forecasts'):
                return f"找不到 {city_name} 的天气预报哦。"

            casts = resp['forecasts'][0]['casts']

            # 防止高德返回的数据不够4天导致越界
            if target_index >= len(casts):
                return f"高德气象局暂时还没有给出{city_name}{relative_day}的预报数据呢。"

            target_cast = casts[target_index]
            date_str = target_cast['date']
            day_weather = target_cast['dayweather']
            night_weather = target_cast['nightweather']
            day_temp = target_cast['daytemp']
            night_temp = target_cast['nighttemp']

            return (f"{city_name} {relative_day}（{date_str}）的天气预报：\n"
                    f"白天【{day_weather}】，夜间【{night_weather}】；\n"
                    f"全天气温 {night_temp}℃ ~ {day_temp}℃。")

    except requests.exceptions.Timeout:
        return f"666，看不了{city_name}的天气，气象局API超时卡死了。"
    except Exception as e:
        print(f"[Tool Error] 天气查询异常: {e}")
        return f"我脑子短路了，查不了{city_name}的天气。"

@tool(description="""
【时间查询工具】
当用户的提问中包含“今天”、“明天”、“昨天”、“现在”、“最近”等相对时间概念时，你【必须】先调用此工具获取当前的基准日期和时间！
-> 无需传入参数（如果框架要求传参，传空字符串 "" 即可）。
""")
def get_current_datetime(query: str = "") -> str:
    """获取当前日期和时间的工具"""
    now = datetime.now()
    return f"现在的标准时间是：{now.strftime('%Y-%m-%d %H:%M:%S')}"

if __name__ == '__main__':
    print(weather_tool.invoke("郑州天气怎么样"))
