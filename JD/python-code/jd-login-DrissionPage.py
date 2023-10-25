import os

from DrissionPage import ChromiumOptions, ChromiumPage, WebPage

# from DrissionPage.easy_set import set_paths
# 配置已保存到文件：/home/feng/workspace/myWeb/.venv/lib/python3.10/site-packages/DrissionPage/configs/configs.ini
# set_paths(browser_path='/usr/bin/google-chrome-stable')
# 弹出浏览器窗口，启动浏览器：google-chrome-stable  --remote-debugging-port=9222，通过代码接管当前浏览器
base_dir = os.path.dirname(os.path.dirname(__file__))
# co = ChromiumOptions()
# co.set_paths(local_port=9222)   # 弹出浏览器窗口
# page = ChromiumPage(addr_driver_opts=co)
init_page = WebPage('d')
url = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"
# page.get(url)
tab_id = init_page.new_tab(url) # 会导致截图、或者获取html内容只能拿到默认打开的无效标签页
print('进入页面')
page = init_page.get_tab(tab_id)
try:
    # page.wait.load_start()
    page.wait.ele_display('#loginname', timeout=60)
    print('等待{}页面加载完成'.format(tab_id))
    bf_content = page.html
    # 文档编码模式获取：进入浏览器控制台，输入 document.charset
    # 浏览器打开文档乱码，将文档中的 head标签下 <meta charset="GBK"> 的 编码格式改为 utf-8 
    with open(os.path.join(base_dir, 'htmls/bf_content.html'), 'w', encoding='utf-8') as f:
        f.write(bf_content)
    print('保存登录之前页面内容')
    # page.get_screenshot(path=os.path.join(base_dir, 'images/screen_shot.png'), full_page=True)
    print('登录之前')
    ele = page.ele('#loginname', timeout=30)
    ele.input('JDtest123456888')
    page.ele('#nloginpwd', timeout=30).input('250Kuai4Mao1')
    page.ele('#loginsubmit',  timeout=30).click()
    page.wait.load_start()
    af_content = page.html
    with open(os.path.join(base_dir, 'htmls/af_content.html'), 'w',encoding='utf-8') as f:
        f.write(af_content)
    print('登录之后')
except Exception as e:
    print('操作页面失败，错误：{}'.format(e))
finally:
    init_page.close_tabs(tab_id)   # 关闭当前页面

# page.quit()
print('end')

