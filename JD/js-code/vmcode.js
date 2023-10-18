var _riskFpMode = _riskFpMode || "strict";
"fast" != _riskFpMode && (_riskFpMode = "strict");
"function" != typeof String.prototype.startsWith && (String.prototype.startsWith = function(l) {
    return this.slice(0, l.length) === l
}
);
"function" != typeof String.prototype.endsWith && (String.prototype.endsWith = function(l) {
    return -1 !== this.indexOf(l, this.length - l.length)
}
);
var jdtRiskContext = {
    d: !1,
    canvas_fp_md5: "",
    isJsTokenFinished: !1,
    version: "3.1.1.0",
    deviceInfo: {
        jsToken: "",
        eid: "",
        fp: ""
    },
    isReady: function() {
        return this.isJsTokenFinished
    }
}
  , collectConfig = {
    fp: {
        language: "language",
        userAgent: "userAgent",
        colorDepth: "colorDepth",
        screenResolution: "screenResolution",
        timezoneOffset: "timezoneOffset",
        sessionStorage: "sessionStorage",
        localStorage: "localStorage",
        indexedDb: "indexedDb",
        addBehavior: "addBehavior",
        openDatabase: "openDatabase",
        cpuClass: "cpuClass",
        platform: "platform",
        hardwareConcurrency: "hardwareConcurrency",
        audioKey: "audioKey",
        doNotTrack: "doNotTrack",
        plugins: "plugins",
        canvas: "canvas",
        webgl: "webgl"
    },
    env: {
        color: "color",
        canvas: "canvas",
        browserMode: "browserMode",
        fonts: "fonts",
        feature: "feature",
        plugins: "plugins",
        screen: "screen",
        position: "position",
        storeCheck: "storeCheck"
    },
    store: {
        giaDKey: "_gia_d",
        canvasFpKey: "CA1AN5BV0CA8DS2EPC",
        ldeKey: "GIA_LDE_MAP_KEY",
        strict: {
            jsTokenKey: "3AB9D23F7A4B3CSS",
            fpKey: "PCA9D23F7A4B3CSS",
            fpTsKey: "PCTSD23F7A4B3CSS",
            eidKey: "3AB9D23F7A4B3C9B"
        },
        fast: {
            jsTokenKey: "3AB9D23F7A4B3CFF",
            fpKey: "PCA9D23F7A4B3CFF",
            fpTsKey: "PCTSD23F7A4B3CFF",
            eidKey: "3AB9D23F7A4B3CFF"
        }
    },
    getEnvExcludeOptions: function(l) {
        if ("strict" == l)
            return {};
        if ("fast" == l)
            return l = {},
            l[this.env.color] = !0,
            l[this.env.fonts] = !0,
            l
    },
    getFpExcludeOptions: function(l) {
        if ("strict" == l)
            return {};
        if ("fast" == l)
            return l = {},
            l[this.fp.webgl] = !0,
            l[this.fp.plugins] = !0,
            l[this.fp.userAgent] = !0,
            l[this.fp.doNotTrack] = !0,
            l
    }
}
  , jdtRiskUtil = function(l) {
    var m = "https:" == document.location.protocol ? "https://" : "http://"
      , n = window.__fp_domain || "gia.jd.com"
      , g = ""
      , f = ""
      , d = "";
    (function() {
        var a = document.location.href.toString();
        try {
            var b = /^https?:\/\/(?:\w+\.)*?(\w*\.(?:com\.cn|cn|com|net|id))[\\\/]*/.exec(a);
            f = b && 1 < b.length ? b[1] : document.domain.split(".").slice(-2).join(".");
            var e = a.indexOf("?");
            0 < e && (g = a.substring(e + 1),
            500 < g.length && (g = g.substring(0, 499)),
            a = a.substring(0, e));
            d = a.substring(m.length)
        } catch (c) {}
    }
    )();
    l.getCurrentPageUrl = function() {
        return d
    }
    ;
    l.getCurrentPageProtocol = function() {
        return m
    }
    ;
    l.getCurrentRootDomain = function() {
        return f
    }
    ;
    l.getFpServerDomain = function() {
        return n
    }
    ;
    l.getUrlQueryStr = function() {
        return g
    }
    ;
    l.getBizId = function() {
        return "undefined" == typeof bp_bizid ? "" : bp_bizid
    }
    ;
    l.createWorker = function() {
        if (window.Worker && !l.worker) {
            try {
                var a = new Blob(["onmessage = function (event) {\n    var data = JSON.parse(event.data);\n    try {\n        var httpRequest;\n        try {\n            httpRequest = new XMLHttpRequest();\n        } catch (h) {}\n        if (!httpRequest)\n            try {\n                httpRequest = new (window['ActiveXObject'])('Microsoft.XMLHTTP')\n            } catch (l) {}\n        if (!httpRequest)\n            try {\n                httpRequest = new (window['ActiveXObject'])('Msxml2.XMLHTTP')\n            } catch (r) {}\n        if (!httpRequest)\n            try {\n                httpRequest = new (window['ActiveXObject'])('Msxml3.XMLHTTP')\n            } catch (n) {}\n\n        if(data){\n            httpRequest['open']('POST', data.url, false);\n            httpRequest['setRequestHeader']('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8');\n            httpRequest['onreadystatechange'] = function () {\n                if (4 === httpRequest['readyState'] && 200 === httpRequest['status']) {\n                    postMessage(httpRequest.responseText);\n                }\n            };\n            httpRequest['send'](data.data);\n        }\n\n    }catch (e){console.error(e);}\n};"],{
                    type: "application/javascript"
                })
            } catch (b) {
                window.BlobBuilder = window.BlobBuilder || window.WebKitBlobBuilder || window.MozBlobBuilder,
                a = new BlobBuilder,
                a.append("onmessage = function (event) {\n    var data = JSON.parse(event.data);\n    try {\n        var httpRequest;\n        try {\n            httpRequest = new XMLHttpRequest();\n        } catch (h) {}\n        if (!httpRequest)\n            try {\n                httpRequest = new (window['ActiveXObject'])('Microsoft.XMLHTTP')\n            } catch (l) {}\n        if (!httpRequest)\n            try {\n                httpRequest = new (window['ActiveXObject'])('Msxml2.XMLHTTP')\n            } catch (r) {}\n        if (!httpRequest)\n            try {\n                httpRequest = new (window['ActiveXObject'])('Msxml3.XMLHTTP')\n            } catch (n) {}\n\n        if(data){\n            httpRequest['open']('POST', data.url, false);\n            httpRequest['setRequestHeader']('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8');\n            httpRequest['onreadystatechange'] = function () {\n                if (4 === httpRequest['readyState'] && 200 === httpRequest['status']) {\n                    postMessage(httpRequest.responseText);\n                }\n            };\n            httpRequest['send'](data.data);\n        }\n\n    }catch (e){console.error(e);}\n};"),
                a = a.getBlob()
            }
            try {
                l.worker = new Worker(URL.createObjectURL(a))
            } catch (b) {}
        }
    }
    ;
    l.reportWorker = function(a, b, e, c) {
        try {
            l.worker && (this.worker.postMessage(JSON.stringify({
                url: a,
                data: b,
                success: !1,
                async: !1
            })),
            this.worker.onmessage = function(h) {}
            )
        } catch (h) {}
    }
    ;
    l.compareVersion = function(a, b) {
        try {
            if (a === b)
                return 0;
            var e = a.split(".");
            var c = b.split(".");
            for (a = 0; a < e.length; a++) {
                var h = parseInt(e[a]);
                if (!c[a])
                    return 1;
                var k = parseInt(c[a]);
                if (h < k)
                    break;
                if (h > k)
                    return 1
            }
        } catch (p) {}
        return -1
    }
    ;
    l.obtainPin = function(a) {
        var b = "";
        "string" === typeof jd_jr_td_risk_pin && 1 == a ? b = jd_jr_td_risk_pin : "string" === typeof pin ? b = pin : "object" === typeof pin && "string" === typeof jd_jr_td_risk_pin && (b = jd_jr_td_risk_pin);
        return b
    }
    ;
    l.sendRequest = function(a, b, e) {
        try {
            try {
                var c = new window.XMLHttpRequest
            } catch (h) {}
            if (!c)
                try {
                    c = new window.ActiveXObject("Microsoft.XMLHTTP")
                } catch (h) {}
            if (!c)
                try {
                    c = new window.ActiveXObject("Msxml2.XMLHTTP")
                } catch (h) {}
            if (!c)
                try {
                    c = new window.ActiveXObject("Msxml3.XMLHTTP")
                } catch (h) {}
            c.open("POST", a, !0);
            c.timeout = 1E4;
            c.withCredentials = !0;
            c.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
            c.onreadystatechange = function() {
                4 === c.readyState && 200 === c.status && e && e(c.responseText)
            }
            ;
            c.send(b)
        } catch (h) {
            jdtRiskContext.d && console.error("sendRequest error : ", h)
        }
    }
    ;
    l.isDegrade = function() {
        var a = jdtRiskCookieManager.getCookie(collectConfig.store.giaDKey);
        if (a && 1 == a)
            return !0;
        a = jdtLocalStorageManager.get(collectConfig.store.ldeKey);
        if (!a)
            return !1;
        try {
            var b = JSON.parse(a)[jdtRiskUtil.getBizId()];
            return b ? b >= (new Date).getTime() : !1
        } catch (e) {}
        return !1
    }
    ;
    l.isValidJsToken = function(a) {
        return a ? a.startsWith("jdd03") && a.endsWith("X") : !1
    }
    ;
    l.cleanAndPushDeS = function(a, b) {
        try {
            if (a && b) {
                var e = jdtLocalStorageManager.get(collectConfig.store.ldeKey)
                  , c = {};
                e && (c = JSON.parse(e));
                var h = (new Date).getTime(), k;
                for (k in c)
                    c[k] < h && delete c[k];
                c[a] = h + 1E3 * b;
                jdtLocalStorageManager.set(collectConfig.store.ldeKey, JSON.stringify(c))
            }
        } catch (p) {}
    }
    ;
    l.randomStr = function(a) {
        var b = "";
        try {
            for (var e = 0; e < a; e++)
                b += "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz".charAt(Math.floor(62 * Math.random()))
        } catch (c) {}
        return b
    }
    ;
    return l
}(jdtRiskUtil || {})
  , jdtRiskEncryptUtil = function(l) {
    l.MD5 = function() {
        function m(a, b, e, c, h, k) {
            a = d(d(b, a), d(c, k));
            return d(a << h | a >>> 32 - h, e)
        }
        function n(a, b, e, c, h, k, p) {
            return m(b & e | ~b & c, a, b, h, k, p)
        }
        function g(a, b, e, c, h, k, p) {
            return m(b & c | e & ~c, a, b, h, k, p)
        }
        function f(a, b, e, c, h, k, p) {
            return m(e ^ (b | ~c), a, b, h, k, p)
        }
        function d(a, b) {
            var e = (a & 65535) + (b & 65535);
            return (a >> 16) + (b >> 16) + (e >> 16) << 16 | e & 65535
        }
        return {
            hex_md5: function(a) {
                if (null == a || void 0 == a || "" == a)
                    return "";
                if (null == a || void 0 == a || "" == a)
                    var b = "";
                else {
                    b = [];
                    for (var e = 0; e < 8 * a.length; e += 8)
                        b[e >> 5] |= (a.charCodeAt(e / 8) & 255) << e % 32
                }
                a = 8 * a.length;
                b[a >> 5] |= 128 << a % 32;
                b[(a + 64 >>> 9 << 4) + 14] = a;
                a = 1732584193;
                e = -271733879;
                for (var c = -1732584194, h = 271733878, k = 0; k < b.length; k += 16) {
                    var p = a
                      , q = e
                      , t = c
                      , u = h;
                    a = n(a, e, c, h, b[k + 0], 7, -680876936);
                    h = n(h, a, e, c, b[k + 1], 12, -389564586);
                    c = n(c, h, a, e, b[k + 2], 17, 606105819);
                    e = n(e, c, h, a, b[k + 3], 22, -1044525330);
                    a = n(a, e, c, h, b[k + 4], 7, -176418897);
                    h = n(h, a, e, c, b[k + 5], 12, 1200080426);
                    c = n(c, h, a, e, b[k + 6], 17, -1473231341);
                    e = n(e, c, h, a, b[k + 7], 22, -45705983);
                    a = n(a, e, c, h, b[k + 8], 7, 1770035416);
                    h = n(h, a, e, c, b[k + 9], 12, -1958414417);
                    c = n(c, h, a, e, b[k + 10], 17, -42063);
                    e = n(e, c, h, a, b[k + 11], 22, -1990404162);
                    a = n(a, e, c, h, b[k + 12], 7, 1804603682);
                    h = n(h, a, e, c, b[k + 13], 12, -40341101);
                    c = n(c, h, a, e, b[k + 14], 17, -1502002290);
                    e = n(e, c, h, a, b[k + 15], 22, 1236535329);
                    a = g(a, e, c, h, b[k + 1], 5, -165796510);
                    h = g(h, a, e, c, b[k + 6], 9, -1069501632);
                    c = g(c, h, a, e, b[k + 11], 14, 643717713);
                    e = g(e, c, h, a, b[k + 0], 20, -373897302);
                    a = g(a, e, c, h, b[k + 5], 5, -701558691);
                    h = g(h, a, e, c, b[k + 10], 9, 38016083);
                    c = g(c, h, a, e, b[k + 15], 14, -660478335);
                    e = g(e, c, h, a, b[k + 4], 20, -405537848);
                    a = g(a, e, c, h, b[k + 9], 5, 568446438);
                    h = g(h, a, e, c, b[k + 14], 9, -1019803690);
                    c = g(c, h, a, e, b[k + 3], 14, -187363961);
                    e = g(e, c, h, a, b[k + 8], 20, 1163531501);
                    a = g(a, e, c, h, b[k + 13], 5, -1444681467);
                    h = g(h, a, e, c, b[k + 2], 9, -51403784);
                    c = g(c, h, a, e, b[k + 7], 14, 1735328473);
                    e = g(e, c, h, a, b[k + 12], 20, -1926607734);
                    a = m(e ^ c ^ h, a, e, b[k + 5], 4, -378558);
                    h = m(a ^ e ^ c, h, a, b[k + 8], 11, -2022574463);
                    c = m(h ^ a ^ e, c, h, b[k + 11], 16, 1839030562);
                    e = m(c ^ h ^ a, e, c, b[k + 14], 23, -35309556);
                    a = m(e ^ c ^ h, a, e, b[k + 1], 4, -1530992060);
                    h = m(a ^ e ^ c, h, a, b[k + 4], 11, 1272893353);
                    c = m(h ^ a ^ e, c, h, b[k + 7], 16, -155497632);
                    e = m(c ^ h ^ a, e, c, b[k + 10], 23, -1094730640);
                    a = m(e ^ c ^ h, a, e, b[k + 13], 4, 681279174);
                    h = m(a ^ e ^ c, h, a, b[k + 0], 11, -358537222);
                    c = m(h ^ a ^ e, c, h, b[k + 3], 16, -722521979);
                    e = m(c ^ h ^ a, e, c, b[k + 6], 23, 76029189);
                    a = m(e ^ c ^ h, a, e, b[k + 9], 4, -640364487);
                    h = m(a ^ e ^ c, h, a, b[k + 12], 11, -421815835);
                    c = m(h ^ a ^ e, c, h, b[k + 15], 16, 530742520);
                    e = m(c ^ h ^ a, e, c, b[k + 2], 23, -995338651);
                    a = f(a, e, c, h, b[k + 0], 6, -198630844);
                    h = f(h, a, e, c, b[k + 7], 10, 1126891415);
                    c = f(c, h, a, e, b[k + 14], 15, -1416354905);
                    e = f(e, c, h, a, b[k + 5], 21, -57434055);
                    a = f(a, e, c, h, b[k + 12], 6, 1700485571);
                    h = f(h, a, e, c, b[k + 3], 10, -1894986606);
                    c = f(c, h, a, e, b[k + 10], 15, -1051523);
                    e = f(e, c, h, a, b[k + 1], 21, -2054922799);
                    a = f(a, e, c, h, b[k + 8], 6, 1873313359);
                    h = f(h, a, e, c, b[k + 15], 10, -30611744);
                    c = f(c, h, a, e, b[k + 6], 15, -1560198380);
                    e = f(e, c, h, a, b[k + 13], 21, 1309151649);
                    a = f(a, e, c, h, b[k + 4], 6, -145523070);
                    h = f(h, a, e, c, b[k + 11], 10, -1120210379);
                    c = f(c, h, a, e, b[k + 2], 15, 718787259);
                    e = f(e, c, h, a, b[k + 9], 21, -343485551);
                    a = d(a, p);
                    e = d(e, q);
                    c = d(c, t);
                    h = d(h, u)
                }
                b = [a, e, c, h];
                a = "";
                for (e = 0; e < 4 * b.length; e++)
                    a += "0123456789abcdef".charAt(b[e >> 2] >> e % 4 * 8 + 4 & 15) + "0123456789abcdef".charAt(b[e >> 2] >> e % 4 * 8 & 15);
                return a
            }
        }
    }();
    l.HASH = function() {
        function m(b, e) {
            b = [b[0] >>> 16, b[0] & 65535, b[1] >>> 16, b[1] & 65535];
            e = [e[0] >>> 16, e[0] & 65535, e[1] >>> 16, e[1] & 65535];
            var c = [0, 0, 0, 0];
            c[3] += b[3] + e[3];
            c[2] += c[3] >>> 16;
            c[3] &= 65535;
            c[2] += b[2] + e[2];
            c[1] += c[2] >>> 16;
            c[2] &= 65535;
            c[1] += b[1] + e[1];
            c[0] += c[1] >>> 16;
            c[1] &= 65535;
            c[0] += b[0] + e[0];
            c[0] &= 65535;
            return [c[0] << 16 | c[1], c[2] << 16 | c[3]]
        }
        function n(b, e) {
            b = [b[0] >>> 16, b[0] & 65535, b[1] >>> 16, b[1] & 65535];
            e = [e[0] >>> 16, e[0] & 65535, e[1] >>> 16, e[1] & 65535];
            var c = [0, 0, 0, 0];
            c[3] += b[3] * e[3];
            c[2] += c[3] >>> 16;
            c[3] &= 65535;
            c[2] += b[2] * e[3];
            c[1] += c[2] >>> 16;
            c[2] &= 65535;
            c[2] += b[3] * e[2];
            c[1] += c[2] >>> 16;
            c[2] &= 65535;
            c[1] += b[1] * e[3];
            c[0] += c[1] >>> 16;
            c[1] &= 65535;
            c[1] += b[2] * e[2];
            c[0] += c[1] >>> 16;
            c[1] &= 65535;
            c[1] += b[3] * e[1];
            c[0] += c[1] >>> 16;
            c[1] &= 65535;
            c[0] += b[0] * e[3] + b[1] * e[2] + b[2] * e[1] + b[3] * e[0];
            c[0] &= 65535;
            return [c[0] << 16 | c[1], c[2] << 16 | c[3]]
        }
        function g(b, e) {
            e %= 64;
            if (32 === e)
                return [b[1], b[0]];
            if (32 > e)
                return [b[0] << e | b[1] >>> 32 - e, b[1] << e | b[0] >>> 32 - e];
            e -= 32;
            return [b[1] << e | b[0] >>> 32 - e, b[0] << e | b[1] >>> 32 - e]
        }
        function f(b, e) {
            e %= 64;
            return 0 === e ? b : 32 > e ? [b[0] << e | b[1] >>> 32 - e, b[1] << e] : [b[1] << e - 32, 0]
        }
        function d(b, e) {
            return [b[0] ^ e[0], b[1] ^ e[1]]
        }
        function a(b) {
            b = d(b, [0, b[0] >>> 1]);
            b = n(b, [4283543511, 3981806797]);
            b = d(b, [0, b[0] >>> 1]);
            b = n(b, [3301882366, 444984403]);
            return b = d(b, [0, b[0] >>> 1])
        }
        return {
            hash128: function(b, e) {
                b = b || "";
                var c = e || 0;
                e = b.length % 16;
                var h = b.length - e
                  , k = [0, c];
                c = [0, c];
                for (var p, q, t = [2277735313, 289559509], u = [1291169091, 658871167], r = 0; r < h; r += 16)
                    p = [b.charCodeAt(r + 4) & 255 | (b.charCodeAt(r + 5) & 255) << 8 | (b.charCodeAt(r + 6) & 255) << 16 | (b.charCodeAt(r + 7) & 255) << 24, b.charCodeAt(r) & 255 | (b.charCodeAt(r + 1) & 255) << 8 | (b.charCodeAt(r + 2) & 255) << 16 | (b.charCodeAt(r + 3) & 255) << 24],
                    q = [b.charCodeAt(r + 12) & 255 | (b.charCodeAt(r + 13) & 255) << 8 | (b.charCodeAt(r + 14) & 255) << 16 | (b.charCodeAt(r + 15) & 255) << 24, b.charCodeAt(r + 8) & 255 | (b.charCodeAt(r + 9) & 255) << 8 | (b.charCodeAt(r + 10) & 255) << 16 | (b.charCodeAt(r + 11) & 255) << 24],
                    p = n(p, t),
                    p = g(p, 31),
                    p = n(p, u),
                    k = d(k, p),
                    k = g(k, 27),
                    k = m(k, c),
                    k = m(n(k, [0, 5]), [0, 1390208809]),
                    q = n(q, u),
                    q = g(q, 33),
                    q = n(q, t),
                    c = d(c, q),
                    c = g(c, 31),
                    c = m(c, k),
                    c = m(n(c, [0, 5]), [0, 944331445]);
                p = [0, 0];
                q = [0, 0];
                switch (e) {
                case 15:
                    q = d(q, f([0, b.charCodeAt(r + 14)], 48));
                case 14:
                    q = d(q, f([0, b.charCodeAt(r + 13)], 40));
                case 13:
                    q = d(q, f([0, b.charCodeAt(r + 12)], 32));
                case 12:
                    q = d(q, f([0, b.charCodeAt(r + 11)], 24));
                case 11:
                    q = d(q, f([0, b.charCodeAt(r + 10)], 16));
                case 10:
                    q = d(q, f([0, b.charCodeAt(r + 9)], 8));
                case 9:
                    q = d(q, [0, b.charCodeAt(r + 8)]),
                    q = n(q, u),
                    q = g(q, 33),
                    q = n(q, t),
                    c = d(c, q);
                case 8:
                    p = d(p, f([0, b.charCodeAt(r + 7)], 56));
                case 7:
                    p = d(p, f([0, b.charCodeAt(r + 6)], 48));
                case 6:
                    p = d(p, f([0, b.charCodeAt(r + 5)], 40));
                case 5:
                    p = d(p, f([0, b.charCodeAt(r + 4)], 32));
                case 4:
                    p = d(p, f([0, b.charCodeAt(r + 3)], 24));
                case 3:
                    p = d(p, f([0, b.charCodeAt(r + 2)], 16));
                case 2:
                    p = d(p, f([0, b.charCodeAt(r + 1)], 8));
                case 1:
                    p = d(p, [0, b.charCodeAt(r)]),
                    p = n(p, t),
                    p = g(p, 31),
                    p = n(p, u),
                    k = d(k, p)
                }
                k = d(k, [0, b.length]);
                c = d(c, [0, b.length]);
                k = m(k, c);
                c = m(c, k);
                k = a(k);
                c = a(c);
                k = m(k, c);
                c = m(c, k);
                return ("00000000" + (k[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (k[1] >>> 0).toString(16)).slice(-8) + ("00000000" + (c[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (c[1] >>> 0).toString(16)).slice(-8)
            }
        }
    }();
    l.TDEncrypt = function() {
        return function(m) {
            m = JSON.stringify(m);
            m = encodeURIComponent(m);
            var n = ""
              , g = 0;
            do {
                var f = m.charCodeAt(g++);
                var d = m.charCodeAt(g++);
                var a = m.charCodeAt(g++);
                var b = f >> 2;
                f = (f & 3) << 4 | d >> 4;
                var e = (d & 15) << 2 | a >> 6;
                var c = a & 63;
                isNaN(d) ? e = c = 64 : isNaN(a) && (c = 64);
                n = n + "23IL<N01c7KvwZO56RSTAfghiFyzWJqVabGH4PQdopUrsCuX*xeBjkltDEmn89.-".charAt(b) + "23IL<N01c7KvwZO56RSTAfghiFyzWJqVabGH4PQdopUrsCuX*xeBjkltDEmn89.-".charAt(f) + "23IL<N01c7KvwZO56RSTAfghiFyzWJqVabGH4PQdopUrsCuX*xeBjkltDEmn89.-".charAt(e) + "23IL<N01c7KvwZO56RSTAfghiFyzWJqVabGH4PQdopUrsCuX*xeBjkltDEmn89.-".charAt(c)
            } while (g < m.length);
            return n + "/"
        }
    }();
    return l
}(jdtRiskEncryptUtil || {})
  , JdtRiskFingerPrint = function(l) {
    function m() {
        var f = document.createElement("canvas");
        return !(!f.getContext || !f.getContext("2d"))
    }
    l = l || {};
    var n = ""
      , g = function() {
        var f = {};
        f.nativeForEach = Array.prototype.forEach;
        f.nativeMap = Array.prototype.map;
        f.each = function(d, a, b) {
            if (null !== d)
                if (f.nativeForEach && d.forEach === f.nativeForEach)
                    d.forEach(a, b);
                else if (d.length === +d.length)
                    for (var e = 0, c = d.length; e < c && a.call(b, d[e], e, d) !== {}; e++)
                        ;
                else
                    for (e in d)
                        if (d.hasOwnProperty(e) && a.call(b, d[e], e, d) === {})
                            break
        }
        ;
        f.map = function(d, a, b) {
            var e = [];
            if (null == d)
                return e;
            if (f.nativeMap && d.map === f.nativeMap)
                return d.map(a, b);
            f.each(d, function(c, h, k) {
                e[e.length] = a.call(b, c, h, k)
            });
            return e
        }
        ;
        f.execute = function(d) {
            try {
                if (this[d]) {
                    var a = (new Date).getTime()
                      , b = this[d]();
                    jdtRiskContext.d && console.log("FP function : [" + d + "] Cost time :", (new Date).getTime() - a);
                    return b
                }
            } catch (e) {
                return jdtRiskContext.d && console.log("fp collect error", e),
                ""
            }
        }
        ;
        f.getLanguage = function() {
            return navigator.language
        }
        ;
        f.getUserAgent = function() {
            return navigator.userAgent.toLowerCase()
        }
        ;
        f.getOsInfo = function() {
            var d = f.getUserAgent()
              , a = "NA"
              , b = "NA";
            try {
                -1 != d.indexOf("win") && -1 != d.indexOf("95") && (a = "windows",
                b = "95"),
                -1 != d.indexOf("win") && -1 != d.indexOf("98") && (a = "windows",
                b = "98"),
                -1 != d.indexOf("win 9x") && -1 != d.indexOf("4.90") && (a = "windows",
                b = "me"),
                -1 != d.indexOf("win") && -1 != d.indexOf("nt 5.0") && (a = "windows",
                b = "2000"),
                -1 != d.indexOf("win") && -1 != d.indexOf("nt") && (a = "windows",
                b = "NT"),
                -1 != d.indexOf("win") && -1 != d.indexOf("nt 5.1") && (a = "windows",
                b = "xp"),
                -1 != d.indexOf("win") && -1 != d.indexOf("32") && (a = "windows",
                b = "32"),
                -1 != d.indexOf("win") && -1 != d.indexOf("nt 5.1") && (a = "windows",
                b = "7"),
                -1 != d.indexOf("win") && -1 != d.indexOf("6.0") && (a = "windows",
                b = "8"),
                -1 == d.indexOf("win") || -1 == d.indexOf("nt 6.0") && -1 == d.indexOf("nt 6.1") || (a = "windows",
                b = "9"),
                -1 != d.indexOf("win") && -1 != d.indexOf("nt 6.2") && (a = "windows",
                b = "10"),
                -1 != d.indexOf("linux") && (a = "linux"),
                -1 != d.indexOf("unix") && (a = "unix"),
                -1 != d.indexOf("sun") && -1 != d.indexOf("os") && (a = "sun os"),
                -1 != d.indexOf("ibm") && -1 != d.indexOf("os") && (a = "ibm os/2"),
                -1 != d.indexOf("mac") && -1 != d.indexOf("pc") && (a = "mac"),
                -1 != d.indexOf("aix") && (a = "aix"),
                -1 != d.indexOf("powerpc") && (a = "powerPC"),
                -1 != d.indexOf("hpux") && (a = "hpux"),
                -1 != d.indexOf("netbsd") && (a = "NetBSD"),
                -1 != d.indexOf("bsd") && (a = "BSD"),
                -1 != d.indexOf("osf1") && (a = "OSF1"),
                -1 != d.indexOf("irix") && (a = "IRIX",
                b = ""),
                -1 != d.indexOf("freebsd") && (a = "FreeBSD"),
                -1 != d.indexOf("symbianos") && (a = "SymbianOS",
                b = d.substring(d.indexOf("SymbianOS/") + 10, 3))
            } catch (e) {}
            return {
                os: a,
                osVersion: b
            }
        }
        ;
        f.getBrowserInfo = function() {
            var d = f.getUserAgent()
              , a = "NA"
              , b = "NA";
            try {
                -1 != d.indexOf("msie") && (a = "ie",
                b = d.substring(d.indexOf("msie ") + 5),
                b.indexOf(";") && (b = b.substring(0, b.indexOf(";"))));
                -1 != d.indexOf("firefox") && (a = "Firefox",
                b = d.substring(d.indexOf("firefox/") + 8));
                -1 != d.indexOf("opera") && (a = "Opera",
                b = d.substring(d.indexOf("opera/") + 6, 4));
                -1 != d.indexOf("safari") && (a = "safari",
                b = d.substring(d.indexOf("safari/") + 7));
                -1 != d.indexOf("chrome") && (a = "chrome",
                b = d.substring(d.indexOf("chrome/") + 7),
                b.indexOf(" ") && (b = b.substring(0, b.indexOf(" "))));
                -1 != d.indexOf("navigator") && (a = "navigator",
                b = d.substring(d.indexOf("navigator/") + 10));
                -1 != d.indexOf("applewebkit") && (a = "applewebkit_chrome",
                b = d.substring(d.indexOf("applewebkit/") + 12),
                b.indexOf(" ") && (b = b.substring(0, b.indexOf(" "))));
                -1 != d.indexOf("sogoumobilebrowser") && (a = "\u641c\u72d7\u624b\u673a\u6d4f\u89c8\u5668");
                if (-1 != d.indexOf("ucbrowser") || -1 != d.indexOf("ucweb"))
                    a = "UC\u6d4f\u89c8\u5668";
                if (-1 != d.indexOf("qqbrowser") || -1 != d.indexOf("tencenttraveler"))
                    a = "QQ\u6d4f\u89c8\u5668";
                -1 != d.indexOf("metasr") && (a = "\u641c\u72d7\u6d4f\u89c8\u5668");
                -1 != d.indexOf("360se") && (a = "360\u6d4f\u89c8\u5668");
                -1 != d.indexOf("the world") && (a = "\u4e16\u754c\u4e4b\u7a97\u6d4f\u89c8\u5668");
                -1 != d.indexOf("maxthon") && (a = "\u9068\u6e38\u6d4f\u89c8\u5668")
            } catch (e) {}
            return {
                browser: a,
                browserVersion: b
            }
        }
        ;
        f.getColorDepth = function() {
            return screen.colorDepth
        }
        ;
        f.getScreenResolution = function() {
            return [screen.height, screen.width].join("x")
        }
        ;
        f.getTimezoneOffset = function() {
            return (new Date).getTimezoneOffset()
        }
        ;
        f.getSessionStorageSupport = function() {
            try {
                return !!window.sessionStorage
            } catch (d) {
                return !0
            }
        }
        ;
        f.getLocalStorageSupport = function() {
            try {
                return !!window.localStorage
            } catch (d) {
                return !0
            }
        }
        ;
        f.getIndexedDBSupport = function() {
            return !!window.indexedDB
        }
        ;
        f.getAddBehaviorSupport = function() {
            return document.body && !!document.body.addBehavior
        }
        ;
        f.getOpenDatabaseSupport = function() {
            return !!window.openDatabase
        }
        ;
        f.getNavigatorCpuClass = function() {
            return navigator.oscpu || navigator.cpuClass ? navigator.cpuClass : "NA"
        }
        ;
        f.getNavigatorPlatform = function() {
            return navigator.platform ? navigator.platform : "NA"
        }
        ;
        f.getHardwareConcurrency = function() {
            return navigator.hardwareConcurrency ? navigator.hardwareConcurrency : "NA"
        }
        ;
        f.getAudioKey = function() {
            var d = ""
              , a = navigator.userAgent.toLowerCase();
            -1 != a.indexOf("chrome") && (a = a.substring(a.indexOf("chrome/") + 7),
            a.indexOf(" ") && (d = a = a.substring(0, a.indexOf(" ")),
            "" != d && d.indexOf(".") && (d = a.substring(0, a.indexOf(".")))));
            a = !0;
            "" != d && !isNaN(d) && 47 > parseInt(d) && (a = !1);
            d = "";
            a && (a = window.AudioContext || window.webkitAudioContext) && (a = new a,
            d = a.sampleRate.toString(),
            a.close && a.close());
            return d
        }
        ;
        f.getDoNotTrack = function() {
            return navigator.doNotTrack || navigator.msDoNotTrack ? navigator.doNotTrack || navigator.msDoNotTrack : "NA"
        }
        ;
        f.getIEPluginsString = function() {
            return void 0 !== window.ActiveXObject ? f.map("AcroPDF.PDF;Adodb.Stream;AgControl.AgControl;DevalVRXCtrl.DevalVRXCtrl.1;MacromediaFlashPaper.MacromediaFlashPaper;Msxml2.DOMDocument;Msxml2.XMLHTTP;PDF.PdfCtrl;QuickTime.QuickTime;QuickTimeCheckObject.QuickTimeCheck.1;RealPlayer;RealPlayer.RealPlayer(tm) ActiveX Control (32-bit);RealVideo.RealVideo(tm) ActiveX Control (32-bit);Scripting.Dictionary;SWCtl.SWCtl;Shell.UIHelper;ShockwaveFlash.ShockwaveFlash;Skype.Detection;TDCCtl.TDCCtl;WMPlayer.OCX;rmocx.RealPlayer G2 Control;rmocx.RealPlayer G2 Control.1".split(";"), function(d) {
                try {
                    return new ActiveXObject(d),
                    d
                } catch (a) {
                    return null
                }
            }).join(";") : ""
        }
        ;
        f.getRegularPluginsString = function() {
            return f.map(navigator.plugins, function(d) {
                var a = f.map(d, function(b) {
                    return [b.type, b.suffixes].join("~")
                }).join(",");
                return [d.name, d.description, a].join("::")
            }, this).join(";")
        }
        ;
        f.getCanvasFp = function() {
            var d = []
              , a = document.createElement("canvas");
            a.width = 2E3;
            a.height = 200;
            a.style.display = "inline";
            var b = a.getContext("2d");
            b.rect(0, 0, 10, 10);
            b.rect(2, 2, 6, 6);
            d.push("cw:" + (!1 === b.isPointInPath(5, 5, "evenodd") ? "yes" : "no"));
            b.textBaseline = "alphabetic";
            b.fillStyle = "#f60";
            b.fillRect(125, 1, 62, 20);
            b.fillStyle = "#069";
            b.font = "11pt no-real-font-123";
            b.fillText("Cwwm aa fjorddbank glbyphs veext qtuiz, \ud83d\ude03", 2, 15);
            b.fillStyle = "rgba(102, 204, 0, 0.2)";
            b.font = "18pt Arial";
            b.fillText("Cwwm aa fjorddbank glbyphs veext qtuiz, \ud83d\ude03", 4, 45);
            b.globalCompositeOperation = "multiply";
            b.fillStyle = "rgb(255,0,255)";
            b.beginPath();
            b.arc(50, 50, 50, 0, 2 * Math.PI, !0);
            b.closePath();
            b.fill();
            b.fillStyle = "rgb(0,255,255)";
            b.beginPath();
            b.arc(100, 50, 50, 0, 2 * Math.PI, !0);
            b.closePath();
            b.fill();
            b.fillStyle = "rgb(255,255,0)";
            b.beginPath();
            b.arc(75, 100, 50, 0, 2 * Math.PI, !0);
            b.closePath();
            b.fill();
            b.fillStyle = "rgb(255,0,255)";
            b.arc(75, 75, 75, 0, 2 * Math.PI, !0);
            b.arc(75, 75, 25, 0, 2 * Math.PI, !0);
            b.fill("evenodd");
            d.push("cfp:" + a.toDataURL());
            return d.join("~")
        }
        ;
        f.getWebglFp = function() {
            var d = function(q) {
                a.clearColor(0, 0, 0, 1);
                a.enable(a.DEPTH_TEST);
                a.depthFunc(a.LEQUAL);
                a.clear(a.COLOR_BUFFER_BIT | a.DEPTH_BUFFER_BIT);
                return "[" + q[0] + ", " + q[1] + "]"
            };
            var a = this.getWebglCanvas();
            if (!a)
                return null;
            var b = []
              , e = a.createBuffer();
            a.bindBuffer(a.ARRAY_BUFFER, e);
            var c = new Float32Array([-.2, -.9, 0, .4, -.26, 0, 0, .732134444, 0]);
            a.bufferData(a.ARRAY_BUFFER, c, a.STATIC_DRAW);
            e.itemSize = 3;
            e.numItems = 3;
            c = a.createProgram();
            var h = a.createShader(a.VERTEX_SHADER);
            a.shaderSource(h, "attribute vec2 attrVertex;varying vec2 varyinTexCoordinate;uniform vec2 uniformOffset;void main(){varyinTexCoordinate=attrVertex+uniformOffset;gl_Position=vec4(attrVertex,0,1);}");
            a.compileShader(h);
            var k = a.createShader(a.FRAGMENT_SHADER);
            a.shaderSource(k, "precision mediump float;varying vec2 varyinTexCoordinate;void main() {gl_FragColor=vec4(varyinTexCoordinate,0,1);}");
            a.compileShader(k);
            a.attachShader(c, h);
            a.attachShader(c, k);
            a.linkProgram(c);
            a.useProgram(c);
            c.vertexPosAttrib = a.getAttribLocation(c, "attrVertex");
            c.offsetUniform = a.getUniformLocation(c, "uniformOffset");
            a.enableVertexAttribArray(c.vertexPosArray);
            a.vertexAttribPointer(c.vertexPosAttrib, e.itemSize, a.FLOAT, !1, 0, 0);
            a.uniform2f(c.offsetUniform, 1, 1);
            a.drawArrays(a.TRIANGLE_STRIP, 0, e.numItems);
            null != a.canvas && b.push(a.canvas.toDataURL());
            b.push("extensions:" + a.getSupportedExtensions().join(";"));
            b.push("w1" + d(a.getParameter(a.ALIASED_LINE_WIDTH_RANGE)));
            b.push("w2" + d(a.getParameter(a.ALIASED_POINT_SIZE_RANGE)));
            b.push("w3" + a.getParameter(a.ALPHA_BITS));
            b.push("w4" + (a.getContextAttributes().antialias ? "yes" : "no"));
            b.push("w5" + a.getParameter(a.BLUE_BITS));
            b.push("w6" + a.getParameter(a.DEPTH_BITS));
            b.push("w7" + a.getParameter(a.GREEN_BITS));
            b.push("w8" + function(q) {
                var t, u = q.getExtension("EXT_texture_filter_anisotropic") || q.getExtension("WEBKIT_EXT_texture_filter_anisotropic") || q.getExtension("MOZ_EXT_texture_filter_anisotropic");
                return u ? (t = q.getParameter(u.MAX_TEXTURE_MAX_ANISOTROPY_EXT),
                0 === t && (t = 2),
                t) : null
            }(a));
            b.push("w9" + a.getParameter(a.MAX_COMBINED_TEXTURE_IMAGE_UNITS));
            b.push("w10" + a.getParameter(a.MAX_CUBE_MAP_TEXTURE_SIZE));
            b.push("w11" + a.getParameter(a.MAX_FRAGMENT_UNIFORM_VECTORS));
            b.push("w12" + a.getParameter(a.MAX_RENDERBUFFER_SIZE));
            b.push("w13" + a.getParameter(a.MAX_TEXTURE_IMAGE_UNITS));
            b.push("w14" + a.getParameter(a.MAX_TEXTURE_SIZE));
            b.push("w15" + a.getParameter(a.MAX_VARYING_VECTORS));
            b.push("w16" + a.getParameter(a.MAX_VERTEX_ATTRIBS));
            b.push("w17" + a.getParameter(a.MAX_VERTEX_TEXTURE_IMAGE_UNITS));
            b.push("w18" + a.getParameter(a.MAX_VERTEX_UNIFORM_VECTORS));
            b.push("w19" + d(a.getParameter(a.MAX_VIEWPORT_DIMS)));
            b.push("w20" + a.getParameter(a.RED_BITS));
            b.push("w21" + a.getParameter(a.RENDERER));
            b.push("w22" + a.getParameter(a.SHADING_LANGUAGE_VERSION));
            b.push("w23" + a.getParameter(a.STENCIL_BITS));
            b.push("w24" + a.getParameter(a.VENDOR));
            b.push("w25" + a.getParameter(a.VERSION));
            try {
                var p = a.getExtension("WEBGL_debug_renderer_info");
                p && (b.push("wuv:" + a.getParameter(p.UNMASKED_VENDOR_WEBGL)),
                b.push("wur:" + a.getParameter(p.UNMASKED_RENDERER_WEBGL)))
            } catch (q) {}
            if (!a.getShaderPrecisionFormat)
                return b.join("\u00a7");
            b.push("w26" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.HIGH_FLOAT).precision);
            b.push("w27" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.HIGH_FLOAT).rangeMin);
            b.push("w28" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.HIGH_FLOAT).rangeMax);
            b.push("w29" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.MEDIUM_FLOAT).precision);
            b.push("w30" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.MEDIUM_FLOAT).rangeMin);
            b.push("w31" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.MEDIUM_FLOAT).rangeMax);
            b.push("w32" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.LOW_FLOAT).precision);
            b.push("w33" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.LOW_FLOAT).rangeMin);
            b.push("w34" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.LOW_FLOAT).rangeMax);
            b.push("w35" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.HIGH_FLOAT).precision);
            b.push("w36" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.HIGH_FLOAT).rangeMin);
            b.push("w37" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.HIGH_FLOAT).rangeMax);
            b.push("w38" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.MEDIUM_FLOAT).precision);
            b.push("w39" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.MEDIUM_FLOAT).rangeMin);
            b.push("w40" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.MEDIUM_FLOAT).rangeMax);
            b.push("w41" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.LOW_FLOAT).precision);
            b.push("w42" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.LOW_FLOAT).rangeMin);
            b.push("w43" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.LOW_FLOAT).rangeMax);
            b.push("w44" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.HIGH_INT).precision);
            b.push("w45" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.HIGH_INT).rangeMin);
            b.push("w46" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.HIGH_INT).rangeMax);
            b.push("w47" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.MEDIUM_INT).precision);
            b.push("w48" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.MEDIUM_INT).rangeMin);
            b.push("w49" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.MEDIUM_INT).rangeMax);
            b.push("w50" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.LOW_INT).precision);
            b.push("w51" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.LOW_INT).rangeMin);
            b.push("w52" + a.getShaderPrecisionFormat(a.VERTEX_SHADER, a.LOW_INT).rangeMax);
            b.push("w53" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.HIGH_INT).precision);
            b.push("w54" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.HIGH_INT).rangeMin);
            b.push("w55" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.HIGH_INT).rangeMax);
            b.push("w56" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.MEDIUM_INT).precision);
            b.push("w57" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.MEDIUM_INT).rangeMin);
            b.push("w58" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.MEDIUM_INT).rangeMax);
            b.push("w59" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.LOW_INT).precision);
            b.push("w60" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.LOW_INT).rangeMin);
            b.push("w61" + a.getShaderPrecisionFormat(a.FRAGMENT_SHADER, a.LOW_INT).rangeMax);
            return b.join("\u00a7")
        }
        ;
        f.getWebglCanvas = function() {
            var d = document.createElement("canvas")
              , a = null;
            try {
                a = d.getContext("webgl") || d.getContext("experimental-webgl")
            } catch (b) {}
            a || (a = null);
            return a
        }
        ;
        return f
    }();
    return {
        getFp: function(f) {
            n = n || jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].fpKey, !1);
            var d = 1 * jdtLocalStorageManager.get(collectConfig.store[_riskFpMode].fpTsKey);
            if (!(n && 32 == n.length && (d || 0) >= (new Date).getTime())) {
                var a = l;
                a = a || {};
                d = [];
                var b = g.execute("getBrowserInfo")
                  , e = g.execute("getOsInfo");
                if (!a[collectConfig.fp.userAgent]) {
                    var c = g.execute("getUserAgent")
                      , h = 1 * b.browserVersion;
                    "ie" == b.browser && 7 <= h ? d.push(c) : d.push(navigator.userAgent)
                }
                a[collectConfig.fp.language] || d.push(g.execute("getLanguage"));
                d.push(b.browser);
                d.push(b.browserVersion);
                d.push(e.os);
                d.push(e.osVersion);
                a[collectConfig.fp.colorDepth] || d.push(g.execute("getColorDepth"));
                a[collectConfig.fp.screenResolution] || d.push(g.execute("getScreenResolution"));
                a[collectConfig.fp.timezoneOffset] || d.push(g.execute("getTimezoneOffset"));
                a[collectConfig.fp.sessionStorage] || g.execute("getSessionStorageSupport") && d.push("sessionStorageKey");
                a[collectConfig.fp.localStorage] || g.execute("getLocalStorageSupport") && d.push("localStorageKey");
                a[collectConfig.fp.indexedDb] || g.execute("getIndexedDBSupport") && d.push("indexedDbKey");
                a[collectConfig.fp.addBehavior] || g.execute("getAddBehaviorSupport") && d.push("addBehaviorKey");
                a[collectConfig.fp.openDatabase] || g.execute("getOpenDatabaseSupport") && d.push("openDatabase");
                a[collectConfig.fp.cpuClass] || d.push(g.execute("getNavigatorCpuClass"));
                a[collectConfig.fp.platform] || d.push(g.execute("getNavigatorPlatform"));
                a[collectConfig.fp.hardwareConcurrency] || d.push(g.execute("getHardwareConcurrency"));
                a[collectConfig.fp.audioKey] || (b = g.execute("getAudioKey")) && d.push(b);
                a[collectConfig.fp.doNotTrack] || d.push(g.execute("getDoNotTrack"));
                a[collectConfig.fp.plugins] || ("Microsoft Internet Explorer" === navigator.appName || "Netscape" === navigator.appName && /Trident/.test(navigator.userAgent) ? d.push(g.execute("getIEPluginsString")) : d.push(g.execute("getRegularPluginsString")));
                !a[collectConfig.fp.canvas] && m() && (b = g.execute("getCanvasFp"),
                jdtRiskContext.canvas_fp_md5 = jdtRiskEncryptUtil.MD5.hex_md5(b),
                jdtRiskStorageManager.store(collectConfig.store.canvasFpKey, jdtRiskContext.canvas_fp_md5, !1),
                d.push(b));
                !a[collectConfig.fp.webgl] && m() && (a = g.execute("getWebglFp"),
                d.push(a));
                jdtRiskContext.d && console.log("fp keys:", d);
                n = jdtRiskEncryptUtil.HASH.hash128(d.join("~~~"), 31);
                jdtRiskStorageManager.store(collectConfig.store[_riskFpMode].fpKey, n, !1);
                jdtLocalStorageManager.set(collectConfig.store[_riskFpMode].fpTsKey, (new Date).getTime() + 6E5)
            }
            f(n)
        }
    }
}
  , jdtRiskCookieManager = function() {
    return {
        setCookie: function(l, m, n) {
            try {
                if (m) {
                    "undefined" == typeof n && (n = 31104E3);
                    var g = new Date;
                    g.setTime(g.getTime() + 1E3 * n);
                    var f = "expires=" + g.toUTCString();
                    document.cookie = l + "=" + m + "; " + f + "; path=/; domain=" + jdtRiskUtil.getCurrentRootDomain()
                }
            } catch (d) {}
        },
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
        }
    }
}()
  , jdtLocalStorageManager = function() {
    return {
        set: function(l, m) {
            try {
                m && window.localStorage && window.localStorage.setItem(l, m)
            } catch (n) {}
        },
        get: function(l) {
            try {
                if (window.localStorage)
                    return window.localStorage.getItem(l)
            } catch (m) {}
            return ""
        }
    }
}()
  , jdtRiskStorageManager = function(l) {
    l.db = void 0;
    return {
        store: function(m, n, g, f) {
            "undefined" == typeof g && (g = !0);
            if (g)
                try {
                    jdtRiskCookieManager.setCookie(m, n, f)
                } catch (d) {}
            try {
                jdtLocalStorageManager.set(m, n)
            } catch (d) {}
            try {
                window.sessionStorage && window.sessionStorage.setItem(m, n)
            } catch (d) {}
            try {
                window.globalStorage && window.globalStorage[".localdomain"].setItem(m, n)
            } catch (d) {}
        },
        load: function(m, n, g) {
            "undefined" == typeof n && (n = !0);
            g = g || function(d) {
                return !!d
            }
            ;
            var f = null;
            if (n)
                try {
                    if (f = jdtRiskCookieManager.getCookie(m),
                    g(f))
                        return f
                } catch (d) {}
            try {
                if (f = jdtLocalStorageManager.get(m),
                g(f))
                    return f
            } catch (d) {}
            try {
                if (window.sessionStorage && (f = window.sessionStorage(m),
                g(f)))
                    return f
            } catch (d) {}
            try {
                if (window.globalStorage && (f = window.globalStorage[".localdomain"](m),
                g(f)))
                    return f
            } catch (d) {}
            return f
        }
    }
}(jdtRiskStorageManager || {})
  , TDEnvCollector = function(l) {
    function m(g) {
        var f = {};
        f.name = g.name;
        f.filename = g.filename.toLowerCase();
        f.description = g.description;
        void 0 !== g.version && (f.version = g.version);
        f.mimeTypes = [];
        for (var d = 0; d < g.length; d++) {
            var a = g[d]
              , b = {};
            b.description = a.description;
            b.suffixes = a.suffixes;
            b.type = a.type;
            f.mimeTypes.push(b)
        }
        return f
    }
    l = l || {};
    var n = function() {
        return {
            execute: function(g) {
                try {
                    if (this[g]) {
                        var f = (new Date).getTime()
                          , d = this[g]();
                        jdtRiskContext.d && console.log("ENV Collector function : [" + g + "] Cost time :", (new Date).getTime() - f);
                        return d
                    }
                } catch (a) {
                    return jdtRiskContext.d && console.log("env collect error", a),
                    ""
                }
            },
            getColorRgb: function() {
                var g = {};
                try {
                    var f = document.createElement("div")
                      , d = "ActiveBorder ActiveCaption AppWorkspace Background ButtonFace ButtonHighlight ButtonShadow ButtonText CaptionText GrayText Highlight HighlightText InactiveBorder InactiveCaption InactiveCaptionText InfoBackground InfoText Menu MenuText Scrollbar ThreeDDarkShadow ThreeDFace ThreeDHighlight ThreeDLightShadow ThreeDShadow Window WindowFrame WindowText".split(" ");
                    if (window.getComputedStyle)
                        for (var a = 0; a < d.length; a++)
                            document.body.appendChild(f),
                            f.style.color = d[a],
                            g[d[a]] = window.getComputedStyle(f).getPropertyValue("color"),
                            document.body.removeChild(f)
                } catch (b) {}
                return g
            },
            getCanvasInfo: function() {
                var g = {};
                g.tdHash = jdtRiskContext.canvas_fp_md5 || jdtRiskStorageManager.load(collectConfig.store.canvasFpKey, !1);
                var f = !1;
                if (window.WebGLRenderingContext) {
                    for (var d = ["webgl", "experimental-webgl", "moz-webgl", "webkit-3d"], a = [], b, e = 0; e < d.length; e++)
                        try {
                            var c = !1;
                            (c = document.createElement("canvas").getContext(d[e], {
                                stencil: !0
                            })) && c && (b = c,
                            a.push(d[e]))
                        } catch (k) {}
                    a.length && (f = {
                        name: a,
                        gl: b
                    })
                }
                if (f) {
                    d = f.gl;
                    g.contextName = f.name.join();
                    g.webglversion = d.getParameter(d.VERSION);
                    g.shadingLV = d.getParameter(d.SHADING_LANGUAGE_VERSION);
                    g.vendor = d.getParameter(d.VENDOR);
                    g.renderer = d.getParameter(d.RENDERER);
                    f = [];
                    try {
                        f = d.getSupportedExtensions(),
                        g.extensions = f
                    } catch (k) {}
                    try {
                        var h = d.getExtension("WEBGL_debug_renderer_info");
                        h && (g.wuv = d.getParameter(h.UNMASKED_VENDOR_WEBGL),
                        g.wur = d.getParameter(h.UNMASKED_RENDERER_WEBGL))
                    } catch (k) {}
                }
                return g
            },
            getBrowserMode: function() {
                return {
                    documentMode: document.documentMode,
                    compatMode: document.compatMode
                }
            },
            getSupportFonts: function() {
                function g(p) {
                    var q = {};
                    c.style.fontFamily = p;
                    document.body.appendChild(c);
                    q.height = c.offsetHeight;
                    q.width = c.offsetWidth;
                    document.body.removeChild(c);
                    return q
                }
                function f(p) {
                    for (var q = 0; q < e.length; q++) {
                        var t = g(p + "," + b[q])
                          , u = e[q];
                        if (t.height !== u.height || t.width !== u.width)
                            return !0
                    }
                    return !1
                }
                var d = []
                  , a = "Abadi MT Condensed Light;Adobe Fangsong Std;Adobe Hebrew;Adobe Ming Std;Agency FB;Arab;Arabic Typesetting;Arial Black;Batang;Bauhaus 93;Bell MT;Bitstream Vera Serif;Bodoni MT;Bookman Old Style;Braggadocio;Broadway;Calibri;Californian FB;Castellar;Casual;Centaur;Century Gothic;Chalkduster;Colonna MT;Copperplate Gothic Light;DejaVu LGC Sans Mono;Desdemona;DFKai-SB;Dotum;Engravers MT;Eras Bold ITC;Eurostile;FangSong;Forte;Franklin Gothic Heavy;French Script MT;Gabriola;Gigi;Gisha;Goudy Old Style;Gulim;GungSeo;Haettenschweiler;Harrington;Hiragino Sans GB;Impact;Informal Roman;KacstOne;Kino MT;Kozuka Gothic Pr6N;Lohit Gujarati;Loma;Lucida Bright;Lucida Fax;Magneto;Malgun Gothic;Matura MT Script Capitals;Menlo;MingLiU-ExtB;MoolBoran;MS PMincho;MS Reference Sans Serif;News Gothic MT;Niagara Solid;Nyala;Palace Script MT;Papyrus;Perpetua;Playbill;PMingLiU;Rachana;Rockwell;Sawasdee;Script MT Bold;Segoe Print;Showcard Gothic;SimHei;Snap ITC;TlwgMono;Tw Cen MT Condensed Extra Bold;Ubuntu;Umpush;Univers;Utopia;Vladimir Script;Wide Latin".split(";")
                  , b = ["monospace", "sans-serif", "serif"]
                  , e = []
                  , c = document.createElement("span");
                c.style.fontSize = "72px";
                c.style.visibility = "hidden";
                c.innerHTML = "mmmmmmmmmmlli";
                for (var h = 0; h < b.length; h++)
                    e[h] = g(b[h]);
                for (h = 0; h < a.length; h++) {
                    var k = a[h];
                    f(k) && d.push(k)
                }
                return d
            },
            getFeature: function() {
                var g = {}, f = [], d;
                for (d in navigator)
                    "object" != typeof navigator[d] && (g[d] = navigator[d]),
                    f.push(d);
                g.enumerationOrder = f;
                g.javaEnabled = navigator.javaEnabled();
                try {
                    g.taintEnabled = navigator.taintEnabled()
                } catch (a) {}
                return g
            },
            getPlugins: function() {
                var g = [], f = "4game;AdblockPlugin;AdobeExManCCDetect;AdobeExManDetect;Alawar NPAPI utils;Aliedit Plug-In;Alipay Security Control 3;AliSSOLogin plugin;AmazonMP3DownloaderPlugin;AOL Media Playback Plugin;AppUp;ArchiCAD;AVG SiteSafety plugin;Babylon ToolBar;Battlelog Game Launcher;BitCometAgent;Bitdefender QuickScan;BlueStacks Install Detector;CatalinaGroup Update;Citrix ICA Client;Citrix online plug-in;Citrix Receiver Plug-in;Coowon Update;DealPlyLive Update;Default Browser Helper;DivX Browser Plug-In;DivX Plus Web Player;DivX VOD Helper Plug-in;doubleTwist Web Plugin;Downloaders plugin;downloadUpdater;eMusicPlugin DLM6;ESN Launch Mozilla Plugin;ESN Sonar API;Exif Everywhere;Facebook Plugin;File Downloader Plug-in;FileLab plugin;FlyOrDie Games Plugin;Folx 3 Browser Plugin;FUZEShare;GDL Object Web Plug-in 16.00;GFACE Plugin;Ginger;Gnome Shell Integration;Google Earth Plugin;Google Earth Plug-in;Google Gears 0.5.33.0;Google Talk Effects Plugin;Google Update;Harmony Firefox Plugin;Harmony Plug-In;Heroes & Generals live;HPDetect;Html5 location provider;IE Tab plugin;iGetterScriptablePlugin;iMesh plugin;Kaspersky Password Manager;LastPass;LogMeIn Plugin 1.0.0.935;LogMeIn Plugin 1.0.0.961;Ma-Config.com plugin;Microsoft Office 2013;MinibarPlugin;Native Client;Nitro PDF Plug-In;Nokia Suite Enabler Plugin;Norton Identity Safe;npAPI Plugin;NPLastPass;NPPlayerShell;npTongbuAddin;NyxLauncher;Octoshape Streaming Services;Online Storage plug-in;Orbit Downloader;Pando Web Plugin;Parom.TV player plugin;PDF integrado do WebKit;PDF-XChange Viewer;PhotoCenterPlugin1.1.2.2;Picasa;PlayOn Plug-in;QQ2013 Firefox Plugin;QQDownload Plugin;QQMiniDL Plugin;QQMusic;RealDownloader Plugin;Roblox Launcher Plugin;RockMelt Update;Safer Update;SafeSearch;Scripting.Dictionary;SefClient Plugin;Shell.UIHelper;Silverlight Plug-In;Simple Pass;Skype Web Plugin;SumatraPDF Browser Plugin;Symantec PKI Client;Tencent FTN plug-in;Thunder DapCtrl NPAPI Plugin;TorchHelper;Unity Player;Uplay PC;VDownloader;Veetle TV Core;VLC Multimedia Plugin;Web Components;WebKit-integrierte PDF;WEBZEN Browser Extension;Wolfram Mathematica;WordCaptureX;WPI Detector 1.4;Yandex Media Plugin;Yandex PDF Viewer;YouTube Plug-in;zako".split(";"), d = navigator.userAgent.toLowerCase(), a;
                if (a = d.match(/rv:([\d.]+)\) like gecko/))
                    var b = a[1];
                if (a = d.match(/msie ([\d.]+)/))
                    b = a[1];
                if (b)
                    for (d = "AcroPDF.PDF;Adodb.Stream;AgControl.AgControl;DevalVRXCtrl.DevalVRXCtrl.1;MacromediaFlashPaper.MacromediaFlashPaper;Msxml2.DOMDocument;Msxml2.XMLHTTP;PDF.PdfCtrl;QuickTime.QuickTime;QuickTimeCheckObject.QuickTimeCheck.1;RealPlayer;RealPlayer.RealPlayer(tm) ActiveX Control (32-bit);RealVideo.RealVideo(tm) ActiveX Control (32-bit);rmocx.RealPlayer G2 Control;Scripting.Dictionary;Shell.UIHelper;ShockwaveFlash.ShockwaveFlash;SWCtl.SWCtl;TDCCtl.TDCCtl;WMPlayer.OCX".split(";"),
                    b = 0; b < d.length; b++) {
                        var e = d[b];
                        try {
                            var c = new ActiveXObject(e);
                            a = {};
                            a.name = e;
                            try {
                                a.version = c.GetVariable("$version")
                            } catch (h) {}
                            try {
                                a.version = c.GetVersions()
                            } catch (h) {}
                            a.version && 0 < a.version.length || (a.version = "");
                            g.push(a)
                        } catch (h) {}
                    }
                else {
                    d = navigator.plugins;
                    a = {};
                    for (b = 0; b < d.length; b++)
                        e = d[b],
                        a[e.name] = 1,
                        g.push(m(e));
                    for (b = 0; b < f.length; b++)
                        c = f[b],
                        a[c] || (e = d[c],
                        e && g.push(m(e)))
                }
                return g
            },
            getScreenInfo: function() {
                for (var g = {}, f = "availHeight availWidth colorDepth bufferDepth deviceXDPI deviceYDPI height width logicalXDPI logicalYDPI pixelDepth updateInterval".split(" "), d = 0; f.length > d; d++) {
                    var a = f[d];
                    void 0 !== screen[a] && (g[a] = screen[a])
                }
                return g
            },
            getPositionInfo: function() {
                for (var g = {}, f = ["devicePixelRatio", "screenTop", "screenLeft"], d = 0; f.length > d; d++) {
                    var a = f[d];
                    void 0 !== window[a] && (g[a] = window[a])
                }
                return g
            },
            getStoreCheck: function() {
                var g = {};
                try {
                    g.cookie = navigator.cookieEnabled,
                    g.localStorage = !!window.localStorage,
                    g.sessionStorage = !!window.sessionStorage,
                    g.globalStorage = !!window.globalStorage,
                    g.indexedDB = !!window.indexedDB
                } catch (f) {}
                return g
            }
        }
    }();
    return {
        getEncryptedCollectInfo: function() {
            var g = l;
            g = g || {};
            var f = {}
              , d = new Date;
            f.ts = {};
            f.ts.deviceTime = d.getTime();
            g[collectConfig.env.canvas] || (f.ca = n.execute("getCanvasInfo") || {});
            g[collectConfig.env.browserMode] || (f.m = n.execute("getBrowserMode") || {});
            g[collectConfig.env.fonts] || (f.fo = n.execute("getSupportFonts") || []);
            g[collectConfig.env.feature] || (f.n = n.execute("getFeature") || {});
            g[collectConfig.env.plugins] || (f.p = n.execute("getPlugins") || []);
            g[collectConfig.env.position] || (f.w = n.execute("getPositionInfo") || {});
            g[collectConfig.env.screen] || (f.s = n.execute("getScreenInfo") || {});
            g[collectConfig.env.color] || (f.sc = n.execute("getColorRgb") || {});
            g[collectConfig.env.storeCheck] || (f.ss = n.execute("getStoreCheck") || {});
            f.tz = d.getTimezoneOffset();
            f.lil = "";
            f.wil = "";
            f.ts.deviceEndTime = (new Date).getTime();
            jdtRiskContext.d && console.log("collect env data :", f);
            return jdtRiskEncryptUtil.TDEncrypt(f)
        }
    }
};
(function() {
    try {
        if (jdtRiskUtil.isDegrade()) {
            var l = jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].jsTokenKey)
              , m = jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].fpKey, !1);
            if (jdtRiskUtil.isValidJsToken(l)) {
                jdtRiskContext.deviceInfo.jsToken = l;
                jdtRiskContext.deviceInfo.fp = m;
                jdtRiskContext.isJsTokenFinished = !0;
                return
            }
        }
    } catch (b) {}
    try {
        jdtRiskContext.deviceInfo.jsToken = jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].jsTokenKey); // 生成x-api-eid-token
        (new JdtRiskFingerPrint(collectConfig.getFpExcludeOptions(_riskFpMode))).getFp(function(b) {
            b && (jdtRiskContext.deviceInfo.fp = b)
        });
        var n = (new TDEnvCollector(collectConfig.getEnvExcludeOptions(_riskFpMode))).getEncryptedCollectInfo();
        l = "string" === typeof orderId ? orderId : "";
        m = "undefined" !== typeof jdfp_pinenp_ext && jdfp_pinenp_ext ? 2 : 1;
        var g = {
            pin: jdtRiskUtil.obtainPin(m),
            oid: l,
            bizId: jdtRiskUtil.getBizId(),
            fc: jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].eidKey),
            mode: _riskFpMode,
            p: "https:" == document.location.protocol ? "s" : "h",
            fp: jdtRiskContext.deviceInfo.fp,
            ctype: m,
            v: jdtRiskContext.version,
            f: "1",
            o: jdtRiskUtil.getCurrentPageUrl(),
            qs: jdtRiskUtil.getUrlQueryStr(),
            jsTk: jdtRiskContext.deviceInfo.jsToken
        };
        try {
            if ("undefined" != typeof gia_fp_qd_uuid && 0 <= gia_fp_qd_uuid.length)
                g.qi = gia_fp_qd_uuid;
            else {
                var f = jdtRiskCookieManager.getCookie("qd_uid");
                g.qi = void 0 == f ? "" : f
            }
        } catch (b) {}
        var d = jdtRiskEncryptUtil.TDEncrypt(g);
        n = "d=" + n;
        var a = jdtRiskUtil.getCurrentPageProtocol() + jdtRiskUtil.getFpServerDomain() + "/jsTk.do?a=" + d;
        jdtRiskUtil.sendRequest(a, n, function(b) {
            try {
                var e = JSON.parse(b);
                if (e && 0 == e.code && e.data) {
                    jdtRiskContext.deviceInfo.jsToken = e.data.token;
                    jdtRiskStorageManager.store(collectConfig.store[_riskFpMode].jsTokenKey, e.data.token);
                    jdtRiskContext.deviceInfo.eid = e.data.eid;
                    jdtRiskStorageManager.store(collectConfig.store[_riskFpMode].eidKey, e.data.eid);
                    try {
                        e.data.gia_d && 1 == e.data.gia_d && jdtRiskCookieManager.setCookie(collectConfig.store.giaDKey, e.data.gia_d, e.data.ds || 600),
                        e.data.deMap && jdtRiskUtil.cleanAndPushDeS(jdtRiskUtil.getBizId(), e.data.deMap[jdtRiskUtil.getBizId()])
                    } catch (c) {}
                }
                jdtRiskContext.isJsTokenFinished = !0
            } catch (c) {
                console.error("resp parse error", c)
            }
        })
    } catch (b) {
        console.error("init func error :", b)
    }
}
)();
function __getTkResult() {
    var l = {
        jsToken: jdtRiskContext.deviceInfo.jsToken,
        fp: jdtRiskContext.deviceInfo.fp
    };
    l.jsToken = l.jsToken || jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].jsTokenKey);
    l.fp = l.fp || jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].fpKey, !1) || jdtRiskUtil.randomStr(32);
    jdtRiskUtil.isValidJsToken(l.jsToken) && (jdtRiskContext.isJsTokenFinished = !0);
    return l
}
function __callbackWrapper(l, m) {
    l && l(m)
}
function getJsToken(l, m) {
    m = m || 3E3;
    var n = __getTkResult();
    if (0 >= m || 50 >= m || jdtRiskContext.isReady())
        __callbackWrapper(l, n);
    else
        var g = Math.ceil(1 * m / 50)
          , f = 1
          , d = setInterval(function() {
            f++;
            if (jdtRiskContext.isReady() || f > g)
                n = __getTkResult(),
                clearInterval(d),
                __callbackWrapper(l, n)
        }, 50)
}
function getJdEid(l, m, n) {
    m = 50 * (n || 60);
    var g = __getTkResult()
      , f = {};
    if (0 >= m || 50 >= m || jdtRiskContext.isReady())
        m = jdtRiskContext.deviceInfo.eid || jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].eidKey),
        f.fp = g.fp,
        f.eid = m,
        l(m, g.fp, f);
    else
        var d = Math.ceil(1 * m / 50)
          , a = 1
          , b = setInterval(function() {
            a++;
            if (jdtRiskContext.isReady() || a > d) {
                clearInterval(b);
                g = __getTkResult();
                var e = jdtRiskContext.deviceInfo.eid || jdtRiskStorageManager.load(collectConfig.store[_riskFpMode].eidKey);
                f.fp = g.fp;
                f.eid = e;
                l(e, g.fp, f)
            }
        }, 50)
}
;