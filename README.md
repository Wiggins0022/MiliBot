MiliBot - 个性化群助手 Agent

一个面向 QQ 群场景的个性化群助手 Agent，支持日常聊天、天气查询、聊天报告总结（功能持续开发中），并可通过 NapCat + AstrBot 接入 QQ 群。项目提供 OpenAI 兼容接口，方便在 AstrBot 中快速配置。

功能亮点
- 个性化群聊助手：基于提示词与个人信息进行风格化对话
- 天气查询：内置天气工具（Open-Meteo）
- 群聊 RAG：基于 Chroma 的知识库检索
- OpenAI 兼容 API：可直接接入 AstrBot

项目结构
- `server.py`：FastAPI 服务，提供 `/v1/models` 与 `/v1/chat/completions`
- `agent/`：Agent 与工具定义
- `rag/`：RAG 相关逻辑与向量库入口
- `prompts/`：提示词与人设
- `resources/`：模型与路径配置

快速开始
1. 创建环境并安装依赖
   - `python -m venv .venv`
   - `pip install -r requirement.txt`
2. 配置环境变量
   - 设置 DashScope API Key（通义千问）
   - Windows PowerShell: `setx ALIYUN_API_KEY "你的Key"`
3. 准备人设与配置
   - 复制 `prompts/person_info.example.txt` -> `prompts/person_info.txt`
   - 复制 `resources/user_config.example.properties` -> `resources/user_config.properties`
4. 初始化 RAG（可选）
   - 准备你的 `data/MiliBot_RAG.json`
   - 运行 `python rag/knowledge_base.py` 生成 `chroma_db/`
5. 启动服务
   - `python server.py`
   - 默认监听 `http://127.0.0.1:8000`

NapCat + AstrBot 接入 QQ 群（概要流程）
1. 启动 NapCat 并登录 QQ
2. 启动 AstrBot，选择 NapCat 作为 QQ 适配器
3. 在 AstrBot 的模型/LLM 配置里选择 OpenAI 兼容接口
   - Base URL: `http://127.0.0.1:8000/v1`
   - Model: `Mili-Agent`
   - API Key: 可填写任意占位（本地服务不校验）
4. 确认 AstrBot 已加入目标群并启用对话

隐私与开源说明
- `data/*.json*`、`chroma_db/`、`rag/chroma_db/`、`agent/logs/` 已加入 .gitignore
- `prompts/person_info.txt`、`resources/user_config.properties` 为本地私有配置，不上传
- 若这些文件此前已被 Git 跟踪，请先执行 `git rm --cached <path>` 再提交

欢迎感兴趣的开发者继续扩展工具（tool），以丰富 Agent 的能力与场景。
