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
    texts = [
            "xxx",
             ]
    threshold = 1
    nest = False
    # 调用 API
    results = call_cptagger_api(texts, threshold, nest)
    for result in results:
        print('字典匹配结果：', result["dict_result"])
        print('机器学习匹配结果：', result["ml_result"])
        print('集成匹配结果：', result["final_result"])
