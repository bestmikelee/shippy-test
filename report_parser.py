import asyncio
import glob
import pandas as pd
import camelot

from db.executors import DailyExecutor, ReportExecutor

pdf_settings = {
    "JPM": {
        "flavor": "stream",
        "table_areas": ['0,375,520,325', '0,325,520,250', '0,250,520,200', '0,175,520,125','0,125,520,50']
    },
    "MORNING": {
        "flavor": "lattice"
    }
}

financial_categories = {
    "revenue": ['Sales/Revenue', 'Revenue'],
    "gross_income": ['Income(Gross)', 'Gross Income'],
    "ebitda": ['EBITDA'],
    "income_tax": ['Income Tax']
}

def process_report(ticker, analyst):
    paths = glob.glob(f"./external/reports/{ticker.upper()}/*.pdf")
    matching_report_paths = [path for path in paths if analyst.lower() in path.lower()]
    if len(matching_report_paths) == 0:
        raise PDFNotFoundException
    if len(matching_report_paths) > 1:
        # figure out why more than one might be matching
        pass
    if len(matching_report_paths) == 1:
        tables = camelot.read_pdf(matching_report_paths[0], **pdf_settings[analyst.upper()])
        merged_tables = pd.concat([table.df for table in tables]).drop_duplicates()
        # turn top row to column header
        merged_tables.columns = merged_tables.iloc[0]
        # delete top row
        merged_tables.drop(index=0, inplace=True)

        merged_tables.set_index(merged_tables.columns[0], drop=True, inplace=True)
        merged_tables = merged_tables.apply(apply_over_axis)
        merged_tables.dropna(inplace=True)
        merged_tables.index = merged_tables.index.map(normalize_indexes)
    return merged_tables

def dataframe_to_rows(table: pd.DataFrame):
    to_add = {}
    for index, rows in table.iterrows():
        for year, val in rows.items():
            to_add[year] = to_add.get(year, { "measured_year": year })
            to_add[year][index] = val
    return to_add.values()

class PDFNotFoundException(Exception):
    pass

def is_year(year: str):
    return year.isnumeric() and int(year) > 1900 and int(year) < 2100

def apply_over_axis(axis):
    return axis.apply(shorthand_to_number)

def shorthand_to_number(short: str):
    if pd.isna(short):
        return None
    short = short.upper()
    if "B" in short:
        short = short.replace("B", "")
        try:
            return int(float(short) * 10**6)
        except Exception as _: 
            return None

def normalize_indexes(index_name):
    for k, v in financial_categories.items():
        if index_name in v:
            return k
    return index_name


if __name__ == "__main__":
    report_exec = ReportExecutor()
    daily_executor = DailyExecutor()
    processed = process_report("aapl", "morning")
    rows = dataframe_to_rows(processed)
    asset = asyncio.run(daily_executor.select_asset("AAPL"))
    for row in rows:
        asyncio.run(report_exec.insert_report(asset.id, "morning", 0, "", **row))