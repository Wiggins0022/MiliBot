import json
import os
import re


class ChatDataCleaner:
    def __init__(self, raw_data_file, output_file, user_config_file, time_threshold_sec=300):
        self.raw_data_file = raw_data_file
        self.output_file = output_file
        self.time_threshold_sec = time_threshold_sec
        self.user_config_file = user_config_file
        self._bracket_token_re = re.compile(r"\[[^\]]+\]")
        self._unknown_terms = [
            "\u4e0d\u77e5\u9053\u600e\u4e48", "\u4e0d\u592a\u6e05\u695a", "\u4e0d\u4f1a\u554a",
            "\u4e0d\u77e5\u9053\u554a", "\u4e0d\u77e5\u9053\u5462",
            "\u4e0d\u77e5\u9053", "\u4e0d\u6e05\u695a", "\u4e0d\u61c2", "\u4e0d\u4f1a"
        ]

    def load_user_config(self):
        config = {}
        try:
            if not os.path.exists(self.user_config_file):
                print(f"警告: 配置文件 {self.user_config_file} 未找到。")
                return config
            with open(self.user_config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"): continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            print(f"加载配置出错: {e}")
        return config

    def normalize_content(self, content):
        """
        标准化内容
        """
        if not content:
            return ""

        pattern = r'[\u2000-\u200B\u3000\u00A0\t]+'
        # 将所有特殊空格替换为标准空格 ' '
        content = re.sub(pattern, ' ', content)
        # 将连续的多个标准空格合并为一个
        content = re.sub(r' {2,}', ' ', content)

        content = re.sub(r"^[fF]+", lambda m: "6" * len(m.group(0)), content)
        return content.strip()

    def should_drop_content(self, content):
        if not content:
            return True

        if self._bracket_token_re.search(content):
            return True

        if "@" in content:
            return True

        # Drop replacement-char garbage or visible square blocks
        if "\ufffd" in content or "□" in content or "■" in content or "◻" in content or "◼" in content:
            return True

        return False

    def stylize_assistant_content(self, content):
        if not content:
            return content

        for term in self._unknown_terms:
            if term in content:
                if term.endswith("\u554a"):
                    return "666" + term
                return "666" + term + "\u554a"

        return content

    def is_valid_text_message(self, content):
        if not content: return False

        # 过滤 XML、CDATA
        if "<?xml" in content or "CDATA" in content or "<msg" in content:
            return False

        # 过滤占位符
        invalid_markers = [
            "[图片]", "[语音]", "[视频]", "[表情]", "[动画表情]",
            "[文件]", "[小程序]", "[位置]", "[转账]", "[合并转发]",
            "[聊天记录]", "[通话]"
        ]

        for marker in invalid_markers:
            if marker in content:
                return False

        # 过滤URL
        if content.startswith("http://") or content.startswith("https://"):
            return False

        return True

    def clean_and_format_chat_data(self):
        config = self.load_user_config()
        TARGET_USER = config.get("TARGET_USER")
        TARGET_ASSISTANT = config.get("TARGET_ASSISTANT")

        if not TARGET_USER or not TARGET_ASSISTANT:
            print("错误: 缺少用户配置。")
            return

        print(f"开始清洗... User: {TARGET_USER} <-> Assistant: {TARGET_ASSISTANT}")

        with open(self.raw_data_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        conversations = []
        current_session = []
        last_timestamp = 0
        dropped_count = 0
        merge_break = False

        # 基础解析与按时间阈值分割会话
        for line in lines:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            if item.get("_type") != "message": continue

            sender = item.get("accountName")
            raw_content = item.get("content", "")
            timestamp = item.get("timestamp", 0)

            if sender not in [TARGET_USER, TARGET_ASSISTANT]:
                merge_break = True
                continue

            content = self.normalize_content(raw_content)

            if not self.is_valid_text_message(content) or self.should_drop_content(content):
                dropped_count += 1
                merge_break = True
                continue

            role = "user" if sender == TARGET_USER else "assistant"

            # 超过时间阈值，切分新的 session
            if last_timestamp != 0 and (timestamp - last_timestamp > self.time_threshold_sec):
                if current_session:
                    conversations.append(current_session)
                current_session = []

            current_session.append({
                "role": role,
                "content": self.stylize_assistant_content(content) if role == "assistant" else content,
                "merge_break": merge_break,
                "timestamp": timestamp
            })
            merge_break = False
            last_timestamp = timestamp

        if current_session:
            conversations.append(current_session)

        rag_data = []

        for session in conversations:
            if not session:
                continue

            # 合并连续的同角色发言
            merged_messages = []
            for msg in session:
                if not merged_messages:
                    merged_messages.append({"role": msg["role"], "content": msg["content"]})
                else:
                    last_msg = merged_messages[-1]
                    if last_msg["role"] == msg["role"] and not msg.get("merge_break"):
                        # 同一个人的连续发言，用换行符拼接
                        last_msg["content"] += "\n" + msg["content"]
                    else:
                        merged_messages.append({"role": msg["role"], "content": msg["content"]})

            # 保证必须以 user 开头
            while merged_messages and merged_messages[0]["role"] == "assistant":
                merged_messages.pop(0)

            # 保证必须以 assistant 结尾
            while merged_messages and merged_messages[-1]["role"] == "user":
                merged_messages.pop()

            # 有效性检查
            if len(merged_messages) < 2:
                continue

            for i in range(0, len(merged_messages) - 1, 2):
                user_msg = merged_messages[i]
                assistant_msg = merged_messages[i + 1]

                # 确保这是一对完整的 Q&A
                if user_msg["role"] == "user" and assistant_msg["role"] == "assistant":
                    rag_data.append({
                        "question": user_msg["content"],
                        "answer": assistant_msg["content"]
                    })

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(rag_data, f, indent=2, ensure_ascii=False)

        print(f"清洗完成！")
        print(f"- 丢弃无效消息: {dropped_count} 条")
        print(f"- 生成用于 RAG 检索的问答对: {len(rag_data)} 个")
        print(f"- 结果已保存至: {self.output_file}")


if __name__ == "__main__":
    raw_data_file = "chat_history.jsonl"
    output_filename = "MiliBot_RAG.json"
    user_config_file = "../resources/user_config.properties"

    if os.path.exists(raw_data_file):
        cleaner = ChatDataCleaner(raw_data_file, output_filename, user_config_file)
        cleaner.clean_and_format_chat_data()
    else:
        print(f"未找到文件: {raw_data_file}")
