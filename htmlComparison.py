from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup


def htmlComparison(html, target):
    soup = BeautifulSoup(html, "html.parser")
    # 目标字符串
    # 查找所有具有特定 class 的 span 元素
    spans = soup.find_all("span", class_=["cGyruf", "EmLCAe", "fontBodyMedium"])

    # 初始化相似度最高的数据
    max_similarity = 0
    best_match_index = -1

    # 相似度比较函数
    def compare_strings(a, b):
        return SequenceMatcher(None, a, b).ratio()

    # 遍历所有找到的 span 标签
    for span in spans:
        # 查找父元素，获取 data-index 值
        parent = span.find_parent("div", attrs={"data-index": True})
        if parent:
            data_index = parent["data-index"]

            # 获取 span 的文本内容并进行比较
            span_text = span.get_text(strip=True)
            similarity = compare_strings(span_text, target)

            # 如果当前相似度更高，则更新最优匹配
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_index = data_index
    return int(best_match_index)
