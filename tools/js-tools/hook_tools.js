
// 需要在执行index页面后才执行
// hook cookie 方法
(function () {
    // 严谨模式 检查所有错误
    'use strict';
    // document 为要hook的对象 这里是hook的cookie
    var cookieTemp = (document.cookie == undefined)?"":document.cookie;
    Object.defineProperty(document, 'cookie', {
        // hook set方法也就是赋值的方法 
        set: function (val) {
            // 这样就可以快速给下面这个代码行下断点
            // 从而快速定位设置cookie的代码
            console.log('Hook捕获到cookie设置->', val);
            debugger;
            cookieTemp = val;
            return val;
        },
        // hook get 方法也就是取值的方法 
        get: function () {
            console.log('Hook捕获到cookie获取->', cookieTemp);
            debugger;
            return cookieTemp;
        }
    });
})();

// hook 指定 cookie 方法
(function () {
    // 严谨模式 检查所有错误
    'use strict';
    // document 为要hook的对象 这里是hook的cookie
    var cookieTemp = "";
    Object.defineProperty(document, 'cookie', {
        // hook set方法也就是赋值的方法 
        set: function (val) {
            console.log('Hook捕获到cookie设置->', val);

            // 这样就可以快速给下面这个代码行下断点
            // 从而快速定位设置cookie的代码
            if (val.indexOf("cookie 名称") !== -1) {
                debugger;
            }
            cookieTemp = val;
            return val;
        },
        // hook get 方法也就是取值的方法 
        get: function () {
            return cookieTemp;
        }
    });
})();


// hook debugger
var _setInterval = setInterval;
setInterval = function (a, b) {
    if (a.toString().indexOf("debugger") != -1) {
        return null;
    }
    _setInterval(a, b);
}



// 本地调试补环境 hook 环境变量代码
var laowang_proxy = function (obj) {
    return new Proxy(obj, {
        set(target, prop, value) {
            console.log('set -->', target[Symbol.toStringTag], '-->', prop, '-->', value);
            return Reflect.set(...arguments);
        },
        get(target, prop, receiver) {
            console.log('get -->', target[Symbol.toStringTag], '-->', prop, '-->', target[prop]);
            return target[prop];
        }
    })
}
window = {};
// 调试属性
Object.defineProperties(window, {
    [Symbol.toStringTag]: {
        value: 'window',
        configurable: true
    }
})
window = laowang_proxy(window);

// VM 入口正则
// _\$[\$\w]{2} = _\$[\$\w]{2}\[_\$[\$\w]{2}\(\)\]\(_\$[\$\w]{2}\, _\$[\$\w]{2}\);


// hook Object.getOwnPropertyDescriptor 方法
Object.getOwnPropertyDescriptor_ = Object.getOwnPropertyDescriptor;
Object.getOwnPropertyDescriptor = function (o, p) {
    if (o.toLocaleString() == "[object Navigator]") {
        return undefined;
    };
    return Object.getOwnPropertyDescriptor_.apply(this, arguments);
}

// ============创建对象的方法============

// 以下均为实例
var a = {};
var b = class b { };
var c = new (function () { });
var d = Object();
var e = Object.create({});

// 以下方法创造了一个构造函数
function text() { };

// ============创建对象的方法============

// 只有实例有 __proto__ 属性
// 实例.__proto__ 获取该实例的原型
// 原型.__proto__ 获取该原型父亲的原型/实例
// 原型.prototype == 原型自身


// 原型链修改（继承指定的原型）

function Tmp() { }; // 创建一个函数（实例+原型）
var tmp = new Tmp();    // 创建一个实例
tmp.__proto__ = ({}).__proto__; // 继承指定原型
Tmp.prototype.__proto__ = ({}).__proto__;


// 修改 window 的原型链示例

var window1 = function window1() { name: "window-name-1" };
var Window1 = {};
Window1.__proto__ = window1.prototype; // 修改 Window1 的原型
Object.defineProperties(Window1, {
    [Symbol.toStringTag]: {
        value: "window1",
        configurable: true
    }
});// 修改原型的名称
