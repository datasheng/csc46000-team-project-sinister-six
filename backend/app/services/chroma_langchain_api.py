import os, requests
import pandas as pd
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
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
    csv_path = f"./data/{table_name}.csv"
    try:
        search_query = f"Stock Name: {table_name}"
        search_results = retriever.invoke(search_query)
        if search_results:
            print("data found, no need for vector store!")
            return True
        else:
            print("Data not found. need to vector store")
        try:
            postgres_to_csv(table_name, csv_path)
            loader = CSVLoader(file_path=csv_path)
            documents = loader.load()

            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]

            db.add_texts(texts=texts, metadatas=metadatas)
            return True
        except Exception as e:
            print("encountered an error when sending request: ", str(e))
    except requests.exceptions.RequestException as e:
        return False


def postgres_to_csv(table_name, csv_path):
    response = requests.get(f"{server_ip}/get_stocks_db?index={table_name}")
    data = response.json()
    print("data retrieved from API successfully. ")
    os.makedirs("./data", exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print(f"data saved to CSV: {csv_path}")


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
