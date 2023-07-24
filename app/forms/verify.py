# 接口校验模块

# wtforms 内置了很多校验函数，我们使用该库来做一些校验
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(Form):
    """ 使用验证器验证 search() function"""

    # StringField 验证Str类型
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    # IntegerField 验证整形
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
