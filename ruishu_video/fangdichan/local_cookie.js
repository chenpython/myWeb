var fs = require('fs');

myProxy = function myProxy(obj) {
    return new Proxy(obj, {
        get: function (target, prop, receiver) {
            console.log("%s get %s -> %s", target, prop, target[prop]);
            return target[prop];
        },
        set: function (target, prop, receiver) {
            if (prop == "$_fpn1") {
                debugger;
            }
            console.log("%s set %s -> %s", target, prop, receiver);
            return Reflect.set(...arguments);
        }
    })
}
location = {
    "ancestorOrigins": {},
    "href": "http://www.fangdi.com.cn/new_house/new_house.html",
    "origin": "http://www.fangdi.com.cn",
    "protocol": "http:",
    "host": "www.fangdi.com.cn",
    "hostname": "www.fangdi.com.cn",
    "port": "",
    "pathname": "/new_house/new_house.html",
    "search": "",
    "hash": ""
}
var mimetypearray = []
Object.defineProperties(mimetypearray, {
    [Symbol.toStringTag]: {
        value: 'MimeTypeArray',
        configurable: true
    }
})

NetworkInformation = {}
Object.defineProperties(NetworkInformation, {
    [Symbol.toStringTag]: {
        value: 'NetworkInformation',
        configurable: true
    }
})

navigator = {
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    mimeTypes: mimetypearray,
    connection: NetworkInformation
}


function removeChild(node) {
    console.log("删除节点：", node)
}

function getElementsByTagName(tagName) {
    console.log('getElementsByTagName: ', tagName)
    resultTagElements = []
    Object.defineProperties(resultTagElements, {
        [Symbol.toStringTag]: {
            value: 'HTMLCollection',
            configurable: true
        }
    })
    switch (tagName.toLowerCase()) {
        case "i": { break }
        case "meta": {
            var content = window.content;
            var htmlheadelement = {
                removeChild: removeChild
            }
            Object.defineProperties(htmlheadelement, {
                [Symbol.toStringTag]: {
                    value: 'HTMLHeadElement',
                    configurable: true
                }
            })

            htmlmetaelement = {
                content: content,
                parentNode: htmlheadelement
            }
            Object.defineProperties(htmlmetaelement, {
                [Symbol.toStringTag]: {
                    value: 'HTMLMetaElement',
                    configurable: true
                }
            })
            resultTagElements[0] = htmlmetaelement
            resultTagElements[1] = htmlmetaelement
            break
        }
    }

    return resultTagElements

}

function addEventListener() { }
function createElement(tagname) {
    console.log('createElement: ', tagname);
    resultElement = {}
    if (tagname.toLowerCase() == 'div') {
        resultElement.getElementsByTagName = getElementsByTagName
        Object.defineProperties(resultElement, {
            [Symbol.toStringTag]: {
                value: 'HTMLDivElement',
                configurable: true
            }
        })
    }

    return resultElement
}
DOMParser = {}

function removeItem(keyName) {
    console.log("removeItem: ", keyName)
}
function openDatabase() {
    // length: 4
    // name: "openDatabase"
}
function getAttribute(attributeName) {
    var attribute = "";
    switch (attributeName) {
        case "selenium":
            attribute = null;
            break;
    }
    return attribute;
}



document = {
    createElement: createElement,
    charset: "UTF-8",
    characterSet: "UTF-8",
    getElementsByTagName: getElementsByTagName,
    documentElement: {
        style: {},
        getAttribute: getAttribute
    },
    addEventListener: addEventListener,
    cookie: 'www.fangdi.com_http_ic=www.fangdi.com.cn_80_RS'
}

Object.defineProperties(document, {
    [Symbol.toStringTag]: {
        value: 'document',
        configurable: true
    }
})

function getItem(keyName) {
    if (keyName == "$_YWTU") {
        return null;
    } else {
        debugger;
    }
}
function setItem(keyName, keyValue) {
    this[keyName] = keyValue;
}

