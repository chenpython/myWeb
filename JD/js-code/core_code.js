// 生成请求参数 pvid 的函数
function pvid() {
    var e = (new Date).getTime();
    return "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, function(t) {
        var n = (e + 16 * Math.random()) % 16 | 0;
        return e = Math.floor(e / 16),
        ("x" == t ? n : 3 & n | 8).toString(16)
    })
}
