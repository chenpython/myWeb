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
    var content = metaContents[4];
    return content;
};

function getExecContent(html_text) {
    const $ = cheerio.load(html_text,);
    const metaContents = [];
    $('script').each((index, element) => {
        const content = $(element)[0];
        if (content) {
            metaContents.push(content);
        }
    });
    var content = metaContents[1].children[0].data;
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


var home_html_path = '/cde/home_success_1_.htm';
var link_js = '/cde/detail_cookie_link.js';
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
    documentElement: documentElement,
    getElementById: getElementById,
    addEventListener: addEventListener,
    createExpression: createExpression,
    visibilityState: 'hidden',
    body: null,
    cookie_: {"FSSBBIl1UgzbN7N80T": "30wcEUzu2nlINDkgSKLPKka2MK7P9SDBsUZT_PI.WT_SUVEr7IFCmVod3hx.MnleY_ffEbIaG2V9B3r.sFIBsThpDRSKw3uAQ2uBY1m3d88adlkGrzG9oQ8d470p8e06QJZDReQovtxrWCmVutIhNuB4uv7KwYnOQiy4daqfZzFGEUtWuoMtQGvCDV.N5gtekER3"},
    removeChild: removeChild,
    appendChild: appendChild,
    all: documentAll,
    characterSet: 'UTF-8'
};
Object.defineProperties(document, {
    [Symbol.toStringTag]: {
        value: 'document',
        configurable: true
    },
    cookie: {
        get: function() {
            var cookieList = [];
            var att;
            for (att in this.cookie_) {
                cookieList.push(att + "=" + this.cookie_[att]);
            };
            return cookieList.join(";");
        },
        set: function(value) {
            var cookieKey = value.split("=")[0];
            var cookieValue = value.split("=")[1];
            cookieKey = cookieKey.trim().replace(" ", "");
            cookieValue = cookieValue.trim().replace(" ", "");
            this.cookie_[cookieKey] = cookieValue;
        }
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
    setItem: setItem,
    FSSBB48: "470552:1",
    $_f1: "Dw3Au.0k5f2nKwZPxHMUiHhe47Q",
    FSSBB14: "470552:438:",
    FSSBB3: "470552:AO2DK._6Iiehbh765gZEia",
    $_f0: "bPDdOo9zc_ruy.7NU5ZzQJvtX80",
    $_fh0: "W7ONyYG2S2TTMnB6tSNM7CMqHsZ",
    FSSBB93: "470552:1",
    FSSBB42: "470552:2",
    $_YWTU: '1pqWcrLXGNq400Rma5gQ4XT7T0tTAF_PjJmV.t83beA',
    $_cDro: '0'
    
};
Object.defineProperties(localStorage, {
    [Symbol.toStringTag]: {
        value: 'localStorage',
        configurable: true
    }
});
localStorage = proxy(localStorage);

sessionStorage = { 
    getItem: getItem, 
    setItem: setItem, 
    $_YWTU: '1pqWcrLXGNq400Rma5gQ4XT7T0tTAF_PjJmV.t83beA',
    $_cDro: '0'
};
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

plugins = [];
Object.defineProperties(plugins, {
    [Symbol.toStringTag]: {
        value: 'PluginArray ',
        configurable: true
    }
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
    plugins: plugins
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
window.screen = {};

window.setTimeout = function setTimeout(code, delay) {
    if (code.toString().indexOf("debugger") == -1) {
        return code();
    }
};
window.setInterval = function setInterval(code, delay) { };

window = proxy(window);
window.top = window;
window.self = window;

content = getHtmlContent(data);
exec_content = getExecContent(data);
eval(js_content);
window.eval('debugger;' + exec_content);


console.log('生成Cookie结束');
// console.log('程序结束，cookie 值：', document.cookie);
var cookie_str = document.cookie
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
