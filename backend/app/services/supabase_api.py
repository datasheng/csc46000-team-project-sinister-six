import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

url: str = os.getenv("SUPABASE_URL") # right now considered empty in .env; awaiting info on this & key
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# TODO:
# need .env info: URL & KEY @Tajwar
# perhaps stored procedures either in codebase or internally in supabase for:
# - storing dataframes into supabase
# - retrieving data from supabase, to be used for tableau implementation
# - retrieving data from supabase, but to be used locally for sklearn or building regression models in general
