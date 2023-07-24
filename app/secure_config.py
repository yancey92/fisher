# 配置文件中的 key 必须是大写的
# 该配置文件，存放一些敏感信息

DATABASE_NAME = "fisher"
DRIVER = "cymysql"  # 需要下载 cymysql 驱动： pipenv install cymysql

# 这个字段是不能随意更改的，因为 flask_sqlalchemy.SQLAlchemy.init_app() 方法中写死了这个 uri
SQLALCHEMY_DATABASE_URI = f"mysql+{DRIVER}://root:123456@localhost:3306/{DATABASE_NAME}"

SECRET_KEY = "1qaz2wsx3edc"

# email配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = "xxxxxx@qq.com"
# QQ邮箱->设置->账户->[POP3...]->生成授权码->发送短信->获取授权码
MAIL_PASSWORD = "xxxxxx"
