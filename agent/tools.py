from langchain_core.tools import tool
import requests
from rag.rag_service import RAGService
from datetime import datetime

rag_service = RAGService()

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

@tool(description="获取天气信息，输入一个地点名称，返回该地点的天气信息")
def weather_tool(query: str):
    """
    获取天气信息的工具
    :param query: 用户输入的查询字符串
    :return: 天气信息字符串
    """
    # 这里可以调用实际的天气API来获取天气信息
    return "这是一个模拟的天气信息回复。"


# WMO 国际气象组织的天气代码翻译字典
WEATHER_CODES = {
    0: "晴朗",
    1: "大部晴朗", 2: "部分多云", 3: "阴天",
    45: "有雾", 48: "沉积雾",
    51: "轻度毛毛雨", 53: "中度毛毛雨", 55: "密集毛毛雨",
    61: "微雨", 63: "中雨", 65: "大雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    95: "雷阵雨", 96: "雷暴伴有冰雹"
}


@tool(return_direct=True, description="""
【天气查询工具】
当群友询问某个地方的天气时，调用此工具获取真实天气。
-> 传入参数 (city) 必须且只能是纯粹的城市名称，例如：“北京”、“郑州”。
""")
def weather_tool(city: str) -> str:
    """获取天气信息的工具"""
    try:
        # 清洗城市名称
        clean_city = city.replace("市", "").replace("天气", "").replace("怎么样", "").replace("的", "").strip()
        print(f"[Tool Calling] 正在查询 {clean_city} 的经纬度...")

        # 把城市名转成经纬度
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_city}&count=1&language=zh"
        geo_resp = requests.get(geo_url, timeout=5).json()

        if "results" not in geo_resp or len(geo_resp["results"]) == 0:
            return f"地理盲区啊，根本找不到【{clean_city}】这个地方，你是不是字打错了？"

        location = geo_resp["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location.get("name", clean_city)

        # 根据经纬度查询当前实时天气
        print(f"[Tool Calling] 获取 {city_name} (Lat: {lat}, Lon: {lon}) 的实时天气...")
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url, timeout=5).json()

        # 解析天气数据
        current = weather_resp.get("current_weather", {})
        temp = current.get("temperature", "未知")
        weather_code = current.get("weathercode", -1)

        # 匹配中文天气描述
        condition = WEATHER_CODES.get(weather_code, "未知神秘天气")
        if temp < 0:
            return f"{city_name}现在是【{condition}】，气温 {temp}℃。记得保暖哦！"
        elif temp > 30:
            return f"{city_name}现在是【{condition}】，气温 {temp}℃。出门记得防晒哦！"
        else:
            return f"{city_name}现在是【{condition}】，气温 {temp}℃。"

    except requests.exceptions.Timeout:
        return f"666，看不了{clean_city}的天气，气象局API超时卡死了。"
    except Exception as e:
        print(f"[Tool Error] 天气查询异常: {e}")
        return f"我脑子短路了，查不了{clean_city}的天气。"

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
    print(weather_tool.invoke("北京"))