

模型层

python 提供了 ORM 库: sqlalchemy，用于通过 model 自动创建数据库表，以及操作数据库数据。

flask 提供了 flask-sqlalchemy 包，方便我们操作 sqlalchemy，进而操作数据库。当然，我们也
可以不用 flask-sqlalchemy，完全通过 sqlalchemy 做 orm 以及数据库的 crud (正删改查)。

pipenv install flask-sqlalchemy
pipenv graph 

