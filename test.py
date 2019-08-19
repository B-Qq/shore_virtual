username = input('请输入用户名:')
password = input('请输入密码:')
if username == 'admin' and password == 'admin':
    print('身份认证成功')
else:
    print('身份认证失败')
