from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import time
import asyncio

# ==========================================
# 1. 导入你写好的 主智能体 (Agent)
# 注意：请确保导入路径和你的实际文件名一致！
# ==========================================
from agent.react_agent import ReactAgent  # 假设你的 Agent 写在这个文件里

print("🚀 正在初始化主智能体 (Agent)，请稍候...")
my_agent = ReactAgent()
print("✅ 主智能体加载完毕！")

# 创建 FastAPI 应用
app = FastAPI(title="MiliBot Agent API", version="2.0")


# ==========================================
# 补充接口：伪装 OpenAI 的模型列表 (菜单)
# 防止 AstrBot 连接时报 404 错误
# ==========================================
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

    print(f"\n[收到 AstrBot 请求] 用户最新问题: {latest_query}")

    # ==========================================
    # 💡 核心修改：调用 Agent 引擎，获取最终回复
    # ==========================================
    def run_agent_sync():
        """
        同步运行你的 Agent stream。
        因为你的 create_stream 会 yield 很多次，
        我们只需要不断覆盖变量，最后保留下来的就是 Agent 的最终发言。
        """
        final_reply = ""
        # 调用你写好的 create_stream 方法
        for chunk in my_agent.create_stream(latest_query):
            final_reply = chunk
        return final_reply.strip()

    try:
        # 丢进后台线程执行，绝对不卡死 FastAPI 的网络监听！
        bot_reply = await asyncio.to_thread(run_agent_sync)

        # 万一 Agent 抽风啥也没返回，做个兜底
        if not bot_reply:
            bot_reply = "666，主板烧了，你刚才说什么？"

        print(f"[Agent 思考完毕] 最终回复内容: {bot_reply}")

    except Exception as e:
        print(f"[报错] Agent 调用失败: {e}")
        bot_reply = f"米粒脑子短路了，后台报错：{str(e)}"

    # ==========================================
    # 打包成标准的 OpenAI 格式返回给 AstrBot
    # ==========================================
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
    print("🌟 启动 FastAPI 服务器...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
