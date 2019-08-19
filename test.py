'''
username = input('请输入用户名:')
password = input('请输入密码:')
if username == 'admin' and password == 'admin':
    print('身份认证成功')
else:
    print('身份认证失败')
'''


# value  = float(input("请输入长度:"))
# unit = input("请输入长度")
# if unit == 'in' or unit == '英寸':
#     print(2111)
# elif unit == 'cm' or unit == '厘米':
#     print(22222)
# else:
#     print(3333)

"""
def foo():
    global a //全局变量使用
    a = 200;

if __name__ == "__main__":
    a = 100 //a为全局变量
    foo()
    print(a)
"""

""" 简单字符串使用
def main():
    str1 = 'hello world'
    print(len(str1))
    print(str1.capitalize())
    print(str1.upper())
    print(str1.find('or'))
    print(str1[0:5])

if __name__ == "__main__":
    main()

"""

""" 列表使用
def main():
    list1 = [1, 2, 3, 4, 5]
    print(list1)
    list2 = ['hello'] * 5
    print(list2)
    list1.append('cccc');
    list1.insert(0, '22222')
    list1.remove('22222');
    print(list1)

if __name__ == "__main__":
    main()
"""
"""
def main():
    fruits = ['grape', 'apple', 'strawberry', 'waxberry']
    fruits += ['pitaya', 'pear', 'mango']
    # 循环遍历列表元素
    for fruit in fruits:
        print(fruit.title(), end=' ')
    print()
    # 列表切片
    fruits2 = fruits[1:4]
    print(fruits2)
    # fruit3 = fruits  # 没有复制列表只创建了新的引用
    # 可以通过完整切片操作来复制列表
    fruits3 = fruits[:]
    print(fruits3)
    fruits4 = fruits[-3:-1]
    print(fruits4)
    # 可以通过反向切片操作来获得倒转后的列表的拷贝
    fruits5 = fruits[::-1]
    print(fruits5)

if __name__ == '__main__':
    main()

# 列表   [1, 2, 3, 4]
# 元组   (1, 2 ,3 )
# 集合   {1, 2 ,3 ,4 }
# 字典   {"name":"黎明", "age":18}
"""

""" 跑马灯
import os
import time

def main():
    content  = "北京欢迎您为你开天辟地 ......."
    while True:
        os.system('cls')
        print(content)
        time.sleep(0.2)
        content = content[1:]  + content[0:1]

if __name__ == "__main__":
    main()
"""

""" 生成随机验证码
import random

def generate_code(code_len = 4):
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyz';
    last_pos = len(all_chars) - 1;
    code = ''
    for _ in range(code_len):
        index = random.randint(0,last_pos);
        code += all_chars[index];
    return code

if __name__ == "__main__":
    result = generate_code(4)
    print(result)

"""
