import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from htmlComparison import htmlComparison
from setchrome import get_chrome_driver

success_file_path = "./step3/3-2"
error_file_path = "./step3/error"

sccuess = False
os.makedirs(error_file_path, exist_ok=True)


def saveerror(item: str, filename: str, sccuess: bool):
    global error_file_path
    if not sccuess:
        with open(
            os.path.join(error_file_path, filename),
            mode="a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)
            writer.writerow([item])


# 获取文件夹中的所有文件和文件夹
all_files = os.listdir(success_file_path)

files_only = [
    file for file in all_files if os.path.isfile(os.path.join(success_file_path, file))
]

user_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data")
driver = get_chrome_driver()


def buttonclick(css_selector, index=0):
    global driver
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


def getstorename(line, delimiter):
    # 确保返回值是字符串
    result = line.split(delimiter)[0]
    return str(result)


def dropdownmenu(html: str):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, html))
    )
    div_elements = driver.find_elements(By.CSS_SELECTOR, html)
    Storagelist = [div.text for div in div_elements]
    return Storagelist


def googlemapinput(search):
    driver.get("https://www.google.com/maps?authuser=0")
    # 輸入搜尋資料
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input.fontBodyMedium.searchboxinput.xiQnY")
        )
    )
    search_box.clear()
    search_box.send_keys(f"{search}")  # 修正变量名
    time.sleep(3)


def save(search_box, roop):
    global driver, sccuess
    try:
        driver.find_element(By.CSS_SELECTOR, ".F7nice")
        div_elements = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.etWJQ.jym1ob"))
        )

        if len(div_elements) > 1:
            savebutton = div_elements[1].find_element(
                By.CSS_SELECTOR, "button.g88MCb.S9kvJb"
            )
            aria_label_value = savebutton.get_attribute("aria-label")

            if aria_label_value == "儲存":
                savebutton.click()
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
                sccuess = True
                print(f"{roop} 已儲存")

            else:
                sccuess = True
                print(f"{roop} 已儲存 (未点击保存按钮)")

        else:
            print("没有足够的 div 元素可供选择")
    except Exception as ex:
        print(ex)
    time.sleep(3)


def dropdownseach(str1):
    try:
        googlemapinput(str1)
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
                save(filenames, str1)
            elif div_count > 1:
                select = htmlComparison(driver.page_source, str1)
                suggestion = div_elements[select]
                suggestion.click()
                save(filenames, str1)
    except Exception as ex:
        print(ex)


driver.get("https://www.google.com/maps?authuser=0")
# time.sleep(2)
# buttonclick('button[aria-label="菜單"]')
# time.sleep(2)
# buttonclick("button.T2ozWe")
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
    filenames = filename.split(".")[0]
    VSCplace = []
    with open(
        success_file_path + "/" + filename, mode="r", newline="", encoding="utf-8"
    ) as file:
        for line in file:
            line = str(line).strip()
            if "–" in line:
                VSCplace.append(getstorename(line, "–"))
            elif "-" in line:
                VSCplace.append(getstorename(line, "-"))
            elif line:
                VSCplace.append(line)
    # dict1 = {}
    # for i in VSCplace:
    #     key = i.split(",")[-1].replace(" ", "")
    #     if key in dict1:
    #         dict1[key].append(i)
    #     else:
    #         dict1[key] = []
    #         dict1[key].append(i)
    for i in VSCplace:

        googlemapinput(i)
        searchbutton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'button[aria-label="搜尋"]')
            )
        )
        searchbutton.click()
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.g88MCb.S9kvJb")
                )
            )
            if driver.find_elements(By.CSS_SELECTOR, "div.F7nice"):
                save(filenames, i)
            else:
                dropdownseach(i)
        except Exception as ex:
            dropdownseach(i)
        saveerror(i, filename, sccuess)
driver.quit()
