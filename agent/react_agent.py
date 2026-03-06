from langchain.agents import create_agent
from model.chat_model import chat_model
from agent.tools import chat_with_memory_tool,weather_tool
from utils.load_prompts import load_main_prompt
from utils.config_handler import load_model_config
from model.model_factory import ModelFactory

class ReactAgent:
    def __init__(self,model_name: str = None):
        if model_name is None:
            model_config = load_model_config()
            model_name = model_config.get('chat_model_name', model_config['default_chat_model_name'])


        model_wrapper = ModelFactory.create_model(model_name)
        chat_model = model_wrapper.generator()

        self.agent = create_agent(
            model=chat_model,
            tools=[chat_with_memory_tool,weather_tool],
            system_prompt=load_main_prompt()
        )

    def create_stream(self, query: str, sender: str=None):
        prompt_with_sender = f"【{sender} 正在和你说话】：\n{query}"

        input_dict = {
            "messages": [
                {"role": "user", "content": prompt_with_sender}
            ]
        }

        for chunk in self.agent.stream(input=input_dict, stream_mode="values"):
            last_messages = chunk['messages'][-1]
            if last_messages:
                yield last_messages.content.strip() + "\n"

if __name__ == '__main__':
    for chunk in ReactAgent().create_stream("我后天去郑州，你建议我后天穿什么？"):
        print(chunk, end='', flush=True)