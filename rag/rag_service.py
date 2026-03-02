from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from rag.knowledge_base import KnowledgeBaseService
from utils.load_prompts import load_rag_prompt, load_person_info
from model.chat_model import chat_model


class RAGService:
    def __init__(self):
        self.retriever = KnowledgeBaseService().get_retriever()

        # 构建提示词模板
        main_prompt_template_str = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(main_prompt_template_str)

        self.person_info = load_person_info()

        self.chat_model = chat_model
        self.parser = StrOutputParser()
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.prompt_template | self.chat_model | self.parser

    def retrieve_relevant_docs(self, query: str):
        """
        从向量数据库中检索与查询相关的文档
        :param query: 查询字符串
        :return: 相关文档列表
        """
        relevant_docs = self.retriever.invoke(query)
        return relevant_docs

    def get_context_from_docs(self, docs) -> str:
        """
        从相关文档中提取上下文信息
        :param docs: 相关文档列表
        :return: 上下文字符串
        """
        context = ""
        counter = 0
        for doc in docs:
            counter += 1
            context += f"文档{counter}：提问：{doc.page_content} 回答：{doc.metadata}\n"
        return context

    def rag_answer(self, query: str) -> str:
        """
        让模型查询知识库并生成回答
        :param query:
        :return:
        """
        relative_docs = self.retrieve_relevant_docs(query)
        context = self.get_context_from_docs(relative_docs)

        # TODO: 这里以后替换成从文件读取最近5条记录的逻辑
        recent_history_str = "暂无近期记录"

        return self.chain.invoke(input={
            "user_input": query,
            "context": context,
            "person_info": self.person_info,
            "recent_history": recent_history_str
        })

if __name__ == '__main__':
    print(RAGService().rag_answer("来财吗"))