import os
import re
import pandas as pd

from time import sleep
from pathlib import Path
from datetime import datetime as dt
from numpy import object_

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.expected_conditions import element_to_be_clickable


DATA_PATH = Path('Downloaded data')


def download_data(url, download_btn_locator, file_match_pattern, other_actions=lambda driver: None):
    try:
        caps = DesiredCapabilities.CHROME.copy()
        caps['pageLoadStrategy'] = 'none'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options, desired_capabilities=caps)
        driver.get(url)
        other_actions(driver) # Do some other optional actions (like changing the time period)
        download_btn = WebDriverWait(driver, 20).until(element_to_be_clickable(download_btn_locator))
        driver.execute_script('arguments[0].click();', download_btn)
    except:
        print('SELENIUM ERROR')
        driver.quit()
        raise
    else:
        # Get and return the file path
        filepath = lambda: sorted(Path(Path.home() / 'Downloads').iterdir(), key=os.path.getmtime)[-1]
        while not re.match(file_match_pattern, filepath().name):
            sleep(.5)
            print('Waiting for the download to finish...')
        driver.quit()
        return filepath()


def get_nasdaq_index():
    filename = f'Companies list {dt.today().strftime("%m-%Y")}.csv'
    if not filename in os.listdir(DATA_PATH):
        filepath = download_data(
            'https://www.nasdaq.com/market-activity/stocks/screener/', 
            (By.CLASS_NAME, 'ns-download-1'), 
            r'(nasdaq_screener_)[0-9]+(\.csv)$'
        )
        os.rename(filepath, DATA_PATH / filename)
    df = pd.read_csv(DATA_PATH / filename, encoding='latin1', on_bad_lines='skip', index_col=0)
    return df[['Name', 'Country', 'Sector', 'Market Cap']]


def get_company_data(symbol:str, time_period:str):
    '''
    Time period argument must be one of the following:
    - 'm1' (last month passed)
    - 'm6' (last six months)
    - 'ytd' (all this year till now)
    - 'y1' (last year)
    - 'y5' (last five years)
    - 'y10' (last ten years)
    '''
    def set_time_period(driver):
        if time_period == 'm1':
            return
        time_period_btn = WebDriverWait(driver, 20).until(
            element_to_be_clickable((By.XPATH, f'//button[@data-value="{time_period.lower()}"]'))
        )
        driver.execute_script('arguments[0].click();', time_period_btn)

    filename = f'{symbol.upper()} {time_period.upper()} {dt.today().strftime("%d-%m-%y")}.csv'

    if not filename in os.listdir(DATA_PATH):
        filepath = download_data(
            f'https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}/historical/', 
            (By.CLASS_NAME, 'historical-download'), 
            r'(HistoricalData_)[0-9]+(\.csv)$',
            other_actions=set_time_period
        )
        os.rename(filepath, DATA_PATH / filename)

    df = pd.read_csv(DATA_PATH / filename, index_col=0)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.rename(columns={'Close/Last':'Close'})
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = df.iloc[::-1]
    for i in df:
        if df[i].dtype == object_:
            df[i] = pd.to_numeric(df[i].apply(lambda val: val[1:]))
    return df
