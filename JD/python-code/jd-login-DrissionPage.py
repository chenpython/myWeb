import time

from DrissionPage import ChromiumPage

# ubuntu启动chrome命令：google-chrome-stable
# from DrissionPage.easy_set import set_paths
# 配置已保存到文件：/home/feng/workspace/myWeb/.venv/lib/python3.10/site-packages/DrissionPage/configs/configs.ini
# set_paths(browser_path='/usr/bin/google-chrome-stable')

page = ChromiumPage()
page.get('https://www.baidu.com/')


# # 创建页面对象，并启动或接管浏览器
# page = ChromiumPage()
# # 跳转到登录页面
# page.get('https://gitee.com/login')

# # 定位到账号文本框，获取文本框元素
# ele = page.ele('#user_login')
# # 输入对文本框输入账号
# ele.input('您的账号')
# # 定位到密码文本框并输入密码
# page.ele('#user_password').input('您的密码')
# # 点击登录按钮
# page.ele('@value=登 录').click()
print('end')
