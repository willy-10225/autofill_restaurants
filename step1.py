import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

path = ".\step1"
orurl = "https://guide.michelin.com"
urllist = [
    "https://guide.michelin.com/tw/zh_TW/restaurants/3-stars-michelin",
    "https://guide.michelin.com/tw/zh_TW/restaurants/2-stars-michelin",
    "https://guide.michelin.com/tw/zh_TW/restaurants/1-star-michelin",
    "https://guide.michelin.com/tw/zh_TW/restaurants/bib-gourmand",
]
# 设置 Chrome 驱动和无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # 禁用图片加载
chrome_options.add_argument("--disable-javascript")  # 禁用JavaScript
chrome_options.add_argument("--disable-extensions")  # 禁用扩展
chrome_options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口
chrome_options.add_argument("--no-sandbox")  # 解决DevToolsActivePort文件不存在的报错
# 设置 Chrome 驱动
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)
for mainurl in urllist:
    # 打开网页
    driver.get(mainurl)  # 替换为目标网址
    orlist = []
    # 等待特定元素加载完成
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "h1")
            )  # 替换为实际的元素选择器
        )
        # 获取最终 HTML
        final_html = driver.page_source
        soup = BeautifulSoup(final_html, "html.parser")
        a = soup.find("ul", class_="pagination")
        b = [i.find("a").get("href") for i in a.find_all("li")][-2]
        lastpage = int(b.split("/")[-1])
        a = soup.find(
            "div", class_="row restaurant__list-row js-restaurant__list_items"
        )
        orlist += [
            orurl + i.find("a", class_="link").get("href")
            for i in a.find_all("div", class_="col-md-6 col-lg-4 col-xl-3")
        ]
        for i in range(2, lastpage + 1):
            driver.get(mainurl + f"/page/{i}")
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h1")
                )  # 替换为实际的元素选择器
            )
            # 获取最终 HTML
            final_html = driver.page_source
            soup = BeautifulSoup(final_html, "html.parser")
            a = soup.find(
                "div", class_="row restaurant__list-row js-restaurant__list_items"
            )
            orlist += [
                orurl + i.find("a", class_="link").get("href")
                for i in a.find_all("div", class_="col-md-6 col-lg-4 col-xl-3")
            ]
            print(len(orlist))
    except Exception as e:
        print("出现错误:", e)

    os.makedirs(path, exist_ok=True)
    # 读取 CSV 文件并将内容存储到 orlist 列表中，确保一行一条 URL
    with open(
        path + rf"\{mainurl.split('/')[-1]}.csv", mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        for url in orlist:
            writer.writerow([url])  # 将每个 URL 作为独立的一行写入
# 关闭浏览器
driver.quit()
