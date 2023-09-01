const cheerio = require('cheerio');
var fs = require('fs');
var path = require("path");

window = global;
Object.defineProperties(window, {
    [Symbol.toStringTag]: {
        value: 'Window',
        configurable: true
    }
});


function getHtmlContent(html_text) {
    const $ = cheerio.load(html_text,);
    const metaContents = [];
    $('meta').each((index, element) => {
        const content = $(element)[0].attribs['content'];
        if (content) {
            metaContents.push(content);
        }
    });
    var content = metaContents[1];
    return content;
};

// 跟踪变量调试
proxy = function (obj) {
    // 基础类型不挂代理监控
    if (typeof obj !== 'object' || obj === null) {
        return obj;
    }

    var proxy_obj = new Proxy(obj, {
        set(target, prop, value) {
            if (prop == "cookie") {
                debugger;
            }
            console.log('设置 %s 的属性：%s 值为：%s', target[Symbol.toStringTag], prop, value);
            return Reflect.set(...arguments);
        },
        // target: 目标对象
        // prop：属性名称
        // prop：属性值
        get(target, prop, receiver) {
            if (prop == "cookie") {
                debugger;
            }
            console.log('获取 %s 的属性：%s 值为：%s', target[Symbol.toStringTag], prop, target[prop]);
            return target[prop];
        },

    });
    return proxy_obj;
};


var home_html_path = '/cde/1_.htm';
var link_js = '/cde/link.js';
var cookiePath = '/home/feng/workspace/myWeb/cde/cookie';


var file_path = path.join(path.dirname(__dirname), home_html_path);
var res = fs.readFileSync(file_path, { encoding: 'utf8', flag: 'r' });
data = res.toString()

js_content = fs.readFileSync(path.join(path.dirname(__dirname), link_js), { encoding: 'utf8', flag: 'r' }).toString();


location = {
    "ancestorOrigins": {},
    "href": "http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml",
    "origin": "http://www.chinadrugtrials.org.cn",
    "protocol": "http:",
    "host": "www.chinadrugtrials.org.cn",
    "hostname": "www.chinadrugtrials.org.cn",
    "port": "",
    "pathname": "/clinicaltrials.searchlist.dhtml",
    "search": "",
    "hash": ""
};


Object.defineProperties(location, {
    [Symbol.toStringTag]: {
        value: 'location',
        configurable: true
    }
});
location = proxy(location);

function addEventListener(type, listener) {
    console.log("addEventListener -> type: " + type + " listener: " + listener);
};

function getAttribute(attributeName) {
    var result;

    switch (attributeName) {
        case "r":
            result = "m";
            break;
        case "selenium":
            result = null;
            break;
        case "driver":
            result = null;
            break;
        case "webdriver":
            result = null;
            break;
    }
    console.log("getAttribute " + attributeName + " -> " + result);
    return result;
};

function removeChild(child) {
    console.log("removeChild -> " + child);
};


function getElementsByTagName(name) {

    var result = [];
    Object.defineProperties(result, {
        [Symbol.toStringTag]: {
            value: 'HTMLCollection',
            configurable: true
        }
    });
    switch (name) {
        case "meta":
            var headElem = { removeChild: removeChild };
            Object.defineProperties(headElem, {
                [Symbol.toStringTag]: {
                    value: 'HTMLHeadElement',
                    configurable: true
                }
            });
            var metaElem = { content: window.content, getAttribute: getAttribute, parentNode: headElem };
            Object.defineProperties(metaElem, {
                [Symbol.toStringTag]: {
                    value: 'HTMLMetaElement ',
                    configurable: true
                }
            });
            result[0] = metaElem;
            break;
        case "script":
            var headElem = { removeChild: removeChild };
            Object.defineProperties(headElem, {
                [Symbol.toStringTag]: {
                    value: 'HTMLHeadElement',
                    configurable: true
                }
            });

            var ele = { getAttribute: getAttribute, parentElement: headElem };
            Object.defineProperties(ele, {
                [Symbol.toStringTag]: {
                    value: 'HTMLScriptElement',
                    configurable: true
                }
            });

            result[0] = ele;
            result[1] = ele;
            break;
    }
    console.log("getElementsByTagName " + name + "-> " + result);
    result = proxy(result);
    return result;
};

function appendChild(aChild) {
    if (this.children) {
        this.children.push(aChild);
    }
    console.log("appendChild  -> " + aChild);
};

htmlFormatElement = function HTMLFormElement() {
    throw TypeError('Ilegal constructor')
};
Object.defineProperties(htmlFormatElement.prototype, {
    [Symbol.toStringTag]: {
        value: 'htmlFormatElement',
        configurable: true
    },
    action: {
        set(v) {
            this.attributes['action'] = v;
        },
        get() {
            var i;
            for (i = 0; i < this.children.length; i++) {
                var child = this.children[i];
                if (child.name == 'action' || child.id == 'action') {
                    return child;
                }
            };
            return this.attributes['action'];
        }
    },
    innerText: {
        set(v) {
            this.attributes['innerText'] = v;
        },
        get() {
            var i;
            for (i = 0; i < this.children.length; i++) {
                var child = this.children[i];
                if (child.name == 'innerText' || child.id == 'innerText') {
                    return child;
                }
            };
            return this.attributes['innerText'];
        }
    },
    textContent: {
        set(v) {
            this.attributes['textContent'] = v;
        },
        get() {
            var i;
            for (i = 0; i < this.children.length; i++) {
                var child = this.children[i];
                if (child.name == 'textContent' || child.id == 'textContent') {
                    return child;
                }
            };
            return this.attributes['textContent'];
        }
    },
    id: {
        set(v) {
            this.attributes['id'] = v;
        },
        get() {
            var i;
            for (i = 0; i < this.children.length; i++) {
                var child = this.children[i];
                if (child.name == 'id' || child.id == 'id') {
                    return child;
                }
            };
            return this.attributes['id'];
        }
    }
});
htmlFormatElement.prototype.children = [];
htmlFormatElement.prototype.attributes = {};

function createElement(tagName) {
    var result = {
        getElementsByTagName: getElementsByTagName,
        appendChild: appendChild
    };

    tagName = tagName.toLowerCase();
    switch (tagName) {
        case "div":
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'HTMLDivElement',
                    configurable: true
                }
            });
            break;
        case "a":
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'HTMLLinkElement',
                    configurable: true
                }
            });
            break;
        case "form":
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'HTMLFormElement',
                    configurable: true
                }
            });
            Object.setPrototypeOf(result, htmlFormatElement.prototype);
            break;
        case "input":
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'HTMLInputElement',
                    configurable: true
                }
            });
            break;
        default:
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'HTMLUnknownElement',
                    configurable: true
                }
            });
            break;
    }

    console.log("createElement " + tagName + "-> " + result);
    result = proxy(result);
    return result
};


style = {};
Object.defineProperties(style, {
    [Symbol.toStringTag]: {
        value: 'style',
        configurable: true
    }
});
style = proxy(style);

documentElement = { style: style, getAttribute: getAttribute };
Object.defineProperties(documentElement, {
    [Symbol.toStringTag]: {
        value: 'HTMLHtmlElement',
        configurable: true
    }
});
documentElement = proxy(documentElement);


