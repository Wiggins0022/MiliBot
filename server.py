import re

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import time
import asyncio

from agent.react_agent import ReactAgent
from rag.history_manager import HistoryManager

my_agent = ReactAgent()
print("智能体加载完毕！")

history_db = HistoryManager()

# 创建 FastAPI 应用
app = FastAPI(title="MiliBot Agent API", version="2.0")


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "Mili-Agent",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "MiliBot"
            }
        ]
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    # 解析 AstrBot 发过来的 JSON 数据
    data = await request.json()

    messages = data.get("messages", [])
    user_model = data.get("model", "Mili-Agent")

    # 从历史消息数组中，提取出用户最后发的一句话
    latest_query = ""
    # 获取用户
    current_sender = "未知群友"
    for msg in reversed(messages):
        if msg.get("role") == "user":
            raw_content = msg.get("content", "")

            # 兼容多模态/图文混合消息格式
            if isinstance(raw_content, list):
                text_parts = [part.get("text", "") for part in raw_content if
                              isinstance(part, dict) and part.get("type") == "text"]
                latest_query = " ".join(text_parts)
            else:
                latest_query = str(raw_content)
            break

    if not latest_query.strip():
        latest_query = "（用户发送了图片或表情包，无文字内容）"

    match = re.search(r'(.*?)\s*<system_reminder>User ID: \d+, Nickname: (.*)', latest_query)
    if match:
        latest_query = match.group(1).strip()  # 获取提问内容
        current_sender = match.group(2).strip()  # 获取昵称

    print(f"\n[收到 AstrBot 请求] 用户{current_sender}：最新问题: {latest_query}")

    def run_agent_sync():
        """
        同步运行Agent stream。
        """
        final_reply = ""
        for chunk in my_agent.create_stream(latest_query,sender=current_sender):
            final_reply = chunk
        return final_reply.strip()

    try:
        bot_reply = await asyncio.to_thread(run_agent_sync)

        if not bot_reply:
            bot_reply = "666，主板烧了，你刚才说什么？"

        print(f"[Agent 思考完毕] 最终回复内容: {bot_reply}")

        # 将用户的提问和模型的回复都保存到历史记录数据库中
        history_db.add_message(role="user", sender_name=current_sender, interact_with=current_sender,
                               content=latest_query)
        history_db.add_message(role="bot", sender_name="米粒", interact_with=current_sender, content=bot_reply)

    except Exception as e:
        print(f"[报错] Agent 调用失败: {e}")
        bot_reply = f"米粒脑子短路了，后台报错：{str(e)}"

    return JSONResponse({
        "id": "chatcmpl-" + str(int(time.time())),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": user_model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": bot_reply
                },
                "finish_reason": "stop"
            }
        ]
    })


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
