import os

from DrissionPage import ChromiumOptions, ChromiumPage

# from DrissionPage.easy_set import set_paths
# 配置已保存到文件：/home/feng/workspace/myWeb/.venv/lib/python3.10/site-packages/DrissionPage/configs/configs.ini
# set_paths(browser_path='/usr/bin/google-chrome-stable')
# 弹出浏览器窗口，启动浏览器：google-chrome-stable  --remote-debugging-port=9222，通过代码接管当前浏览器
base_dir = os.path.dirname(os.path.dirname(__file__))


co = ChromiumOptions()
co.set_paths(local_port=9222)   # 弹出浏览器窗口
page = ChromiumPage(addr_driver_opts=co)

url = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"

page.get(url)
page.wait.load_start()
bf_content = page.html
with open(os.path.join(base_dir, 'htmls/bf_content.html'), 'w') as f:
    f.write(bf_content)
print('登录之前')
ele = page.ele('#loginname')
ele.input('jlsl123456')
page.ele('#nloginpwd').input('250Kuai4Mao1')
page.ele('@value=item item-fore5').click()
page.wait.load_start()
af_content = page.html
with open(os.path.join(base_dir, 'htmls/af_content.html'), 'w') as f:
    f.write(af_content)
print('登录之后')
page.close_tabs()
# page.quit()
print('end')