sessionStorage = {
    getItem: getItem,
    setItem: setItem,
    length: 0
}
Object.defineProperties(sessionStorage, {
    [Symbol.toStringTag]: {
        value: 'sessionStorage',
        configurable: true
    }
})

localStorage = { removeItem: removeItem, getItem: getItem, setItem: setItem }
Object.defineProperties(localStorage, {
    [Symbol.toStringTag]: {
        value: 'localStorage',
        configurable: true
    }
})
localStorage = myProxy(localStorage)


function attachEvent() {
}

document = myProxy(document)

window_mine = {
    $_ts: {},
    top: {
        location: location
    },
    document: document,
    attachEvent: attachEvent,
    location: location,
    navigator: navigator,
    DOMParser: DOMParser,
    addEventListener: addEventListener,
    localStorage: localStorage,
    sessionStorage: sessionStorage,
    name: "",
    openDatabase: openDatabase
};


window = Object.assign(global, window_mine)
window.self = window;
Object.defineProperties(window, {
    [Symbol.toStringTag]: {
        value: 'window',
        configurable: true
    }
})

var tsFunc = require("./c.FxJzG50F.dfe1675.js");
tsFunc.tsFunction();

var cntFunc = require("./content.js");
var cnt_list = cntFunc.contentHandler();
window.content = cnt_list[0];

window = myProxy(window)



// function homeCode(codeStr) {
//     var matches = new RegExp(/{(ret=[\$\w]+\.call\([\s\w\$]+,([\s\w\$]+)\);)}/).exec(codeStr);
//     var variableName = matches[2];
//     var entrence = matches[1];
//     var codeString = `{var check_strs = new RegExp(/(_\$[\w\$]{2})=\(_\$[\w\$]{2}\((_\$[\w\$]{2}\[139\])\)\)\(\);/).exec(${variableName});var start_index = check_strs.index;var target_str = check_strs[2];var result_str = check_strs[1];${variableName} = \`\${${variableName}.substring(0, start_index)}if(\${target_str}!="try{return (window instanceof Window);}catch(e){}"){ \${check_strs[0]}}else{ \${result_str}=true};\${${variableName}.substring(start_index + check_strs[0].length, ${variableName}.length)\`;${entrence}}`;
//     var updateCodeStr = codeStr.replace(matches[0], codeString)
//     return updateCodeStr
// }

var home_js_code = homeCode(cnt_list[1]);

function homeCode(codeStr) {
    var matches = new RegExp(/{(ret=[\$\w]+\.call\([\s\w\$]+,([\s\w\$]+)\);)}/).exec(codeStr);
    var variableName = matches[2];
    var entrence = matches[1];
    var updateCodeStr = "{var check_strs = new RegExp(/(_\\$[\\w\\$]{2})=\\(_\\$[\\w\\$]{2}\\((_\\$[\\w\\$]{2}\\[139\\])\\)\\)\\(\\);/).exec(" + variableName + ");" +
        "var start_index = check_strs.index;" +
        "var target_str = check_strs[2];" +
        "var result_str = check_strs[1];" +
        variableName + "=" + variableName + ".substring(0, start_index) + 'if(' + target_str + '!="
        + '"try{return (window instanceof Window);}catch(e){}"){' + "' + check_strs[0] + '}else{' + result_str + '=true;};'+" + variableName + ".substring(start_index + check_strs[0].length, " + variableName + ".length);" +
        entrence +
        '}'

    updatecodeStr_ = codeStr.substring(0, matches.index) + updateCodeStr + codeStr.substring(matches.index + matches[0].length,)
    return updatecodeStr_
}
// 自执行代码
eval(home_js_code);
console.log("cookie生成结束");
// console.log(document.cookie)

var cookie_str = document.cookie.split('=')[1]
const binaryData = Buffer.from(cookie_str, 'binary');

// 将二进制数据写入文件
fs.writeFile('/home/feng/workspace/myWeb/ruishu_video/fangdichan/cookie', binaryData, (err) => {
    if (err) {
        console.error('Error writing to file:', err);
        return;
    }
    console.log('Data has been written to output.bin successfully.');
});

console.log("程序结束");