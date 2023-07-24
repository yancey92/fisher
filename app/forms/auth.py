from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models.user import User


# EmailForm 继承 Form
# 下面所有需要验证 email 的，也都可以继承 EmailForm 这个类，这样下面的所有类里面就不用都写 email 的校验了
class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64, message="电子邮箱不符合规范")])


# 继承 EmailForm，同时也间接继承了 Form
class RegisterForm(EmailForm):
    nickname = StringField(
        "昵称", validators=[DataRequired(), Length(2, 10, message="昵称至少需要两个字符，最多10个字符")]
    )
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(message="密码不能为空"),
            Length(6, 20, message="密码需要6到20个字符"),
        ],
    )

    # 自定义验证器: wtforms.validators 组件约定 validate_xxx() 会额外验证 xxx 字段的合法性
    # 如果验证失败，需要抛出指定类型的 wtforms.validators.ValidationError 异常
    # 下面的 validate_email 会和 上面的 email 验证器一起验证，上面的 email 验证通过后会走 validate_email
    def validate_email(self, field):
        if User.query.filter_by(email=field.data, enable_status=1).first():
            raise ValidationError("电子邮件已被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data, enable_status=1).first():
            raise ValidationError("昵称已存在")


# 继承 EmailForm，同时也间接继承了 Form
class LoginForm(EmailForm):
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(message="密码不能为空"),
            Length(6, 20, message="密码需要6到20个字符"),
        ],
    )


class ResetPasswordForm(Form):
    password1 = PasswordField(
        "新密码",
        validators=[
            DataRequired(),
            Length(6, 20, message="密码长度至少需要在6到20个字符之间"),
            EqualTo("password2", message="两次输入的密码不相同"),
        ],
    )
    password2 = PasswordField("确认新密码", validators=[DataRequired(), Length(6, 20)])
