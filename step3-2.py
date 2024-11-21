from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import os
from htmlComparison import htmlComparison
from difflib import SequenceMatcher

success_file_path = "./step3/3-2"
error_file_path = "./step3/error"
os.makedirs(error_file_path, exist_ok=True)
def getstorename(entry, str1):
    parts = entry.split(",")
    if len(parts) > 1:
        name_part = parts[0].split(str1)[0].strip()
        city_part = ", ".join(part.strip() for part in parts[1:])
        return f"{name_part}, {city_part}"
    return entry  # 如果没有处理，就返回原字符串

def saveerror(item: str,filename: str):
    with open(error_file_path+"/"+filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([item])
# 获取文件夹中的所有文件和文件夹
all_files = os.listdir(success_file_path)

files_only = [file for file in all_files if os.path.isfile(os.path.join(success_file_path, file))]

user_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data")
chrome_options = Options()
chrome_options.add_argument(rf"user-data-dir={user_data_dir}")
chrome_options.add_argument("profile-directory=Default")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)
def buttonclick(css_selector, index=0):
    """
    点击指定索引的按钮
    :param css_selector: CSS 选择器
    :param driver: WebDriver 实例
    :param index: 按钮的索引，默认是第一个（0）
    """
    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        if index < len(buttons):
            buttons[index].click()
            print(f"成功点击第 {index} 个按钮 {css_selector}")
        else:
            print(f"索引 {index} 超出按钮数量范围（总共有 {len(buttons)} 个按钮）")
    except Exception as e:
        print(f"无法点击按钮 {css_selector} 的第 {index} 个: {e}")

def save(div_elements,search_box):
    
    div_elements = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.etWJQ.jym1ob"))
    )
    
    if len(div_elements) > 1:
        button = div_elements[1].find_element(By.CSS_SELECTOR, "button.g88MCb.S9kvJb")
        aria_label_value = button.get_attribute("aria-label")
        if aria_label_value == "儲存":
            button.click()
            suggestion_grid = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[aria-label="儲存至清單中"]')
                )
            )
            label_element = suggestion_grid.find_element(
                By.XPATH, f'.//div[contains(text(), "{search_box}")]'
            )
            outer_div = label_element.find_element(
                By.XPATH,
                './ancestor::div[@aria-checked="false" and @role="menuitemradio"]',
            )
            outer_div.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'button[data-value="已儲存"]')
                )
            )
            print(f"{i} 已儲存")

        else:
            print(f"{i} 已儲存 (未点击保存按钮)")

    else:
        print("没有足够的 div 元素可供选择")
    time.sleep(3)

driver.get("https://www.google.com/maps?authuser=0")
time.sleep(2)
buttonclick('button[aria-label="菜單"]')
time.sleep(2)
buttonclick("button.T2ozWe")

def dropdownmenu(html:str):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, html))
    )
    div_elements = driver.find_elements(By.CSS_SELECTOR, html)
    Storagelist = [div.text for div in div_elements]
    return Storagelist
# for filenames in files_only:
#     Storagelist = dropdownmenu('div.Io6YTe.fontBodyLarge.kR99db.fdkmkc')
#     filename=filenames.split('.')[0]
#     if filename in Storagelist:
#         index = Storagelist.index(filename)
#         buttonclick("button[aria-label='更多選項']",index)
#         buttonclick("div[data-index='5']")
#         buttonclick("button.okDpye.PpaGLb")
#     filename=filenames.split('.')[0]
#     buttonclick('button[aria-label="新增清單"]')
#     element = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "input.gRsCne.azQIhc"))
#         )
#     search_box = driver.find_element(By.CSS_SELECTOR, "input.gRsCne.azQIhc")
#     search_box.clear()
#     search_box.send_keys(f"{filename}")
#     buttonclick('button.okDpye.PpaGLb')
#     time.sleep(2)
#     buttonclick('button[aria-label="菜單"]')
#     time.sleep(2)
#     buttonclick("button.T2ozWe")
    

for filename in files_only:
    filenames=filename.split('.')[0]
    Storeplace = []
    with open(success_file_path+"/"+filename, mode="r", newline="", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "–" in line:
                Storeplace.append(getstorename(line, "–"))
            elif "-" in line:
                Storeplace.append(getstorename(line, "-"))
            elif line:
                Storeplace.append(line)
    # dict1 = {}
    # for i in Storeplace:
    #     key = i.split(",")[-1].replace(" ", "")
    #     if key in dict1:
    #         dict1[key].append(i)
    #     else:
    #         dict1[key] = []
    #         dict1[key].append(i)
    for i in Storeplace:
        try:
            # 進入網站
            driver.get("https://www.google.com/maps?authuser=0")
            # 輸入搜尋資料
            search_box = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input.fontBodyMedium.searchboxinput.xiQnY")
                )
            )
            search_box.clear()
            search_box.send_keys(f"{i}")  # 修正变量名
            time.sleep(3)
            # 等待下拉選單
            if driver.find_elements(By.CSS_SELECTOR, 'div[role="grid"][aria-label="建議"]'):
                suggestion_grid = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'div[role="grid"][aria-label="建議"]')
                    )
                )

                div_elements = suggestion_grid.find_elements(
                    By.CSS_SELECTOR, "div[data-index]"
                )
                div_count = len(div_elements)

                if div_count == 1:
                    suggestion = div_elements[0]
                    suggestion.click()
                    save(div_elements,filenames)
                elif div_count > 1:
                    select = htmlComparison(driver.page_source, i)
                    suggestion = div_elements[select]
                    suggestion.click()
                    save(div_elements,filenames)
            else:
                searchbutton = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'button[aria-label="搜尋"]')
                    )
                )
                searchbutton.click()
                time.sleep(3)
                highest_similarity = 0
                if driver.find_elements(
                    By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd"
                ):
                    div_elements = driver.find_elements(
                        By.CSS_SELECTOR, "div.Nv2PK.THOPZb.CpccDe "
                    )
                    div_list = []
                    for div in div_elements:
                        # 抓取 qBF1Pd fontHeadlineSmall 的文字
                        title_element = div.find_element(
                            By.CSS_SELECTOR, "div.qBF1Pd.fontHeadlineSmall"
                        )
                        title_text = title_element.text
                        # 抓取 'Tiệm Cơm Thố Chuyên Ký' 和 'Ton That Dam'
                        address_element = div.find_elements(
                            By.CSS_SELECTOR, "div.W4Efsd span"
                        )
                        address_text = " ".join(
                            [span.text for span in address_element if span.text]
                        )
                        if "餐廳" in address_text:
                            similarity = SequenceMatcher(None, address_text, i).ratio()
                            if similarity > highest_similarity:
                                highest_similarity = similarity
                                closest_element = div
                    if closest_element:
                        time.sleep(1)
                        closest_element.click()
                        save(div_elements,filenames)
                    else:
                        print("未找到相似的店家。")
                        saveerror(i,filename)
        except Exception as ex:
            print(f"处理店名 {i} 时出错: {ex}")
            saveerror(i,filename)

    driver.quit()
