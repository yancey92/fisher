from jinja2 import Template

template = Template(r"""
{% with x = 5 %}
    {{ x }}  <!-- 输出: 5 -->
{% endwith %}

{{ x }}  <!-- 输出: 变量 x 未定义 -->
""")

# my_variable 没有被定义时
output = template.render(my_variable="a")
print(output)  # 输出：3

