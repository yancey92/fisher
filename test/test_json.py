"""
 示例：对象转 json 格式字符串
"""
import json


class People:
    def __init__(self, name, age, pet):
        self.name = name
        self.age = age
        self.pet = pet


class Pet:
    def __init__(self, pet_type, pet_name):
        self.pet_type = pet_type
        self.pet_name = pet_name


pet = Pet("Cat", "Lili")
people = People("Xiao ming", 12, pet)

json_str = json.dumps(people, default=lambda obj: obj.__dict__)

# 输出：{"name": "Xiao ming", "age": 12, "pet": {"pet_type": "Cat", "pet_name": "Lili"}}
print(json_str)