function getElementById(id) {
    var result = null;
    switch (id) {
        case "9DhefwqGPrzGxEp9hPaoag":
            var headNode = { removeChild: removeChild };
            Object.defineProperties(headNode, {
                [Symbol.toStringTag]: {
                    value: 'HTMLHeadElement',
                    configurable: true
                }
            });
            result = { content: window.content, parentNode: headNode };
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'HTMLMetaElement ',
                    configurable: true
                }
            });

    }
    console.log("getElementById " + id + "-> " + result);
    return result;
}

function addEventListener(element, type, listener) {
    console.log("addEventListener -> " + type);
    return null;
}

function createExpression(xpathText, namespaceURLMapper) {
    var result = null;
    switch (xpathText) {
        case "//html":
            var result = {};
            Object.defineProperties(result, {
                [Symbol.toStringTag]: {
                    value: 'XPathExpression',
                    configurable: true
                }
            });
            break;
    }
    console.log("createExpression " + xpathText + " -> " + result);
    result = proxy(result);
    return result;
};


html = {};
Object.defineProperties(html, {
    [Symbol.toStringTag]: {
        value: 'HTMLHtmlElement',
        configurable: true
    }
});
head = {};
Object.defineProperties(head, {
    [Symbol.toStringTag]: {
        value: 'HTMLHeadElement',
        configurable: true
    }
});
meta = {};
Object.defineProperties(meta, {
    [Symbol.toStringTag]: {
        value: 'HTMLMetaElement',
        configurable: true
    }
});
title = {};
Object.defineProperties(title, {
    [Symbol.toStringTag]: {
        value: 'HTMLTitleElement',
        configurable: true
    }
});
documentAll = [
    html, head, meta, meta, title
]
Object.defineProperties(documentAll, {
    [Symbol.toStringTag]: {
        value: 'HTMLAllCollection',
        configurable: true
    }
});
document = {
    createElement: createElement,
    getElementsByTagName: getElementsByTagName,
    cookie: "",
    documentElement: documentElement,
    getElementById: getElementById,
    addEventListener: addEventListener,
    createExpression: createExpression,
    visibilityState: 'hidden',
    body: null,
    removeChild: removeChild,
    appendChild: appendChild,
    all: documentAll,
    characterSet: 'UTF-8'
};
Object.defineProperties(document, {
    [Symbol.toStringTag]: {
        value: 'document',
        configurable: true
    }
});
document = proxy(document);


function removeItem(keyName) {
    delete this[keyName];
    console.log("removeItem -> ", keyName);
};

function getItem(keyName) {
    var result = this[keyName];
    if (result == undefined) {
        result = null;
    }
    console.log("getItem " + keyName + "-> " + result);
    return result;
};

function setItem(keyName, value) {
    this[keyName] = value;
    console.log("setItem " + keyName + "-> " + value);
};


localStorage = {
    removeItem: removeItem,
    getItem: getItem,
    setItem: setItem
};
Object.defineProperties(localStorage, {
    [Symbol.toStringTag]: {
        value: 'localStorage',
        configurable: true
    }
});
localStorage = proxy(localStorage);

sessionStorage = { getItem: getItem, setItem: setItem };
Object.defineProperties(sessionStorage, {
    [Symbol.toStringTag]: {
        value: 'sessionStorage',
        configurable: true
    }
});
sessionStorage = proxy(sessionStorage);

mimeTypes = [];
Object.defineProperties(mimeTypes, {
    [Symbol.toStringTag]: {
        value: 'MimeTypeArray',
        configurable: true
    }
});
mimeTypes = proxy(mimeTypes);


DeprecatedStorageQuota = {};
Object.defineProperties(DeprecatedStorageQuota, {
    [Symbol.toStringTag]: {
        value: 'DeprecatedStorageQuota',
        configurable: true
    }
});

NetworkInformation = {};
Object.defineProperties(NetworkInformation, {
    [Symbol.toStringTag]: {
        value: 'NetworkInformation',
        configurable: true
    }
});

getOwnPropertyDescriptorOrg = Object.getOwnPropertyDescriptor;
Object.getOwnPropertyDescriptor = function getOwnPropertyDescriptor(obj, prop) {
    if (obj[Symbol.toStringTag] == 'navigator' && prop == 'webdriver') {
        return;
    }
    return getOwnPropertyDescriptorOrg(obj, prop);

}


Navigator = function Navigator() {
    throw TypeError("Illegal constructor");
};
Navigator.prototype.webdriver = false;


toStringOrg = Object.toString;
function myToString() {
    return "function get webdriver() { [native code] }";
};
function webdriver() { return false };
webdriver.toString = myToString;

Object.defineProperties(Navigator.prototype, {
    [Symbol.toStringTag]: {
        value: 'Navigator',
        configurable: true
    },
    webdriver: {
        configurable: true,
        enumerable: true,
        get: webdriver,
        set: undefined
    },

});

navigator = {
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    mimeTypes: mimeTypes,
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    webkitPersistentStorage: DeprecatedStorageQuota,
    languages: ['zh-CN'],
    platform: "Win32",
    maxTouchPoints: 0,
    connection: NetworkInformation,
    // [Symbol.toPrimitive]:{
    //     value: "getOwnPropertyDescriptor"
    // }
};

Object.setPrototypeOf(navigator, Navigator.prototype);
navigator = proxy(navigator);

function open(a, b) {
    var result = undefined;
    if (a == "EkcP" && b == 1) {
        result = {};
        Object.defineProperties(result, {
            [Symbol.toStringTag]: {
                value: 'IDBOpenDBRequest',
                configurable: true
            }
        });
    }

    console.log("open " + a + " " + b + "-> " + result);
    return result;
}

indexedDB = {
    open: open
};
Object.defineProperties(indexedDB, {
    [Symbol.toStringTag]: {
        value: 'IDBFactory',
        configurable: true
    }
});
indexedDB = proxy(indexedDB);


DOMParser = function DOMParser() {
    debugger;
};
Object.defineProperties(DOMParser, {
    [Symbol.toStringTag]: {
        value: 'DOMParser',
        configurable: true
    }
});
DOMParser = proxy(DOMParser);

function webkitRequestFileSystem() {
    var result = null;
    console.log("webkitRequestFileSystem -> " + result);
    return result;
};

MutationObserver = function MutationObserver(callback) {
    var result = {
        observe: observe
    };
    Object.defineProperties(result, {
        [Symbol.toStringTag]: {
            value: 'MutationObserver',
            configurable: true
        }
    });
    console.log("MutationObserver callback: " + callback + " -> " + result);
    return result;
};

function observe(target, options) {
    var result = undefined;
    console.log("observe " + target + "-> " + result);
    return result;
};

function xmlRequestOpen(method, url) {
    console.log("xmlRequestOpen  method", + method + " -> ", url);
};
function xmlRequestSend(body) {
    console.log("xmlRequestSend  -> ", body);
};

function XMLHttpRequest() {
    console.log("XMLHttpRequest -> ", null);
};

