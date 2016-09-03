import argparse
from loggy import loggy
import requests
from sys import stdout

LOGGY = loggy('fetch_data')
SRC_URL = "https://www.tdcj.state.tx.us/documents/High_Value_Data_Sets.xlsx"

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Downloads data from tdcj.state.tx.us")
    args = parser.parse_args()

    LOGGY.info("Downloading: %s" % SRC_URL)

    resp = requests.get(SRC_URL, stream=True)
    for chunk in resp.iter_content(chunk_size=1024):
        if chunk:
            stdout.buffer.write(chunk)
