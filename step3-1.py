from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import time
import os
def buttonclick(css_selector):
    try:
        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        button.click()
    except Exception as e:
        print(f"无法点击按钮 {css_selector}")

folder_path = "./step2/success"
# 获取文件夹中的所有文件和文件夹
all_files = os.listdir(folder_path)
files_only = [file for file in all_files if os.path.isfile(os.path.join(folder_path, file))]

chrome_options = Options()
chrome_options.add_argument(
    r"user-data-dir=C:/Users/willy.lin/AppData/Local/Google/Chrome/User Data"
)  # 替换为您的 Chrome 用户配置文件路径
chrome_options.add_argument("profile-directory=Default")  # 使用默认配置文件
chrome_options.add_argument("--no-sandbox")  # 禁用沙盒模式
chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享内存问题
#chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
chrome_options.add_argument(
    "--disable-gpu"
)  # 在部分系统上，禁用 GPU 加速可以提高稳定性

# 初始化 WebDriver 并打开 Chrome
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

for filename in files_only:
    Storeplace = []
    with open(folder_path+"/"+filename, mode="r", newline="", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # 去除每行的换行符和首尾空格
            if line:  # 确保不是空行
                Storeplace.append(line)  # 将整行作为一个字符串加入

    # 初始化处理状态的列表
    unprocessed_storeplaces = Storeplace[:]  # 尚未处理的店名（开始时是所有店名）
    error = []  # 处理失败的店名
    # 设置 Chrome 配置
    
    driver.get("https://www.google.com/maps?authuser=0")

    time.sleep(2)
    buttonclick('button[aria-label="菜單"]')
    buttonclick("button.T2ozWe")
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Io6YTe.fontBodyLarge.kR99db.fdkmkc'))
    )
    div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.Io6YTe.fontBodyLarge.kR99db.fdkmkc')
    Storagelist = [div.text for div in div_elements]
    # 確認有無清單
    if filename.split('.')[0] not in  Storagelist:
        buttonclick('button[aria-label="新增清單"]')
        element = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input.gRsCne.azQIhc"))
            )
        search_box = driver.find_element(By.CSS_SELECTOR, "input.gRsCne.azQIhc")
        search_box.clear()
        search_box.send_keys(f"{filename.split('.')[0]}")
        buttonclick('button.okDpye.PpaGLb')
        driver.get("https://www.google.com/maps?authuser=0")
    driver.get("https://www.google.com/maps?authuser=0")
    try:
        label_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{filename.split('.')[0]}')]"))
        )
        button = label_element.find_element(By.XPATH, "./ancestor::button")
        button.click()
    except Exception as e:
        print(f"无法找到或点击 清單 标签: {e}")
    time.sleep(1)
    buttonclick("button[aria-label='更多選項']")
    buttonclick("div[data-index='0']")


    count = 0
    for Storename in Storeplace:
        try:
            button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.nsq2dc.U7lAq"))
            )
            button.click()
            # 在搜索框输入店名和地址
            element = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input.LxoNjd"))
            )
            search_box = driver.find_element(By.CSS_SELECTOR, "input.LxoNjd")
            search_box.clear()
            search_box.send_keys(f"{Storename}")
            time.sleep(3)
            suggestion_grid = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[role="grid"][aria-label="建議"]#ucc-0')
                )
            )

            # 找到 suggestion_grid 内所有的 div 元素
            div_elements = suggestion_grid.find_elements(
                By.CSS_SELECTOR, 'div[tabindex="-1"]'
            )

            # 获取 div 的数量
            div_count = len(div_elements)
            # 等待搜索建议并点击第一个建议
            if div_count == 1:
                suggestion = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "div[data-suggestion-index='0']")
                    )
                )
                suggestion.click()
                count += 1
                unprocessed_storeplaces.remove(Storename)  # 从未处理列表中移除
                print(f"处理成功: {Storename}, 当前处理计数: {count}")
            else:
                # 如果建议数量不是1，则刷新页面
                print(f"建議数量异常 ({div_count})，刷新页面并重试: {Storename}")
                driver.refresh()  # 刷新页面
                time.sleep(5)  # 等待页面刷新完成后再继续
                error.append(Storename)

        except Exception as e:
            print(f"处理店名 {Storename} 时出错")
            driver.refresh()  # 刷新页面
            time.sleep(5)  # 等待页面刷新完成后再继续
            error.append(Storename)  # 处理失败的加入错误列表

    # 定义文件路径
    success_file_path = "./step3/success/"
    error_file_path = "./step3/error/"

    # 提取文件夹路径并确保目录存在
    success_folder = os.path.dirname(success_file_path)
    error_folder = os.path.dirname(error_file_path)

    # 创建文件夹（如果不存在）
    os.makedirs(success_folder, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)
    with open(error_folder+Storename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for item in error:
            writer.writerow([item])
# 关闭浏览器
driver.quit()