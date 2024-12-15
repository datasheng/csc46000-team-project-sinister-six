import pandas as pd


def process_stock_data(data):
    """
    Processes stock data by resetting the index, renaming columns to match Supabase schema,
    and converting the 'Date' column from UNIX timestamp to 'YYYY-MM-DD' format.
    :param data: Pandas DataFrame
    :return: Processed Pandas DataFrame
    """
    data.reset_index(inplace=True)

    data.rename(columns={
        "Close": "Close/Last",
    }, inplace=True)

    data["Date"] = pd.to_datetime(
        data["Date"], unit="ms").dt.strftime('%Y-%m-%d')

    return data
