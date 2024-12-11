import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2 import sql

load_dotenv()

# right now considered empty in .env; awaiting info on this & key
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
db: str = os.getenv("DATABASE_URL")

supabase: Client = create_client(url, key)

# TODO:
# need .env info: URL & KEY @Tajwar
# perhaps stored procedures either in codebase or internally in supabase for:
# - storing dataframes into supabase
# - retrieving data from supabase, to be used for tableau implementation
# - retrieving data from supabase, but to be used locally for sklearn or building regression models in general


def execute_sql(query):
    """
    Execute a raw SQL query on the Supabase database.
    :param query: SQL query as a string
    :return: None
    """
    try:
        # Connect to the PostgreSQL database
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
    execute_sql(create_table_query)


def store_data_sb(dataframe, table_name):
    # """
    # inputs: dataframe (pandas DF), table_name in supabase
    # output: returns the response from API after storing/insert procedure
    # """
    # input_data = dataframe.to_dict(orient="records")
    # response = supabase.table(table_name).insert(input_data).execute()
    # if response.get("error"):
    #     print(f"Error: {response.get('error')}")
    # return response
    """
    Creates a new table in Supabase (if not exists) and stores the provided DataFrame.
    :param dataframe: Pandas DataFrame to store
    :param table_name: Name of the table to create and store data into
    :return: Response from Supabase API
    """
    if dataframe.empty:
        return {"error": "The dataframe is empty. No data to store."}

    try:
        # Call the separate function for table creation
        create_table(table_name)
    except Exception as e:
        return {"error": f"Failed to create table '{table_name}': {str(e)}"}

    input_data = dataframe.to_dict(orient="records")

    # try:
    #     response = supabase.table(table_name).insert(input_data).execute()
    #     if "error" in response:
    #         return {"error": response.get("error")}
    #     return {"status": "success", "data": response.get("data")}
    # except Exception as e:
    #     return {"error": f"Failed to insert data into table '{table_name}': {str(e)}"}
    response = supabase.table(table_name).insert(input_data).execute()
    if response.get("error"):
        print(f"Error: {response.get('error')}")
    return response


def get_data_sb(table_name):
    """
    input: table_name. examples: SPY, VOO, AAPL (stock symbol and table name treated as interchangeable)
    output: table data as a dataframe
    """
    response = supabase.table(table_name).select("*").execute()
    df = pd.read_json(response)
    print("dataframe: ", df)
    return df
