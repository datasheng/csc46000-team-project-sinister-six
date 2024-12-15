import os, requests

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()
CHROMA_PATH = "chroma"
OPENAI_KEY = os.getenv("OPENAI_KEY")
embed = OpenAIEmbeddings(
    api_key=OPENAI_KEY,
    model="text-embedding-3-large"
)
db = Chroma(
            collection_name="stocks",
            embedding_function=embed,
            persist_directory=CHROMA_PATH
        )
retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 2, "score_threshold": 0.05},
        )
server_ip = 'http://localhost:5000'

def vector_store(table_name):
    try:
        search_query = f"Stock Name: {table_name}"
        search_results = retriever.invoke(search_query)
        if search_results:
            print("data found, no need for vector store!")
            return True
        else:
            print("Data not found. need to vector store")
        try:
            response = requests.get(f"{server_ip}/get_stocks_db?index={table_name}")
            data = response.json()
            print("data retrieved from API successfully. ")
            for item in data:
                # might need to implement a way to avoid double counting data
                db.add_texts(
                    texts=[
                        f"Stock Name: {table_name}, Open: {item['Open']}, High: {item['High']}, Low: {item['Low']}, Close/Last: {item['Close/Last']}, Volume: {item['Volume']}"],
                    # Use the text field for embedding
                    metadatas=[{
                        "stock": table_name,
                        "date": item["Date"],
                        "close_last": item["Close/Last"],
                        "open": item["Open"],
                        "high": item["High"],
                        "low": item["Low"],
                        "volume": item["Volume"]
                    }]
                )
            return True
        except Exception as e:
            print("encountered an error when sending request: ", str(e))
    except requests.exceptions.RequestException as e:
        return False

def build_rag_chain():
    model = ChatOpenAI(
        api_key=OPENAI_KEY,
        model="gpt-4o"
    )
    context = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )
    context_history = ChatPromptTemplate(
        [
            ("system", context),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        model, retriever, context_history
    )
    query = (
        f"You are an assistant for question-answering tasks. "
        f"The context given is about stocks, etfs, and their recent data which will be given to you."
        f"Base the answer ONLY on the data given to you relating to the given query and "
        f"the discussed stock's data. The data given is based on the past 3 months of the stock's data."
        f"\n\n"
        "{context}"
    )
    final_prompt = ChatPromptTemplate(
        [
            ("system", query),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    qna_chain = create_stuff_documents_chain(model, final_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qna_chain)
    return rag_chain
