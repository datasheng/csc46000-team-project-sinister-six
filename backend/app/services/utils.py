import pandas as pd


def process_stock_data(data):
    """
    Processes stock data by resetting the index, renaming columns to match Supabase schema,
    and converting the 'Date' column from UNIX timestamp to 'YYYY-MM-DD' format.
    :param data: Pandas DataFrame
    :return: Processed Pandas DataFrame
    """
    # Reset index
    data.reset_index(inplace=True)

    # Rename columns to match Supabase schema
    data.rename(columns={
        "Date": "date",
        "Open": "open",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)

    # Convert UNIX timestamp to datetime and format as 'YYYY-MM-DD'
    data["date"] = pd.to_datetime(
        data["date"], unit="ms").dt.strftime('%Y-%m-%d')

    return data
