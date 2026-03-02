from langchain.agents import create_agent
from model.chat_model import chat_model
from agent.tools import chat_with_memory_tool,weather_tool

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            tools=[chat_with_memory_tool,weather_tool]
        )

    def create_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        for chunk in self.agent.stream(input=input_dict, stream_mode="values"):
            last_messages = chunk['messages'][-1]
            if last_messages:
                yield last_messages.content.strip() + "\n"

if __name__ == '__main__':
    for chunk in ReactAgent().create_stream("北京的天气怎么样？"):
        print(chunk, end='', flush=True)