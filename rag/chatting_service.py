from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

from common.lc_modules import getVectorStore, getEmbeddings, getLlm, getMemory

llm = getLlm()
embeddings = getEmbeddings()


def do_chat(question: str, channel: str = 'default', sessionId: str = ''):
    # Given the following conversation and a follow up question, answer the question.
    condense_question_prompt = ChatPromptTemplate.from_template('''
        Chat History: {{chat_history}}

        Question: {question}
    ''')
    # Answer my questions based on your knowledge and our older conversation. Do not make up answers.
    # If you do not know the answer to a question, just say "I don't know".
    combine_docs_custom_prompt = PromptTemplate.from_template('''
        You are DeepMotion's customer service, your name is Marven,

        Context: {context}
        
        {question}
        
        As a customer service, you will answer:
    ''')

    memory = getMemory(sessionId)
    retriever = getVectorStore(embeddings, channel).as_retriever(search_type="similarity", search_kwargs={
        "distance_threshold": 5})
    # retriever = getVectorStore(embeddings, channel).as_retriever(search_type="similarity", k=3)

    qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory,
                                               condense_question_prompt=condense_question_prompt,
                                               combine_docs_chain_kwargs=dict(prompt=combine_docs_custom_prompt),
                                               verbose=False)
    result = qa.run({"question": question})
    return result


if __name__ == "__main__":
    print(do_chat('Who are you?'))
    print('=============================')
    print(do_chat('Where are you from?'))
    print('=============================')
    print(do_chat('Why i cannot login Deepmotion?'))
    print('=============================')
    print(do_chat('How can i close my account?'))
