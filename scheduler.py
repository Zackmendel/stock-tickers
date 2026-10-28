import time
import scheduler
from datetime import datetime
from extract_ticker import extract_tickers

def basic_job():
    print(f'Job Started at: {datetime.now()}')

schedule.every().minute.do(basic_job)

schedule.every().minute.do(extract_tickers)

while True:
    schedule.run_pending()
    time.sleep(1)