from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config_handler import load_chroma_config
from model.embedding_model import embedding_model
from utils.logger_handler import logger
import os
import json
import time


class KnowledgeBaseService:
    def __init__(self):
        self.chroma_config = load_chroma_config()
        self.vector_store = Chroma(
            collection_name=self.chroma_config['collection_name'],
            embedding_function=embedding_model,
            persist_directory=self.chroma_config['persist_directory']
        )

    def load_json_to_vectordb(self, json_file_path: str):
        """
        读取清洗好的 RAG JSON 文件并批量存入 Chroma 向量数据库
        """
        if not os.path.exists(json_file_path):
            logger.error(f"【load_json_to_vectordb】找不到文件: {json_file_path}")
            return

        logger.info(f"开始加载 JSON 文件: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            rag_data = json.load(f)

        documents = []
        for item in rag_data:
            question = item.get("question", "").strip()
            answer = item.get("answer", "").strip()

            if not question or not answer:
                continue

            doc = Document(
                page_content=question,
                metadata={"answer": answer, "source": "chat_history"}
            )
            documents.append(doc)

        total_docs = len(documents)
        if total_docs == 0:
            logger.info("【load_json_to_vectordb】没有有效的问答对可供入库，已跳过向量化过程")
            return

        logger.info(f"共找到 {total_docs} 条有效的问答对，开始批量入库到 Chroma 向量数据库...")

        batch_size = 100

        for i in range(0, total_docs, batch_size):
            batch = documents[i: i + batch_size]
            self.vector_store.add_documents(batch)
            logger.info(f"已成功入库: {min(i + batch_size, total_docs)} / {total_docs}")

            time.sleep(1)

        logger.info("所有文档已成功入库到 Chroma 向量数据库！")

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": self.chroma_config['search_k']})


if __name__ == "__main__":
    kb_service = KnowledgeBaseService()

    kb_service.load_json_to_vectordb("../data/MiliBot_RAG.json")
