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

""" 类的使用  self.__name 属性名或方法名前加 __ 标识私有
class Student:
    def __init__(self, name, age):
        self.__name = name;
        self.__age = age;
    def study(self, course_name):
        print("%s 正在学习 %s" % (self.__name, course_name))

if __name__ == "__main__":
    s = Student("李明", 2);
    s.study("英语")
    ss = Student("丽丽", 5)
    ss.study("英语")

"""

"""
class Test:
    def __init__(self, foo):
        self._foo = foo
    def _bar(self):
        print(self._foo)
        print("__bar")

def main():
    t = Test("cc")

if __name__ == "__main__":
    main()
"""

""" 时钟
from time import sleep

class Clock:
    def __init__(self , hour = 0, minute = 0, second = 0):
        self._hour = hour;
        self._minute = minute
        self._second = second
    def run(self):
        self._second += 1
        if self._second == 60:
            self._second = 0
            self._minute += 1
            if self._minute == 60:
                self._minute = 0
                self._hour += 1
                if self._hour == 24:
                    self._hour = 0

    def show(self):
        return '%02d:%02d:%02d' % (self._hour, self._minute, self._second)

def main():
    clock = Clock(23,59,58)
    while True:
        print(clock.show())
        sleep(1)
        clock.run()

if __name__ == "__main__":
    main()

"""

"""
import tkinter
import tkinter.messagebox

def main():
    flag = True

    # 修改标签上的文字
    def change_label_text():
        nonlocal flag
        flag = not flag
        color, msg = ('red', 'Hello, world!')\
            if flag else ('blue', 'Goodbye, world!')
        label.config(text=msg, fg=color)

    # 确认退出
    def confirm_to_quit():
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
            top.quit()

    # 创建顶层窗口
    top = tkinter.Tk()
    # 设置窗口大小
    top.geometry('240x160')
    # 设置窗口标题
    top.title('小游戏')
    # 创建标签对象并添加到顶层窗口
    label = tkinter.Label(top, text='Hello, world!', font='Arial -32', fg='red')
    label.pack(expand=1)
    # 创建一个装按钮的容器
    panel = tkinter.Frame(top)
    # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定事件回调函数
    button1 = tkinter.Button(panel, text='修改', command=change_label_text)
    button1.pack(side='left')
    button2 = tkinter.Button(panel, text='退出', command=confirm_to_quit)
    button2.pack(side='right')
    panel.pack(side='bottom')
    # 开启主事件循环
    tkinter.mainloop()

if __name__ == '__main__':
    main()

"""
import logging
from logging import handlers

class Logger(object):
    #  日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)     # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))   # 设置日志级别
        sh = logging.StreamHandler()    # 往屏幕上输出
        sh.setFormatter(format_str)     # 设置屏幕上显示的格式
        # 往文件里写入 指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        #  实例化TimedRotatingFileHandler
        #  interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)     # 设置文件里写入的格式
        self.logger.addHandler(sh)      # 把对象加到logger里
        self.logger.addHandler(th)


if __name__ == '__main__':
    log = Logger('all.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')

