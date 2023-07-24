import requests


class HTTP:

    # 通过 http get 方法，返回json对象 或者 文本对象
    @staticmethod
    def get(url, return_json=True):
        response = requests.get(url)
        if response.status_code != 200:
            return {} if return_json else ""

        return response.json() if return_json else response.text
