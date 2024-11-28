import concurrent.futures
import csv
import os
import random
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# 定义函数用于处理单个 URL，增加重试机制
def fetch_data(url):
    try:
        session = requests.Session()
        # 设置重试策略
        retry = Retry(
            total=5,  # 重试次数
            backoff_factor=1,  # 每次重试之间的等待时间指数增加（1秒，2秒，4秒等）
            status_forcelist=[429, 500, 502, 503, 504],  # 遇到这些状态码时重试
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        response = session.get(url)
        if response.status_code == 200:
            # 使用 BeautifulSoup 解析 HTML 内容
            soup = BeautifulSoup(response.content, "html.parser")
            Storename = soup.find("h1", class_="data-sheet__title").text
            placename = soup.find("div", class_="data-sheet__block--text").text
            placename = " ".join(placename.split())
            return [Storename, placename]
        else:
            print(f"请求失败: {response.status_code}, URL: {url}")
            return None
    except Exception as e:
        print(f"请求 {url} 失败: {e}")
        return None


# 添加请求延迟
def delayed_request(url):
    time.sleep(random.uniform(0.5, 2.0))  # 设置随机延迟，0.5到2秒
    return fetch_data(url)


# 并发处理
# 并发处理的函数，返回失败的 URL 列表
def process_urls(url_list):
    Store = []
    failed_urls = []  # 用于存储失败的 URL
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # max_workers 设置线程数量，建议根据网络带宽和目标网站响应速度调整
        futures = {executor.submit(delayed_request, url): url for url in url_list}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                Store.append(result)
            else:
                failed_urls.append(futures[future])  # 记录失败的 URL
            print(f"已处理: {len(Store)} 个")
    return Store, failed_urls


folder_path = r".\step1"

# 获取文件夹中的所有文件和文件夹
all_files = os.listdir(folder_path)
files_only = [
    file for file in all_files if os.path.isfile(os.path.join(folder_path, file))
]

# 读取 CSV 文件并将 URL 存储到 orlist 列表中
for filename in files_only:
    orlist = []
    with open(f"./step1/{filename}", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            orlist.extend(row)  # 将每一行的数据添加到 orlist 中

    all_store = []  # 用于存储所有成功处理的数据
    failed_urls = orlist  # 开始时将所有 URL 作为待处理列表
    count = 0
    while count != len(failed_urls):
        count = len(failed_urls)
        # 处理 URL
        store, failed_urls = process_urls(failed_urls)
        all_store.extend(store)  # 累积成功的数据

        if failed_urls:
            print(f"还有 {len(failed_urls)} 个请求失败，等待 300 秒后重试...")
            time.sleep(300)  # 等待 300 秒后重试
        else:
            break

    # 定义文件路径
    success_file_path = rf".\step2\success\{filename}"
    error_file_path = rf".\step2\error\{filename}"

    # 提取文件夹路径并确保目录存在
    success_folder = os.path.dirname(success_file_path)
    error_folder = os.path.dirname(error_file_path)

    # 创建文件夹（如果不存在）
    os.makedirs(success_folder, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)

    # 将结果写入 CSV 文件
    with open(success_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(all_store)

    # 记录最终失败的 URL，方便后续重试
    if failed_urls:
        with open(error_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for url in failed_urls:
                writer.writerow([url])

    print(f"处理完成，共成功处理 {len(all_store)} 个，失败 {len(failed_urls)} 个")
