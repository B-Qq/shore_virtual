'''
username = input('请输入用户名:')
password = input('请输入密码:')
if username == 'admin' and password == 'admin':
    print('身份认证成功')
else:
    print('身份认证失败')
'''


value  = float(input("请输入长度:"))
unit = input("请输入长度")
if unit == 'in' or unit == '英寸':
    print(2111)
elif unit == 'cm' or unit == '厘米':
    print(22222)
else:
    print(3333)