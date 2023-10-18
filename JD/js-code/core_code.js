// 生成请求参数 pvid 的函数
function pvid() {
    var e = (new Date).getTime();
    return "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, function(t) {
        var n = (e + 16 * Math.random()) % 16 | 0;
        return e = Math.floor(e / 16),
        ("x" == t ? n : 3 & n | 8).toString(16)
    })
}


var jdtRiskCookieManager = {
    getCookie: function(l) {
        try {
            l += "=";
            for (var m = document.cookie.split(";"), n = 0; n < m.length; n++) {
                var g = m[n].trim();
                if (0 == g.indexOf(l))
                    return g.substring(l.length, g.length)
            }
        } catch (f) {}
        return ""
    } // 从 cookie 中截取 key 为3AB9D23F7A4B3CSS 的值
};


function load(m, n, g) {
    g = g || function(d) {
        return !!d
    }
    ;
    var f = null;

    try {
        if (f = jdtRiskCookieManager.getCookie(m),
        g(f))
            return f
    } catch (d) {}
    return f
}

console.log(pvid())
