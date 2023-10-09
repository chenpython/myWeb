function n() {
    function t(t) {
        function i() {
            k.onmousedown = null,
            c.removeEvt(f, "mousemove", s),
            c.removeEvt(f, "mouseup", d),
            c.removeEvt(f, "touchmove", g),
            c.removeEvt(f, "touchend", p),
            c.removeEvt(k, "touchstart", r);
            var t = {};
            t.btn = k,
            t.bar = w.childNodes[1],
            C.className += " nc-align-center scale_text2",
            C.innerHTML = '<span class="nc-lang-cnt" ><b>' + l.getLanuage(e, "LOADING") + "</b></span>" + a(),
            m()
        }
        function s(e) {
            x || (x = !0);
            var t = (e || u.event).clientX
              , a = Math.min(S, Math.max(-2, R + (t - v)));
            if (k.style.left = a + "px",
            n(Math.round(100 * Math.max(0, a / S)), a),
            t >= N + w.offsetWidth && (a < S || t - R < S))
                return void d.call(this);
            var s = c.getClientRect(k).left;
            a !== S && t - s - y !== S || i()
        }
        function d() {
            parseInt(k.style.left) < S && (c.addClass(k, "button_move"),
            c.addClass(b, "bg_move"),
            k.style.left = "0px",
            n(0, 0),
            setTimeout(function() {
                c.removeClass(k, "button_move"),
                c.removeClass(b, "bg_move")
            }, 500)),
            c.removeEvt(this, "touchmove", g),
            c.removeEvt(f, "touchmove", g),
            c.removeEvt(f, "mousemove", s),
            c.removeEvt(f, "mouseup", d)
        }
        function p(e) {
            d.call(this, e.touches[0])
        }
        function g(e) {
            e.preventDefault(),
            s.call(this, e.touches[0])
        }
        try {
            var h = document.getElementsByClassName("nc_iconfont btn_slide")
              , _ = h && h[0] && h[0].getBoundingClientRect ? h[0].getBoundingClientRect() : {
                x: "",
                y: "",
                width: "",
                height: "",
                top: "",
                bottom: "",
                left: "",
                right: ""
            };
            o.options.trans = o.options.trans || {},
            o.options.trans.ncbtn = _.x + "|" + _.y + "|" + _.width + "|" + _.height + "|" + _.top + "|" + _.bottom + "|" + _.left + "|" + _.right
        } catch (t) {
            o.options.trans.ncbtn = "|||||||"
        }
        o.__fy.fyObj.startRecord();
        var x = !1
          , v = (t || u.event).clientX
          , y = k.offsetWidth
          , S = w.offsetWidth - y
          , R = k.offsetLeft
          , N = c.getClientRect(w).left;
        c.addHandler(f, "mousemove", s),
        c.addHandler(f, "mouseup", d),
        c.addHandler(f, "touchmove", g),
        c.addHandler(f, "touchend", p)
    }
    function n(e, t) {
        S.style.width = Math.max(0, t) + k.offsetWidth / 2 + "px"
    }
    function r(e) {
        e.preventDefault(),
        t.call(this, e.touches[0])
    }
    function d(e) {
        for (var t = e.offsetLeft, n = e.offsetParent; null !== n; )
            t += n.offsetLeft,
            n = n.offsetParent;
        return t
    }
    function h(e) {
        for (var t = e.offsetTop, n = e.offsetParent; null !== n; )
            t += n.offsetTop,
            n = n.offsetParent;
        return t
    }
    function m() {
        function t() {
            s++,
            a.n = o.__fy.getFYToken(o.__fy_options),
            (-1 == a.n.indexOf("default") || s > 50) && r ? (r = !1,
            setTimeout(function() {
                if (-1 != a.n.indexOf("default") && e.reportUrl && c.getNCPunish(e, "fyDefault", a.n),
                e.noRequest)
                    _(a);
                else {
                    var t = {
                        url: p.URL[e.foreign ? "us" : "cn"].analyze,
                        callback: "callback",
                        data: a,
                        success: function(e) {
                            x(e)
                        },
                        fail: function() {
                            i(g)
                        }
                    };
                    if (e.replaceCallback) {
                        var n = "";
                        n += c.obj2param(t.data);
                        t.url,
                        t.url.indexOf("?");
                        e.replaceCallback(t)
                    } else
                        c.jsonp(t)
                }
            }, 1),
            clearInterval(l)) : !r && l && clearInterval(l)
        }
        var n = (new Date,
        e.trans || {});
        n.umidToken = o.__fy.getUidToken();
        try {
            n.ncSessionID = function(e) {
                return parseInt(e.offsetWidth + "a" + e.offsetHeight + "a" + d(e) + "a" + h(e), 11).toString(16)
            }(f.getElementById("nc_" + o.wrapperId + "_n1t"))
        } catch (e) {
            n.ncSessionID = "0"
        }
        var a = {
            a: e.appkey,
            t: e.token,
            n: o.__fy.getFYToken(o.__fy_options),
            p: c.obj2str(n),
            scene: e.scene || "",
            asyn: 0,
            lang: e.language,
            v: p.jsv
        }
          , s = 0
          , r = !0;
        t();
        var l = setInterval(t, 20)
    }
    function _(t) {
        k.className = "nc_iconfont btn_ok",
        k.innerHTML = "&#xe60b;",
        C.innerHTML = '<span class="nc-lang-cnt" data-nc-lang="SLIDE"><b>' + l.getLanuage(e, "SUCCESS") + "</b></span>",
        e.success && e.success(t)
    }
    function x(t) {
        if (t.success) {
            if (0 === t.result.code) {
                k.className = "nc_iconfont btn_ok",
                k.innerHTML = "&#xe60b;",
                C.innerHTML = '<span class="nc-lang-cnt" data-nc-lang="SLIDE"><b>' + l.getLanuage(e, "SUCCESS") + "</b></span>";
                var n = {
                    sig: t.result.value,
                    sessionId: t.result.csessionid,
                    token: e.token
                };
                e.success && e.success(n)
            } else if (300 === t.result.code || 69634 === t.result.code || 8778 === t.result.code) {
                var a = function(e, t, n) {
                    for (var i = 0, a = t, s = e.length; a < s; )
                        i <<= 3,
                        i += e.charCodeAt(a),
                        a += n;
                    i < 0 && (i = 0 - i);
                    for (var o = "0123456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ", r = ""; i >= 58; ) {
                        var c = i % 58;
                        r = o[c] + r,
                        i = (i - c) / 58
                    }
                    r += o[(new Date).getDate()];
                    var l = r.length;
                    return l > 6 && (r = r.substr(l - 6, l - 1)),
                    r
                }(e.token, 0, 1);
                8778 === t.result.code ? s(a, 1) : s(a, 0)
            }
        } else
            i(t.success)
    }
    o.nc_wrapper.innerHTML = "";
    var v = f.createElement("div");
    v.id = "nc_" + o.wrapperId + "_n1t",
    v.className = "nc_scale";
    var b = f.createElement("div");
    b.id = "nc_" + o.wrapperId + "__bg",
    b.className = "nc_bg",
    b.style.width = "0px",
    v.appendChild(b);
    var y = f.createElement("span");
    y.id = "nc_" + o.wrapperId + "_n1z",
    y.className = "nc_iconfont btn_slide",
    y.ariaLabel = "\u6ed1\u5757",
    y.tabIndex = 0,
    y.role = "button",
    y.style.left = "0px",
    y.innerHTML = "\ue601",
    v.appendChild(y);
    var C = f.createElement("div");
    C.id = "nc_" + o.wrapperId + "__scale_text",
    C.className = "scale_text slidetounlock",
    C.innerHTML = '<span class="nc-lang-cnt"  data-nc-lang="SLIDE">' + l.getLanuage(e, "SLIDE") + "</span>",
    v.appendChild(C),
    o.nc_wrapper.appendChild(v);
    var w = v
      , k = y
      , S = w.getElementsByTagName("DIV")[0];
    k.onmousedown = t,
    c.addHandler(k, "touchstart", r),
    w.onselectstart = function() {
        return !1
    }
}