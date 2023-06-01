import requests

# 示例代码
# jscode = """
# (function(){
#     console.log("test")
#     return "执行成功"
# })()
# """
# 控制台执行
# console: var demo = new Hlclient("ws://127.0.0.1:12080/ws?group=zzz&name=hlg");

path = '/mnt/c/Users/PICO/Documents/node.js/cde_debug/d.FxJzG50F.6152bb9.js'
jscode = open(path, 'r').read()



url = "http://192.168.2.131:12080/execjs"
data = {
    "group": "zzz",
    "name": "hlg",
    "jscode":jscode
}
res = requests.post(url, data=data)
print(res.text)

