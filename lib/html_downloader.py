import time

import requests

# headlessのChromeを利用したhtmlダウンローダ
def html_download_by_chrome(url: str, wait_sec: int = 5) -> str:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    def __chrome_option_generator():
        options = Options()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        # 共有メモリファイル出力場所で　/dev/shm　ではなく　/tmp　を利用
        options.add_argument("--disable-dev-shm-usage")
        return options

    driver = webdriver.Chrome(
        'chromedriver',
        chrome_options = __chrome_option_generator(),
    )

    driver.get(url)
    time.sleep(wait_sec)
    html = driver.page_source

    return html

# simpleなhtmlダウンローダ 取得できない値あり
def html_download(url: str) -> str:
    r = requests.get(url)
    return r.text

# example.htmlを返す
def html_example() -> str:
    import pathlib
    current_dir = pathlib.Path(__file__).resolve().parent
    print(pathlib.Path(__file__).resolve().parent)
    exapmle_html_path = str(current_dir) + '/../html_example/example.html'
    with open(exapmle_html_path) as f:
        html = f.read()
        return html
