import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk # 导入ttk模块，因为下拉菜单控件在ttk中
import operatorDb

wuya = tkinter.Tk()
wuya.title("wuya")
wuya.geometry("300x200+10+20")


# 创建下拉菜单
cmb = ttk.Combobox(wuya)
cmb.pack()
# 设置下拉菜单中的值
cmb['value'] = ('上海','北京','天津','广州')

# 设置默认值，即默认下拉框中的内容
cmb.current(2)
# 默认值中的内容为索引，从0开始

# 执行函数
def func(event):
    text.insert('insert',cmb.get()+"\n")
cmb.bind("<<ComboboxSelected>>",func)

def link_button():
    text.insert('insert',cmb.get()+"\n")

tk.Button(wuya,text='连接线缆',command=link_button,width=8,background='blue').place(x=20,y=16)

text = tkinter.Text(wuya)
text.pack()
wuya.mainloop()