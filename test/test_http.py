import http.client

try:
    # https connection
    conn = http.client.HTTPSConnection("example.com")
    conn.request("GET", "/")
    response = conn.getresponse()
    if response.status != 200:
        # 如果响应的状态码不是200，我们抛出一个HTTPException异常。
        raise http.client.HTTPException(
            f"HTTP Exception: {response.status} - {response.reason}"
        )
    else:
        print("Request successful")
except http.client.HTTPException as e:
    print("HTTP Exception:", e)
except Exception as e:
    print("Error:", e)
