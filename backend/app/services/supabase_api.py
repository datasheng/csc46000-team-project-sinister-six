import os
from supabase import create_client, Client
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
from chroma_langchain import vector_store, build_rag_chain

load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
db: str = os.getenv("DATABASE_URL")
supabase: Client = create_client(url, key)
# TODO:
# perhaps stored procedures either in codebase or internally in supabase for:
# - retrieving data from supabase, to be used for tableau implementation
# - retrieving data from supabase, but to be used locally for sklearn or building regression models in general


def execute_sql(query):
    """
    connects to postgresql -> executes given query -> closes connection
    :param query: SQL query as a string
    :return: None
    """
    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to execute query: {str(e)}")


def create_table(table_name):
    """
    Creates a table in Supabase with a predefined schema.
    if table already exists, nothing happens pretty much
    :param table_name: Table name
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        date DATE NOT NULL,
        open FLOAT8,
        close FLOAT8,
        volume FLOAT8
    );
    """
    try:
        execute_sql(create_table_query)
    except Exception as e:
        print("Couldn't create table")
        return {"error": f"Failed to create table '{table_name}': {str(e)}"}


def store_data_sb(dataframe, table_name):
    """
    ensures table is created/exists -> stores dataframe into table
    inputs: dataframe (pandas DF)
            table_name: table name in supabase
    output: returns the response from API after storing/insert procedure
    """
    if dataframe.empty:
        return {"error": "The dataframe is empty. No data to store."}
    create_table(table_name)
    input_data = dataframe.to_dict(orient="records")
    try:
        response = supabase.table(table_name.lower()).upsert(input_data, ignore_duplicates=True).execute()
        return response
    except Exception as e:
        print(f"Failed to insert into table '{table_name}': {str(e)}. \n Make sure that the table exists or table "
              f"name matches.")
        return {"error": f"Failed inserting into table '{table_name}': {str(e)}"}


def get_data_all_sb(table_name, start_date="1900-01-01", end_date=None):
    """
    input: table_name. examples: SPY, VOO, AAPL (stock symbol and table name treated as interchangeable)
    output: table data as a dataframe
    """
    try:
        if end_date is None:
            end_date = datetime.today().strftime("%Y-%m-%d")
        response = supabase.table(table_name.lower()).select("*").gte("Date", start_date).lte("Date", end_date).execute()
        data = response.data
        return data
    except Exception as e:
        return {"error getting data from Supabase": str(e)}


def query_llm_data(query, table_name):
    """
    currently, this just gives you an LLM response and analysis based on the data that's
    already stored in postgresql. somehow just need the table name as input to get this correctly
    input: query, table_name
    output: LLM response
    """
    store = vector_store(table_name)
    if store:
        print("successful vector store")
        print("building rag chain")
        rag_chain = build_rag_chain()
        history = []
        result = rag_chain.invoke({"input": query, "chat_history": history})
        answer = result.get("answer", "No response available")
        print(answer)
        return answer
    else:
        return "Problem querying LLM"


if __name__ == "__main__":
    query_llm_data("Tell me about your data on the stock voo", 'voo')
