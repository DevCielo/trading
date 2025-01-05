import pandas as pd

def add_pair_sheets(df_ma_res, writer):
    # For each pair in the df_ma_res (i.e. each combination of long and short moving average applied to a trading pair)
    for p in df_ma_res.pair.unique():
        tdf = df_ma_res[df_ma_res.pair == p]
        tdf.to_excel(writer, sheet_name=p, index=False)

def prepare_data(df_ma_res, df_ma_trades):
    df_ma_res.sort_values(by=['pair', 'total_gain'], ascending=[True, False], inplace=True)

    # Remove timezone cause excel crashes :(
    df_ma_trades['time'] = [ x.replace(tzinfo=None) for x in df_ma_trades['time']]

def process_data(df_ma_res, df_ma_trades, writer):
    prepare_data(df_ma_res, df_ma_trades)
    add_pair_sheets(df_ma_res, writer)


def create_excel(df_ma_res, df_ma_trades, granularity):
    filename = f"ma_sim_{granularity}.xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    process_data(
        df_ma_res[df_ma_res.granularity == granularity].copy(), 
        df_ma_trades[df_ma_trades.granularity == granularity].copy(), 
        writer
    )

    writer.close()

if __name__ == "__main__":

    # Summary of performance metrics for each combination of long and short moving averages applied to different
    # trading pairs and time granularities
    df_ma_res = pd.read_pickle("../data/ma_res.pkl")

    # Info about each individual trade executed by MA strategies
    df_ma_trades = pd.read_pickle("../data/ma_trades.pkl")

    create_excel(df_ma_res, df_ma_trades, "H1")
    create_excel(df_ma_res, df_ma_trades, "H4")