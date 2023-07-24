# pytest 库是一组工具
# 测试文件的名称必须以 test_ 打头，当你用 pytest 运行测试时，它将查找以 test_ 打头的文件。

from app.libs import httper


def test_get():
    keyword_url = "https://api.ituring.com.cn/api/Search/Books?q={}&page={}"
    result = httper.HTTP.get(keyword_url.format("docker", 1))
    print(result)
    assert result

