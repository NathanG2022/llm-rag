import os
from typing import List

from cachetools import TTLCache, cached
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_google_vertexai import VertexAI
from langchain_openai import ChatOpenAI

from common.utils import getAbsPathLocatedFromCurFile
from config import SETTINGS


def getVectorStore(embeddings: Embeddings, channel: str) -> VectorStore:
    if SETTINGS.env == 'local':
        from langchain_community.vectorstores.redis import Redis
        return Redis(SETTINGS.redis_url, 'rag_' + channel, embeddings)
    else:
        import cassio
        from langchain_community.vectorstores import Cassandra

        cassio.init(
            database_id='d3f3fbf0-7f8e-4b5b-953e-dce7765e2d25',
            token='AstraCS:GNArOxDwWNdzkSLDXcbtSyqP:33cb2e28abb5a835257616be89775f89149a395488976ad277d7c5e9cee32c38',
        )

        return Cassandra(embeddings,
                         session=None,
                         table_name='rag_' + channel,
                         keyspace="default_keyspace")


def saveDocToVectorStore(documents: List, embeddings: Embeddings, channel: str) -> VectorStore:
    if SETTINGS.env == 'local':
        from langchain_community.vectorstores.redis import Redis
        return Redis.from_documents(documents, embeddings,
                                    redis_url=SETTINGS.redis_url,
                                    index_name='rag_' + channel)
    else:
        import cassio
        from langchain_community.vectorstores import Cassandra

        cassio.init(
            database_id='d3f3fbf0-7f8e-4b5b-953e-dce7765e2d25',
            token='AstraCS:GNArOxDwWNdzkSLDXcbtSyqP:33cb2e28abb5a835257616be89775f89149a395488976ad277d7c5e9cee32c38',
        )

        return Cassandra.from_documents(documents, embeddings,
                                        session=None,
                                        table_name='rag_' + channel,
                                        keyspace="default_keyspace")


def getEmbeddings() -> Embeddings:
    # return OpenAIEmbeddings(api_key=SETTINGS.openai_api_key)
    from langchain_google_vertexai import VertexAIEmbeddings
    return VertexAIEmbeddings('textembedding-gecko@001')


def getLlm(model_name: str = "gemini-1.5-flash-001") -> ChatOpenAI | VertexAI:
    if model_name == 'gpt':
        os.environ["OPENAI_API_KEY"] = SETTINGS.openai_api_key
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    # elif model_name == 'llama3':
    #     LLM_Model = './meta-llama/Meta-Llama-3-8B-Instruct'
    #     model, tokenizer = load_llm(LLM_Model)
    else:
        from langchain_google_vertexai import ChatVertexAI
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = getAbsPathLocatedFromCurFile(__file__,
                                                                                    "../config/mobile-app-services-1a26dd1943d6.json")
        return ChatVertexAI(model_name=model_name, temperature=0)


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def getMemory(sessionId: str):
    return ConversationBufferWindowMemory(memory_key='chat_history', k=3,
                                          return_messages=True)
    # return ConversationBufferMemory(memory_key='chat_history', input_key="question", max_len=50,
    #                                 return_messages=True)
