import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

url: str = os.getenv("SUPABASE_URL")  # right now considered empty in .env; awaiting info on this & key
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# TODO:
# need .env info: URL & KEY @Tajwar
# perhaps stored procedures either in codebase or internally in supabase for:
# - storing dataframes into supabase
# - retrieving data from supabase, to be used for tableau implementation
# - retrieving data from supabase, but to be used locally for sklearn or building regression models in general


def store_data_sb(dataframe, table_name):
    """
    inputs: dataframe (pandas DF), table_name in supabase
    output: returns the response from API after storing/insert procedure
    """
    input_data = dataframe.to_dict(orient="records")
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
