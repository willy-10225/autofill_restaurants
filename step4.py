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

def getstorename(entry, str1):
    parts = entry.split(",")
    if len(parts) > 1:
        name_part = parts[0].split(str1)[0].strip()
        city_part = ", ".join(part.strip() for part in parts[1:])
        return f"{name_part}, {city_part}"
    return entry  # 如果没有处理，就返回原字符串


Storeplace = []
with open(r".\MergedStoreplace.csv", mode="r", newline="", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if "–" in line:
            Storeplace.append(getstorename(line, "–"))
        elif "-" in line:
            Storeplace.append(getstorename(line, "-"))
        elif line:
            Storeplace.append(line)
dict1 = {}
for i in Storeplace:
    key = i.split(",")[-1].replace(" ", "")
    if key in dict1:
        dict1[key].append(i)
    else:
        dict1[key] = []
        dict1[key].append(i)


processed_storeplaces = []
unprocessed_storeplaces = Storeplace[:]
error = []

user_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data")
chrome_options = Options()
chrome_options.add_argument(rf"user-data-dir={user_data_dir}")
chrome_options.add_argument("profile-directory=Default")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面


def buttonclick(css_selector):
    try:
        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        button.click()
    except Exception as e:
        print(f"无法点击按钮 {css_selector}: {e}")


def save(div_elements, driver):
    global processed_storeplaces, unprocessed_storeplaces
    div_elements = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.etWJQ.jym1ob"))
    )

    if len(div_elements) > 1:
        button = div_elements[1].find_element(By.CSS_SELECTOR, "button.g88MCb.S9kvJb")
        aria_label_value = button.get_attribute("aria-label")
        if aria_label_value == "儲存":
            button.click()
            suggestion_grid = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[aria-label="儲存至清單中"]')
                )
            )
            label_element = suggestion_grid.find_element(
                By.XPATH, './/div[contains(text(), "必比登")]'
            )
            outer_div = label_element.find_element(
                By.XPATH,
                './ancestor::div[@aria-checked="false" and @role="menuitemradio"]',
            )
            outer_div.click()
            WebDriverWait(driver, 30).until(
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

driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
for i in Storeplace:
    try:
        # 進入網站
        driver.get("https://www.google.com/maps?authuser=0")
        # 輸入搜尋資料
        search_box = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input.fontBodyMedium.searchboxinput.xiQnY")
            )
        )
        search_box.clear()
        search_box.send_keys(f"{i}")  # 修正变量名
        time.sleep(3)
        # 等待下拉選單
        if driver.find_elements(By.CSS_SELECTOR, 'div[role="grid"][aria-label="建議"]'):
            suggestion_grid = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[role="grid"][aria-label="建議"]')
                )
            )

            div_elements = suggestion_grid.find_elements(By.CSS_SELECTOR, "div[data-index]")
            div_count = len(div_elements)

            if div_count == 1:
                suggestion = div_elements[0]
                suggestion.click()
                save(div_elements, driver)
            elif div_count > 1:
                select = htmlComparison(driver.page_source, i)
                suggestion = div_elements[select]
                suggestion.click()
                save(div_elements, driver)
        else:
            searchbutton = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'button[aria-label="搜尋"]'))
            )
            searchbutton.click()
            time.sleep(3)
            highest_similarity=0
            if driver.find_elements(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd'):
                div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb.CpccDe ')
                div_list=[]
                for div in div_elements:
                    # 抓取 qBF1Pd fontHeadlineSmall 的文字
                    title_element = div.find_element(By.CSS_SELECTOR, 'div.qBF1Pd.fontHeadlineSmall')
                    title_text = title_element.text
                    # 抓取 'Tiệm Cơm Thố Chuyên Ký' 和 'Ton That Dam'
                    address_element = div.find_elements(By.CSS_SELECTOR, 'div.W4Efsd span')
                    address_text = " ".join([span.text for span in address_element if span.text])
                    if "餐廳" in address_text:
                        similarity = SequenceMatcher(None, address_text, i).ratio()
                        if similarity > highest_similarity:
                            highest_similarity = similarity
                            closest_element = div
                if closest_element:
                    time.sleep(1)
                    closest_element.click()
                    save(div_elements, driver)
                else:
                    print("未找到相似的店家。")    
                    error.append(i)
    except Exception as ex: 
        print(f"处理店名 {i} 时出错: {ex}")
        error.append(i)
    processed_storeplaces.append(i)
    unprocessed_storeplaces.remove(i)

driver.quit()


with open(r".\ProcessedStoreplace.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for item in processed_storeplaces:
        writer.writerow([item])

with open(
    r".\UnprocessedStoreplace.csv", mode="w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)
    for item in unprocessed_storeplaces:
        writer.writerow([item])

with open(r".\ErrorStoreplace.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for item in error:
        writer.writerow([item])
