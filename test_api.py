# -*- coding: UTF-8 -*-
import requests


def call_cptagger_api(texts, threshold=None, nest=None):
    url = "[API_Endpoint]/cptagger"
    data = {
        "texts": texts,
        "threshold": threshold,
        "nest": nest
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # 输出结果
            results = response.json()
            return results
        else:
            print("Failed to call API:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", str(e))


# 示例调用
if __name__ == "__main__":
    texts = ["xxx", ]
    threshold = 0.95
    nest = False
    # 调用 API
    results = call_cptagger_api(texts, threshold, nest)
    for i, result in enumerate(results):
        print(f'待识别文本{i}：', texts[i])
        for j, res in enumerate(result):
            print(f'\t文本片段{i}/{j}：', res["text"])
            print('\t\t字典匹配结果：', res["dict_result"])
            print('\t\t机器学习匹配结果：', res["ml_result"])
            print('\t\t集成匹配结果：', res["final_result"])
