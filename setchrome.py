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
    # 指定 Chrome 的用户数据目录，以保留用户的登录状态、浏览记录等。如果该目录不存在，Chrome 会自动创建。

    chrome_options.add_argument("profile-directory=Default")
    # 指定使用的用户配置文件目录，"Default" 通常是默认用户的配置。

    chrome_options.add_argument("--no-sandbox")
    # 禁用沙盒模式，以提升性能和稳定性。通常用于在无图形界面环境中运行浏览器时。

    chrome_options.add_argument("--disable-dev-shm-usage")
    # 禁用 `/dev/shm`，将共享内存写入硬盘。解决 Docker 容器中共享内存不足的问题。

    chrome_options.add_argument("--disable-gpu")
    # 禁用 GPU 加速，用于避免某些环境中 GPU 渲染导致的问题，例如无图形界面环境。

    chrome_options.add_argument("--start-maximized")
    # 启动时将浏览器窗口最大化，以便获得最佳视图效果。 # chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver
