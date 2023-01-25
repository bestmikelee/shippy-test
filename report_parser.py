import os
from pathlib import Path
import camelot

def parse_pdfs():
    path = Path('./external/reports/AAPL_JPM.pdf')
    print(path)
    tables = camelot.read_pdf('./external/reports/AAPL_JPM.pdf')
    camelot.plot(tables[0], kind='text').show()

if __name__ == "__main__":
    parse_pdfs()