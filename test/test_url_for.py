from flask import Flask, url_for

app = Flask(__name__)


# 通常，endpoint 与视图函数同名
@app.route('/', endpoint="index")
def index():
    pass


with app.test_request_context():
    print(url_for('index'))  # 输出：/