XMLHttpRequestResult = {
    open: xmlRequestOpen,
    send: xmlRequestSend
};
Object.defineProperties(XMLHttpRequestResult, {
    [Symbol.toStringTag]: {
        value: 'XMLHttpRequest',
        configurable: true
    }
});

XMLHttpRequest.prototype = XMLHttpRequestResult;

WebKitMutationObserver = {
    observe: observe
};
Object.defineProperties(WebKitMutationObserver, {
    [Symbol.toStringTag]: {
        value: 'WebKitMutationObserver',
        configurable: true
    }
});

NodeList = [];
Object.defineProperties(NodeList, {
    [Symbol.toStringTag]: {
        value: 'NodeList',
        configurable: true
    }
});

MutationRecord = {
    type: "childList",
    addedNodes: NodeList
};
Object.defineProperties(MutationRecord, {
    [Symbol.toStringTag]: {
        value: 'MutationRecord',
        configurable: true
    }
});

chrome = {};


window.location = location;
window.localStorage = localStorage;
window.sessionStorage = sessionStorage;
window.addEventListener = addEventListener;
window.navigator = navigator;
window.name = '';
window.indexedDB = indexedDB;
window.DOMParser = DOMParser;
window.webkitRequestFileSystem = webkitRequestFileSystem;
window.WebKitMutationObserver = WebKitMutationObserver;
window.MutationObserver = MutationObserver;
window.open = open;
window.XMLHttpRequest = XMLHttpRequest;
window.MutationRecord = MutationRecord;
window.chrome = chrome;
window.clientInformation = navigator;
window.TEMPORARY = 0;

window.setTimeout = function setTimeout(code, delay) {
    if (code.toString().indexOf("debugger") == -1) {
        return code();
    }
};
window.setInterval = function setInterval(code, delay) { };

window = proxy(window);
window.top = window;
window.self = window;

content = getHtmlContent(data)
eval(js_content);

debugger;

