import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

user_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data")


def get_chrome_driver():
    global user_data_dir
    chrome_options = Options()
    chrome_options.add_argument(rf"user-data-dir={user_data_dir}")
    chrome_options.add_argument("profile-directory=Default")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver
