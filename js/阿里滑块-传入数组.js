function(e, t, n) {
            "use strict";
            !function(e) {
                var t = "_nc_initialized";
                if (!e[t]) {
                    e[t] = 1;
                    var o = n(5).v;
                    window.console || (window.console = {
                        log: function() {
                            return 0
                        }
                    }),
                    n(71),
                    n(73),
                    n(69),
                    n(72);
                    var i = e.pointman && "19" == pointman._z
                      , r = {}
                      , a = {
                        has_pointman: i,
                        index: 0,
                        js_type: "pc",
                        v: o
                    };
                    e.UA_Opt = e.UA_Opt || {};
                    var c = n(74).makeNC(r, a);
                    c.v = o,
                    r.init = function() {}
                    ,
                    a.has_pointman && (r.noCaptcha = c,
                    pointman.define("nc", function() {
                        return r
                    })),
                    e.noCaptcha = c
                }
            }(window)
        }