function _$Gn() {
    return 5
}
function _$z9() {
    var _$wF = _$AL(_$Er())[_$q0()](_$Cf());
    for (var _$yB = 0; _$yB < _$wF.length; _$yB++)
        _$wF[_$yB] = _$GY(_$wF[_$yB]);
    return _$wF;
}
function _$sU(_$wF) {
    return function() {
        _$wF = (_$wF * 17405 + 40643) >> 9 & 0xFFFF;
        return _$wF;
    }
    ;
}
function _$zX() {
    return 15
}
function _$DH(_$wF) {
    var _$Ac = _$Gn();
    _$Ey = _$Bc();
    if (_$EU()) {
        _$wF[_$jK(_$FT(), 16)] = _$zX();
    }
    _$Gb(_$wF);
    return _$zX();
}
function _$pg(_$yB, _$ql) {
    for (var _$wF = 0; _$wF < _$ql.length; _$wF++) {
        _$HF[_$yQ(_$yB[_$wF])] = _$kp(_$ql[_$wF]);
    }
}
function _$nJ() {
    debugger ;
}
function _$BM(_$wF) {
    if (!_$G7)
        return;
    if (typeof _$wF === _$jV()) {
        _$wF = _$D1(_$wF);
    }
    _$wF = _$o0() + _$Ha(_$wF);
    return _$G7[_$wF];
}
function _$uX(_$ql, _$yB) {
    if (!_$G7)
        return;
    if (typeof _$ql === _$jV()) {
        _$ql = _$D1(_$ql);
    }
    var _$wF = _$BM(_$ql);
    if (_$wF)
        _$yB = _$GY(_$wF) + _$yB;
    _$ql = _$o0() + _$Ha(_$ql);
    _$G7[_$ql] = _$yB;
}
function _$kO() {
    return 4
}
function _$Fi(_$EB) {
    var _$Et = _$EB.length
      , _$vF = new _$G4(_$HB[_$my()](_$Et * 3 / 4));
    var _$ER, _$rn, _$Ew, _$EA;
    var _$Bw = 0
      , _$EM = 0
      , _$ql = _$Et - 3;
    var _$yB = _$yy();
    var _$DJ = _$yB[0]
      , _$yn = _$yB[1]
      , _$Ey = _$yB[2]
      , _$Ac = _$yB[3]
      , _$E4 = _$yB[4]
      , _$wF = _$yB[5];
    for (_$Bw = 0; _$Bw < _$ql; ) {
        _$ER = _$bB.call(_$EB, _$Bw++);
        _$rn = _$bB.call(_$EB, _$Bw++);
        _$Ew = _$bB.call(_$EB, _$Bw++);
        _$EA = _$bB.call(_$EB, _$Bw++);
        _$vF[_$EM++] = _$DJ[_$ER] | _$yn[_$rn];
        _$vF[_$EM++] = _$Ey[_$rn] | _$Ac[_$Ew];
        _$vF[_$EM++] = _$E4[_$Ew] | _$wF[_$EA];
    }
    if (_$Bw < _$Et) {
        _$ER = _$bB.call(_$EB, _$Bw++);
        _$rn = _$bB.call(_$EB, _$Bw++);
        _$vF[_$EM++] = _$DJ[_$ER] | _$yn[_$rn];
        if (_$Bw < _$Et) {
            _$Ew = _$bB.call(_$EB, _$Bw);
            _$vF[_$EM++] = _$Ey[_$rn] | _$Ac[_$Ew];
        }
    }
    return _$vF;
}
function _$wu(_$yB, _$wF) {
    var _$ql;
    return function(_$EB, _$Ac) {
        if (_$ql === _$HC) {
            _$ql = _$uh(_$yQ(_$yB), _$yQ(_$wF));
        }
        return _$ql;
    }
    ;
}
function _$F2(_$wF) {
    _$wF[_$jK(_$Bc(), 16)] = _$BU();
    var _$Ey = _$kO();
    _$EB = _$Fb();
    _$wF[0] = _$EK();
    return _$Fa();
}
function _$EU() {
    return 0
}
function _$fe(_$Ac, _$wF) {
    _$wF = _$Hm.call(_$w6(_$wF), '|');
    _$Ac = _$w6(_$Ac);
    var _$yB, _$ql = _$G8.call(_$Ac, 0, 2), _$EB;
    for (_$yB = 0; _$yB < _$wF.length; _$yB++) {
        _$EB = _$G8.call(_$Ac, 2 + _$yB * 2, 2);
        _$HF[_$ql + _$EB] = _$HF[_$wF[_$yB]];
    }
}
function _$rK() {
    return 10
}
function _$dW(_$yB) {
    var _$wF = arguments;
    return _$yB[_$dR()](/\{(.+?)\}/g, function(_$EB, _$ql) {
        return _$wF[_$GY(_$ql) + 1];
    });
}
function _$q3(_$ql) {
    _$ql = _$Hm.call(_$ql, _$tm());
    for (var _$wF = 0; _$wF < _$ql.length - 1; _$wF += 2) {
        var _$yB = _$ql[_$wF];
        _$ql[_$wF] = _$ql[_$wF + 1];
        _$ql[_$wF + 1] = _$yB;
    }
    return _$ql.join(_$tm());
}
function _$mt(_$wF) {
    for (var _$ql, _$yB, _$EB = _$wF.length - 1; _$EB > 0; _$EB--) {
        _$ql = _$HB[_$nz()](_$EC() * _$EB);
        _$yB = _$wF[_$EB];
        _$wF[_$EB] = _$wF[_$ql];
        _$wF[_$ql] = _$yB;
    }
    return _$wF;
}
function _$mR() {
    return _$CP(95, 36);
}
function _$AA() {
    var _$wF = _$Er();
    var _$yB = _$Er();
    _$wF = _$Hm.call(_$AL(_$wF), _$ET);
    _$yB = _$Hm.call(_$AL(_$yB), _$ET);
    _$y4(_$wF, _$yB);
}
function _$on(_$yB) {
    var _$wF = [], _$ql, _$EB, _$Ac, _$Ey = _$bB.call(_$mj(), 0);
    for (_$ql = 0; _$ql < _$yB.length; ) {
        _$EB = _$yB[_$ql];
        if (_$EB < 0x80) {
            _$Ac = _$EB;
        } else if (_$EB < 0xc0) {
            _$Ac = _$Ey;
        } else if (_$EB < 0xe0) {
            _$Ac = ((_$EB & 0x3F) << 6) | (_$yB[_$ql + 1] & 0x3F);
            _$ql++;
        } else if (_$EB < 0xf0) {
            _$Ac = ((_$EB & 0x0F) << 12) | ((_$yB[_$ql + 1] & 0x3F) << 6) | (_$yB[_$ql + 2] & 0x3F);
            _$ql += 2;
        } else if (_$EB < 0xf8) {
            _$Ac = _$Ey;
            _$ql += 3;
        } else if (_$EB < 0xfc) {
            _$Ac = _$Ey;
            _$ql += 4;
        } else if (_$EB < 0xfe) {
            _$Ac = _$Ey;
            _$ql += 5;
        } else {
            _$Ac = _$Ey;
        }
        _$ql++;
        _$wF.push(_$Ac);
    }
    return _$zu(_$wF);
}
function _$w6(_$Bw) {
    _$Bw = _$Hm.call(_$Bw, '');
    var _$ql, _$yB = _$sU(1723), _$wF = [], _$Ac = _$Bw.length, _$EB, _$Ey;
    for (_$ql = 0; _$ql < _$Ac; _$ql++) {
        _$wF.push(_$yB() % _$Ac);
    }
    for (_$ql = _$Ac - 1; _$ql >= 0; _$ql--) {
        _$EB = _$wF[_$ql];
        _$Ey = _$Bw[_$ql];
        _$Bw[_$ql] = _$Bw[_$EB];
        _$Bw[_$EB] = _$Ey;
    }
    return _$Bw.join('');
}
function _$BU() {
    return 7
}
function _$yQ(_$ql) {
    var _$EB = _$ql.length
      , _$wF = new _$G4(_$EB)
      , _$yB = 0
      , _$Ac = _$yP();
    while (_$yB < _$EB) {
        _$wF[_$yB] = _$Ac[_$bB.call(_$ql, _$yB++)];
    }
    return _$wF.join(_$lG());
}
function _$Fr(_$wF) {
    var _$Ac = _$FT();
    _$Ac = _$zX();
    _$wF[_$jK(_$Av(), 16)] = _$EK();
    _$wF[12] = _$uP();
    return _$EU();
}
function _$Bc() {
    return 6
}
function _$AL(_$ql) {
    var _$wF, _$Ey = _$bj(_$ql), _$Bw = new _$G4(_$Ey - 1);
    var _$yB = _$bB.call(_$ql, 0) - 40;
    for (var _$Ac = 0, _$EB = 1; _$EB < _$Ey; ++_$EB) {
        _$wF = _$bB.call(_$ql, _$EB);
        if (_$wF >= 40 && _$wF < 127) {
            _$wF += _$yB;
            if (_$wF >= 127)
                _$wF = _$wF - 87;
        }
        _$Bw[_$Ac++] = _$wF;
    }
    return _$CP.apply(null, _$Bw);
}
function _$l0() {
    return 2
}
function _$FM() {
    return 12
}
function _$iX(_$Ac, _$Ey, _$Bw, _$Et, _$EB, _$yB) {
    _$Ac = _$CF(_$q3(_$AL(_$Ac)), 2);
    var _$wF = _$yU(_$AL(_$Ey));
    _$Ey = _$Hm.call(_$wF, _$ET);
    _$Bw = _$AL(_$Bw);
    if (_$Bw.length > 0) {
        _$Bw = _$Hm.call(_$Bw, _$ET);
        _$Ey = _$Ey[_$oh()](_$Bw);
    }
    var _$EM = _$mR();
    for (var _$ql = 0; _$ql < _$Ac.length; _$ql++) {
        _$HF[_$EM + _$Ac[_$ql]] = _$Ey[_$ql];
    }
    _$Et = _$CF(_$AL(_$Et), 2);
    _$wF = _$AL(_$EB);
    _$EB = _$Hm.call(_$wF, _$ET);
    _$wF = _$AL(_$yB);
    _$yB = _$Hm.call(_$wF, _$ET);
    _$EB = _$EB[_$oh()](_$yB);
    _$zh(_$Et, _$EB);
}
function _$pf() {
    var _$ql = _$Cl();
    var _$yB = [];
    for (var _$EM = 0; _$EM < 6; _$EM++) {
        _$yB[_$EM] = [];
    }
    _$yy = function() {
        return _$yB;
    }
    ;
    var _$Ac = _$yB[0]
      , _$EB = _$yB[1]
      , _$Bw = _$yB[2]
      , _$Ey = _$yB[3]
      , _$E4 = _$yB[4]
      , _$wF = _$yB[5];
    _$a7(_$wF, 0, 255, -1);
    for (_$EM = 0; _$EM < _$ql.length; _$EM++) {
        var _$Et = _$bB.call(_$ql[_$EM], 0);
        _$Ac[_$Et] = _$EM << 2;
        _$EB[_$Et] = _$EM >> 4;
        _$Bw[_$Et] = (_$EM & 15) << 4;
        _$Ey[_$Et] = _$EM >> 2;
        _$E4[_$Et] = (_$EM & 3) << 6;
        _$wF[_$Et] = _$EM;
    }
}
function _$hk() {
    return "_ZdslargmlZ[y pcrspl dslargmlZgb[y t_p v ; bmaskclr,ecrCjckclr@wGbZgb[9 t_p t ; v,amlrclr9 v,n_pclrLmbc,pckmtcAfgjbZv[9 pcrspl t9{{Z[[";
}
function _$v0() {
    if (_$CF)
        /$/.test(_$pf());
    _$iX(_$Er(), _$Er(), _$Er(), _$Er(), _$Er(), _$Er());
    _$aY();
    _$Hy = _$HF[_$hI()];
    _$EC = _$HB[_$gS()];
    _$FE = _$HF[_$a5()];
    _$aF = _$HF[_$jS()];
    _$b0 = _$HB[_$bS()];
    _$Bq = _$HF[_$pI()];
    try {
        _$G7 = _$HF[_$nF()];
    } catch (_$wF) {}
    if (_$G7) {
        try {
            _$G7[_$lz()] = _$lz();
            _$G7[_$lV()](_$lz());
            _$G7[_$ma()] = _$nF();
        } catch (_$wF) {
            _$G7 = _$HC;
        }
    }
    if (!_$nr && !_$GQ) {
        _$GQ = 0;
        _$nr = 0;
        _$fO = 0;
    }
    if (!_$Bq) {
        _$Bq = new _$Ai();
        _$HF[_$pI()] = _$Bq;
    }
    _$dZ = _$Fi(_$im());
}
function _$jN(_$EM, _$aR, _$ql) {
    var _$E4 = _$Hx();
    _$Am();
    var _$D8 = 0
      , _$EA = 0;
    var _$EB = _$zf(_$Cf());
    _$E4 = _$Hx();
    _$yn();
    function _$BJ() {
        var _$Dl = _$xY(_$EM, _$D8);
        _$D8 += _$t4(_$EM, _$D8);
        return _$Dl;
    }
    var _$bQ = _$BJ();
    var _$Ew = _$rn();
    var _$ER = _$rn();
    _$ER = _$ER[_$fo()](_$rn(true));
    var _$Et = _$rn();
    _$Et = _$Et[_$fo()](_$rn(true));
    var _$wn = _$rn()[_$fo()](_$rn(true));
    _$E4 = _$Hx();
    _$yn();
    var _$Fn = _$BJ();
    _$EM = _$Fi(_$EM[_$qQ()](_$D8));
    _$D8 = 0;
    _$E4 = _$Hx();
    var _$Fd = _$aR[_$jH()](_$ql[1], _$ql[2]);
    var _$Bw = _$aR[_$jH()](0, _$ql[0]);
    var _$DO = _$aR[_$jH()](_$ql[3], _$ql[4]);
    var _$DJ = [_$wn, _$DO, [], _$Bw, _$Fd];
    if (_$HF[_$yQ(_$Gd(_$vW()))]) {
        _$mt(_$Bw);
    }
    _$E4 = _$Hx();
    var _$yB, _$En = 0, _$vF = [_$HC, _$HC, _$HC, _$HC, _$HC, _$Ac, _$Ey, _$wF];
    _$yB = _$Ey(1);
    _$E4 = _$Hx();
    _$pg(_$DO, _$Et);
    _$tG(_$yQ(_$yB));
    return;
    function _$m3() {
        var _$Dl = _$EM[_$D8];
        if ((_$Dl & 0x80) === 0) {
            _$D8 += 1;
            return _$Dl;
        }
        if ((_$Dl & 0xc0) === 0x80) {
            _$Dl = ((_$Dl & 0x3f) << 8) | _$EM[_$D8 + 1];
            _$D8 += 2;
            return _$Dl;
        }
    }
    function _$Ac(_$Ev) {
        var _$Dl = _$m3(), _$EY, _$Cc = new _$G4(_$Ev), _$gZ = new _$G4(_$Dl), _$CZ = new _$G4(_$Ev + _$Dl);
        if (_$Ev == 3) {
            var _$a6 = _$HF[_$mA()][_$nz()]((_$Hx() - _$mS) / 1000);
            _$yi = _$yi + _$HF[_$mA()][_$nz()](_$HF[_$mA()][_$d2()](_$a6 / 5.88 + 1));
        }
        _$EY = 0;
        while (_$EY < _$Dl)
            _$gZ[_$EY++] = _$Ey(1);
        _$EY = 0;
        while (_$EY < _$Ev)
            _$Cc[_$EY++] = _$Ey(1);
        _$mt(_$Cc);
        _$EY = 0;
        var _$Ea = 0
          , _$E0 = 0;
        while (_$Ea < _$Dl && _$E0 < _$Ev) {
            var _$eA = (_$EC() % 100) * (_$Dl - _$Ea + 1) / (_$Ev - _$E0) >= 50;
            var _$cl = _$EC() % 10;
            if (_$eA) {
                while (_$Ea < _$Dl && _$cl > 0) {
                    _$CZ[_$EY++] = _$gZ[_$Ea++];
                    --_$cl;
                }
            } else {
                while (_$E0 < _$Ev && _$cl > 0) {
                    _$CZ[_$EY++] = _$Cc[_$E0++];
                    --_$cl;
                }
            }
        }
        while (_$Ea < _$Dl)
            _$CZ[_$EY++] = _$gZ[_$Ea++];
        while (_$E0 < _$Ev)
            _$CZ[_$EY++] = _$Cc[_$E0++];
        return _$CZ.join(_$lG());
    }
    function _$rn(_$eA) {
        var _$CZ, _$Dl, _$EY, _$E0;
        _$yn();
        _$Dl = _$BJ();
        _$CZ = _$BJ();
        _$EY = _$y6(_$CZ);
        if (_$Dl === 0 && _$CZ === 0)
            return [];
        var _$gZ = _$EY[_$q0()](_$EB);
        if (_$eA) {
            for (var _$Ev = 0; _$Ev < _$Dl; _$Ev++) {
                _$gZ[_$Ev] = _$iL(_$gZ[_$Ev]);
            }
        }
        return _$gZ;
    }
    function _$Ey(_$Dl) {
        var _$E0 = 0, _$Ev, _$EY, _$gZ;
        if (_$Dl === 1) {
            _$CZ();
            if (_$EY <= 4) {
                return _$DJ[_$EY][_$gZ];
            }
            return _$vF[_$EY](_$gZ);
        }
        _$Ev = new _$G4(_$Dl);
        while (_$E0 < _$Dl) {
            _$CZ();
            if (_$EY <= 4) {
                _$Ev[_$E0++] = _$DJ[_$EY][_$gZ];
            } else {
                _$Ev[_$E0++] = _$vF[_$EY](_$gZ);
            }
        }
        return _$Ev.join(_$lG());
        function _$CZ() {
            _$EY = _$C6();
            _$gZ = _$EY & 0x1F;
            _$EY = _$EY >> 5;
            if (_$gZ == 0x1f) {
                _$gZ = _$m3() + 31;
            }
        }
    }
    function _$C6() {
        return _$EM[_$D8++];
    }
    function _$yn() {
        if (_$EA === -1)
            return;
        if (_$EA === 0) {
            _$D8++;
            if (_$EM[_$jJ()](_$D8) === _$lO()) {
                _$D8++;
            } else if (_$EM[_$jJ()](_$D8) === _$hm()) {
                _$EA = -1;
                _$D8++;
                return;
            } else {}
        }
        var _$Dl;
        if (typeof (_$EM) === _$o4()) {
            _$Dl = _$GY(_$EM[_$qQ()](_$D8 + 1, 3));
        } else {
            _$Dl = _$GY(_$zu(_$EM, _$D8 + 1, _$D8 + 4));
        }
        if (_$Dl !== _$EA) {}
        _$D8 += 4;
        _$EA++;
    }
    function _$y6(_$gZ) {
        var _$Dl = _$D8;
        _$D8 += _$gZ;
        return _$EM[_$is()](_$Dl, _$D8);
    }
    function _$wF() {
        var _$Ev, _$gZ, _$Dl;
        _$Ev = _$Ey(1);
        _$Ey(1);
        _$gZ = _$Ey(1);
        _$Ey(1);
        _$Dl = _$Ey(1);
        _$HF[_$yQ(_$Ev)] = _$wu(_$gZ, _$Dl);
    }
    ;;;;
}
function _$iL(_$yB) {
    var _$wF = _$Fi(_$yB);
    return _$on(_$wF);
}
function _$Hx() {
    return new _$te()[_$lr()]();
}
function _$EK() {
    return 1
}
function _$h8(_$yB) {
    var _$wF;
    return function() {
        if (_$wF === _$HC) {
            _$wF = _$iL(_$yB);
            _$wF = _$AL(_$wF);
        }
        return _$wF;
    }
    ;
}
function _$D7(_$wF) {
    var _$Ey = _$BU();
    _$Ey = _$rK();
    var _$Ac = _$Fb();
    _$EB = _$l0() + _$Gn();
    _$Ey = _$rK() + _$FT();
    _$Gi(_$wF);
    _$wF[_$jK(_$wF[_$jK(_$kO(), 16)], 16)] = _$EI(_$wF);
    return _$Bc();
}
function _$Ch(_$wF) {
    _$wF[14] = _$Fa();
    _$wF[_$jK(_$BU(), 16)] = _$rK();
    var _$EB = _$Fb();
    _$EB = _$Av();
    return _$EK();
}
function _$CF(_$yB, _$Ey) {
    var _$EB = _$bj(_$yB)
      , _$wF = new _$G4(_$iJ(_$EB / _$Ey))
      , _$ql = 0
      , _$Ac = 0;
    for (; _$Ac < _$EB; _$Ac += _$Ey,
    _$ql++)
        _$wF[_$ql] = _$G8.call(_$yB, _$Ac, _$Ey);
    return _$wF;
}
function _$uh(_$EB, _$wF) {
    _$EB = _$EB[_$q0()](_$k3());
    _$EB.push(_$wF);
    var _$Ac = _$EB.length
      , _$ql = new _$G4(_$Ac);
    for (var _$yB = 0; _$yB < _$Ac; _$yB++) {
        _$ql[_$yB] = _$rq()[_$fo()](_$yB, _$gj());
    }
    return new _$FD(_$k2(),_$pA() + _$ql.join(_$k3()) + _$oW())(_$EB);
}
function _$sx(_$wF) {
    return function() {
        return _$wF;
    }
    ;
}
function _$z1(_$wF, _$yB) {
    _$nr |= _$wF;
    if (_$yB)
        _$GQ |= _$wF;
}
function _$zZ() {
    _$Hd = _$D1.prototype.charAt;
    _$bB = _$D1.prototype.charCodeAt;
    _$pe = _$D1.prototype.codePointAt;
    _$GB = _$D1.prototype.concat;
    _$yT = _$D1.prototype.endsWith;
    _$cw = _$D1.prototype.includes;
    _$Ht = _$D1.prototype.indexOf;
    _$CH = _$D1.prototype.lastIndexOf;
    _$sJ = _$D1.prototype.localeCompare;
    _$ur = _$D1.prototype.match;
    _$s9 = _$D1.prototype.normalize;
    _$bX = _$D1.prototype.padEnd;
    _$x7 = _$D1.prototype.padStart;
    _$ts = _$D1.prototype.repeat;
    _$GK = _$D1.prototype.replace;
    _$zj = _$D1.prototype.search;
    _$F1 = _$D1.prototype.slice;
    _$Hm = _$D1.prototype.split;
    _$jl = _$D1.prototype.startsWith;
    _$G8 = _$D1.prototype.substr;
    _$zt = _$D1.prototype.substring;
    _$xw = _$D1.prototype.toLocaleLowerCase;
    _$ih = _$D1.prototype.toLocaleUpperCase;
    _$G0 = _$D1.prototype.toLowerCase;
    _$g8 = _$D1.prototype.toSource;
    _$hg = _$D1.prototype.toString;
    _$c6 = _$D1.prototype.toUpperCase;
    _$z8 = _$D1.prototype.trim;
    _$tg = _$D1.prototype.trimLeft;
    _$zb = _$D1.prototype.trimRight;
    _$qG = _$D1.prototype.valueOf;
}
function _$eD() {
    return "tYt4HDeF7AiGBG$_cJCxhe";
}
function _$vI() {
    var _$yB = _$tJ(_$kv(_$hk()))("9DhefwqGPrzGxEp9hPaoag")
      , _$Ac = 0
      , _$ql = {};
    _$ql._$d6 = _$Ey;
    _$ql._$mI = _$wF;
    return _$ql;
    function _$wF() {
        return _$G8.call(_$yB, _$Ac);
    }
    function _$EB() {
        var _$Et = _$bB.call(_$yB, _$Ac);
        if (_$Et >= 40) {
            _$Ac++;
            return _$Et - 40;
        }
        var _$Bw = 39 - _$Et;
        _$Et = 0;
        for (var _$EM = 0; _$EM < _$Bw; _$EM++) {
            _$Et *= 87;
            _$Et += _$bB.call(_$yB, _$Ac + 1 + _$EM) - 40;
        }
        _$Ac += _$Bw + 1;
        return _$Et + 87;
    }
    function _$Ey() {
        var _$Bw = _$EB();
        var _$EM = _$G8.call(_$yB, _$Ac, _$Bw);
        _$Ac += _$Bw;
        return _$EM;
    }
}
function _$tG(_$wF) {
    if (_$wF === _$HC || _$wF === _$lG()) {
        return;
    }
    var _$EB = _$HF[_$r8()][_$wA()], _$ql;
    if (!_$b4) {
        _$b4 = _$EB[_$gE()];
    }
    if (_$HF[_$qA()]) {
        _$ql = _$HF[_$qA()](_$wF);
    } else {
        var _$yB = _$HF[_$pT()];
        debugger ;
        _$ql = eval( _$wF);
        // _$ql = _$yB[_$mm()](_$HF, _$wF);
    }
    if (_$b4 !== _$EB.push) {
        _$EB.push = _$b4;
    }
    return _$ql;
}
function _$EI(_$wF) {
    var _$EB = _$Gn();
    _$Ey = _$Bc();
    _$wF[_$jK(_$EU(), 16)] = _$FM();
    var _$EB = _$gh();
    _$Ac = _$l0();
    return _$Gn();
}
function _$aY() {
    var _$wF = new _$G4(256), _$EB = new _$G4(256), _$ql;
    for (var _$Ac = 0; _$Ac < 256; _$Ac++) {
        _$wF[_$Ac] = _$CP(_$EB[_$Ac] = _$Ac);
    }
    var _$Ey = _$ez();
    for (_$Ac = 32; _$Ac < 127; _$Ac++)
        _$ql = _$Ac - 32,
        _$wF[_$Ac] = _$Hd.call(_$Ey, _$ql),
        _$EB[_$Ac] = _$bB.call(_$Ey, _$ql);
    _$Ey = _$wF;
    _$yP = function() {
        return _$Ey;
    }
    ;
    var _$yB = _$Hm.call(_$o6(), _$lG());
    _$zI = function() {
        return _$yB;
    }
    ;
}
function _$Gb(_$wF) {
    var _$Ac = _$EU();
    _$Ac = _$FM();
    var _$EB = _$gh();
    _$Ey = _$l0();
    _$wF[15] = _$Bc();
    _$Ac = _$rK();
    return _$FT();
}
function _$a7(_$wF, _$yB, _$ql, _$EB) {
    for (; _$yB < _$ql; _$yB++) {
        _$wF[_$yB] = _$EB;
    }
}
function _$t4(_$yB, _$EB) {
    var _$wF = _$yy()[5];
    var _$ql = _$wF[_$bB.call(_$yB, _$EB)];
    if (_$ql < 82)
        return 1;
    return 86 - _$ql + 1;
}
function _$uP() {
    return 3
}
function _$vW() {
    return 406;
}
function _$kp(_$yB) {
    var _$wF;
    return function(_$ql, _$EB) {
        if (_$wF === _$HC) {
            _$wF = _$yQ(_$yB);
        }
        return _$wF;
    }
    ;
}
function _$Gi(_$wF) {
    _$Ch(_$wF);
    _$wF[12] = _$uP();
    var _$EB = _$FT();
    _$Ey = _$zX();
    var _$EB = _$EK();
    _$EB = _$Fa();
    _$Eo(_$wF);
    return _$wF[_$jK(_$EU(), 16)];
}
function _$Av() {
    return 8
}
function _$zh(_$ql, _$EB) {
    var _$yB = _$mR();
    for (var _$wF = 0; _$wF < _$EB.length; _$wF++) {
        _$HF[_$yB + _$ql[_$wF]] = _$h8(_$EB[_$wF]);
    }
}
var _$HC, _$G7;
_$HF = window;
_$D1 = String;
_$zZ();
_$fe(_$eD(), _$uL());
_$CP = _$D1.fromCharCode;
_$iJ = _$HB.ceil;
_$ET = _$CP(96);
function _$Gv(_$wF) {
    var _$Ey = _$FT();
    _$Ey = _$zX();
    _$wF[3] = _$l0();
    _$wF[15] = _$Bc();
    return _$BU();
}
function _$nN(_$wF) {
    return _$c7(_$Cx(_$wF));
}
function _$Ha(_$Bw, _$EB) {
    if (typeof _$Bw === _$o4())
        _$Bw = _$F6(_$Bw);
    if (!_$EB)
        _$EB = _$Cl();
    var _$wF, _$yB = _$Gt = 0, _$ql = _$Bw.length, _$Ey, _$Ac;
    _$wF = new _$G4(_$HB[_$nT()](_$ql * 4 / 3));
    _$ql = _$Bw.length - 2;
    while (_$yB < _$ql) {
        _$Ey = _$Bw[_$yB++];
        _$wF[_$Gt++] = _$EB[_$Ey >> 2];
        _$Ac = _$Bw[_$yB++];
        _$wF[_$Gt++] = _$EB[((_$Ey & 3) << 4) | (_$Ac >> 4)];
        _$Ey = _$Bw[_$yB++];
        _$wF[_$Gt++] = _$EB[((_$Ac & 15) << 2) | (_$Ey >> 6)];
        _$wF[_$Gt++] = _$EB[_$Ey & 63];
    }
    if (_$yB < _$Bw.length) {
        _$Ey = _$Bw[_$yB];
        _$wF[_$Gt++] = _$EB[_$Ey >> 2];
        _$Ac = _$Bw[++_$yB];
        _$wF[_$Gt++] = _$EB[((_$Ey & 3) << 4) | (_$Ac >> 4)];
        if (_$Ac !== _$HC) {
            _$wF[_$Gt++] = _$EB[(_$Ac & 15) << 2];
        }
    }
    return _$wF.join(_$lG());
}
function _$yU(_$ql) {
    _$ql = _$Hm.call(_$ql, _$tm());
    for (var _$wF = 0; _$wF < _$ql.length - 1; _$wF += 2) {
        var _$yB = _$ql[_$wF];
        _$ql[_$wF] = _$ql[_$wF + 1];
        _$ql[_$wF + 1] = _$yB;
    }
    return _$ql.join(_$tm());
}
function _$jK(_$yB, _$wF) {
    return _$b0(_$yB) % _$wF;
}
function _$Eo(_$wF) {
    _$wF[8] = _$FM();
    _$wF[_$jK(_$zX(), 16)] = _$gh();
    _$wF[9] = _$Gn();
    return _$Bc();
}
function _$af(_$wF) {
    var _$Ey = _$FM();
    var _$Ey = _$l0();
    if (_$Bc()) {
        _$Ac = _$kO();
    }
    _$wF[_$jK(_$uP(), 16)] = _$EU();
    _$wF[_$jK(_$FT(), 16)] = _$zX();
    _$Ac = _$l0();
    return _$wF[_$jK(_$Fa(), 16)];
}
function _$xY(_$Ac, _$Ey) {
    var _$wF = _$yy()[5];
    var _$EB = _$wF[_$bB.call(_$Ac, _$Ey)];
    if (_$EB < 82)
        return _$EB;
    var _$yB = 86 - _$EB;
    _$EB = 0;
    for (var _$ql = 0; _$ql < _$yB; _$ql++) {
        _$EB *= 86;
        _$EB += _$wF[_$bB.call(_$Ac, _$Ey + 1 + _$ql)];
    }
    return _$EB + 82;
}
function _$pk(_$wF) {
    _$wF[0] = _$p7(_$wF);
    _$wF[_$jK(_$wF[_$jK(_$zX() + _$gh(), 16)], 16)] = _$af(_$wF);
    if (_$wF[_$jK(_$rK() + _$FT(), 16)]) {
        _$DH(_$wF);
    }
    _$wF[1] = _$wF[_$jK(_$zX() + _$gh(), 16)];
    return _$D7(_$wF);
}
function _$uL() {
    return "C|I|IRc|lmU|oscajoetotcrtprn||aniunrAteeOpDrdauoaerEennevebMn|h|nF|ocseraattype";
}
function _$BB(_$ql) {
    var _$EB = _$eh && new _$eh();
    if (_$EB) {
        var _$Ac = _$EB[_$kQ()];
        if (!_$Ac) {
            return;
        }
        var _$yB = _$Ac[_$ok()]();
        var _$wF = _$Hm.call(_$yB, _$rT());
        _$yB = _$wF[_$pW()]();
        if (_$yB === _$lG() && _$wF.length > 0)
            _$yB = _$wF[_$pW()]();
        if (_$Ht.call(_$yB, _$od()) !== -1 || _$Cu(_$yB, _$j8()) || _$yB === _$ig()) {
            _$uX(_$ql, 1);
            return true;
        }
    }
}
function _$Am() {
    _$wk = _$HF[_$pT()][_$ok()]()[_$dR()](/[\r\n\s]/g, _$lG()) !== _$qn();
}
function _$zf(_$Ey) {
    var _$Ac = _$Ey.length, _$wF = new _$G4(_$Ac), _$EB, _$ql, _$yB = _$zI();
    for (_$EB = 0; _$EB < _$Ac; _$EB++) {
        _$ql = _$bB.call(_$Ey, _$EB);
        if (_$ql >= 32 && _$ql < 127)
            _$wF[_$EB] = _$yB[_$ql - 32];
        else
            _$wF[_$EB] = _$Hd.call(_$Ey, _$EB);
    }
    return _$wF.join(_$lG());
}
function _$Er() {
    return _$xr._$d6();
}
function _$kv(_$ql) {
    var _$wF, _$Ey = _$ql.length, _$Bw = new _$G4(_$Ey - 1);
    var _$yB = _$bB.call(_$ql, 0) - 93;
    for (var _$Ac = 0, _$EB = 1; _$EB < _$Ey; ++_$EB) {
        _$wF = _$bB.call(_$ql, _$EB);
        if (_$wF >= 40 && _$wF < 92) {
            _$wF += _$yB;
            if (_$wF >= 92)
                _$wF = _$wF - 52;
        } else if (_$wF >= 93 && _$wF < 127) {
            _$wF += _$yB;
            if (_$wF >= 127)
                _$wF = _$wF - 34;
        }
        _$Bw[_$Ac++] = _$wF;
    }
    return _$CP.apply(null, _$Bw);
}
function _$yY() {
    var _$ql = _$AL(_$Er());
    _$ql = _$CF(_$ql, 2);
    var _$yB = _$zf(_$re());
    for (var _$wF = 0; _$wF < _$ql.length; _$wF++) {
        _$ql[_$wF] = _$yB + _$ql[_$wF];
    }
    return _$ql;
}
function _$gh() {
    return 13
}
var _$nr, _$GQ, _$fO;
var _$nj = 1;
_$bg = _$kv("qzs|u`v");
;;var _$b4;
;_$xr = _$vI();
_$AA();
function _$Cl() {
    return _$Hm.call(_$mY(), _$tm());
}
function _$F6(_$ql) {
    var _$yB, _$wF = 0, _$EB;
    _$ql = _$nN(_$ql);
    _$EB = _$ql.length;
    _$yB = new _$G4(_$EB);
    _$EB -= 3;
    while (_$wF < _$EB) {
        _$yB[_$wF] = _$bB.call(_$ql, _$wF++);
        _$yB[_$wF] = _$bB.call(_$ql, _$wF++);
        _$yB[_$wF] = _$bB.call(_$ql, _$wF++);
        _$yB[_$wF] = _$bB.call(_$ql, _$wF++);
    }
    _$EB += 3;
    while (_$wF < _$EB)
        _$yB[_$wF] = _$bB.call(_$ql, _$wF++);
    return _$yB;
}
function _$p7(_$wF) {
    _$FZ(_$wF);
    var _$Ac = _$uP();
    if (_$kO()) {
        _$wF[_$jK(_$gh(), 16)] = _$l0();
    }
    _$wF[6] = _$kO();
    _$wF[2] = _$Av();
    _$F2(_$wF);
    return _$Fr(_$wF);
}
function _$bj(_$wF) {
    return _$wF[_$bg];
}
function _$i1() {
    _$sX = _$Bq[_$fc()];
    _$Bq[_$fc()] = _$HC;
    _$Bq._$xp = _$Hx();
    _$mS = _$Bq._$xp;
    _$z1(4, 0);
    _$z1(2, _$BB(7));
    var _$Ac = _$yY();
    var _$yB = _$z9();
    var _$EB = _$z9();
    _$Gd = _$wF;
    _$CL = _$EB[1];
    _$yi = _$EB[0];
    _$FO = _$EB[2];
    if (_$sX) {
        _$jN(_$sX, _$Ac, _$yB);
        _$sX = _$HC;
    }
    _$Bq._$zD = _$Hx();
    if (_$Bq._$zD - _$Bq._$xp > 12000) {
        _$z1(1, 1);
        _$uX(13, 1);
    } else {
        _$z1(1, 0);
    }
    _$z1(8, 0);
    function _$ql() {
        return _$eZ;
    }
    function _$wF(_$Ey) {
        return _$HF[_$yQ(_$Ac[_$Ey])];
    }
}
function _$FT() {
    return 11
}
function _$zu(_$yB, _$Ey, _$ql) {
    _$Ey = _$Ey || 0;
    if (_$ql === _$HC)
        _$ql = _$yB.length;
    var _$wF = new _$G4(_$HB[_$uE()](_$yB.length / 40960))
      , _$Ac = _$ql - 40960
      , _$EB = 0;
    while (_$Ey < _$Ac) {
        _$wF[_$EB++] = _$CP[_$dz()](null, _$yB[_$dJ()](_$Ey, _$Ey += 40960));
    }
    if (_$Ey < _$ql)
        _$wF[_$EB++] = _$CP[_$dz()](null, _$yB[_$dJ()](_$Ey, _$ql));
    return _$wF.join(_$tm());
}
function _$Fb() {
    return 9
}
function _$Cu(_$wF, _$yB) {
    return _$F1.call(_$wF, 0, _$yB.length) === _$yB;
}
function _$y4(_$ql, _$EB) {
    var _$yB = _$mR();
    for (var _$wF = 0; _$wF < _$EB.length; _$wF++) {
        _$HF[_$yB + _$ql[_$wF]] = _$sx(_$EB[_$wF]);
    }
}
function _$FZ(_$wF) {
    var _$EB = _$rK();
    _$Ac = _$FT();
    var _$Ey = _$Av();
    _$Ey = _$EK();
    _$wF[_$jK(_$Bc(), 16)] = _$BU();
    return _$rK();
}
function _$Fa() {
    return 14
}
_$v0();
_$i1();
;

console.log('生成Cookie结束');
// console.log('程序结束，cookie 值：', document.cookie);
var cookie_str = document.cookie.split('=')[1]
const binaryData = Buffer.from(cookie_str, 'binary');

// 将二进制数据写入文件
fs.writeFile(cookiePath, binaryData, (err) => {
    if (err) {
        console.error('Error writing to file:', err);
        return;
    }
    console.log('Data has been written to output.bin successfully.');
});

console.log("程序结束");


// function getHtmlContent(html_text) {
//     var matches = html_text.match(/<meta[^>]*content=["']([^"']*)["'][^>]*>/gi);
//     var contentValues = matches.map((match) => {
//         const contentValueRegex = /content=["']([^"']*)["']/i;
//         const result = contentValueRegex.exec(match);
//         return result ? result[1] : null;
//     });
//     var content = contentValues[1];
//     return content;
// };

// function getTsParameters(html_text) {
//     var regex = /[";]*/g    // 替换所有";符号
//     var matchCd = html_text.match(/\$\_ts\.cd\s*=\s*(.+)/)[1].replace(regex, '');
//     var matchNsd = parseInt(html_text.match(/\$\_ts\.nsd\s*=\s*(.+)/)[1].replace(regex, '').split(" ")[0]);
//     return [matchCd, matchNsd];
// };
