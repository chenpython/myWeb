console.log("this is window.js");

function MyProxy(obj) {
    return new Proxy(obj, {
        get: function (target, prop, receiver) {
            console.log("%s get %s -> %s", target, prop, target[prop]);
            return target[prop];
        },
        set: function (target, prop, receiver) {
            console.log("%s set %s -> %s", target, prop, receiver);
            return Reflect.set(...arguments);
        }
    })
}

// hook tostring
(() => {
    "use strict";
    const $toString = Function.toString;
    const myFunction_toString_symbol = Symbol('('.concat('', ')_', (Math.random() + '').toString(36)));
    const myTostring = function () {
        return typeof this == 'function' && this[myFunction_toString_symbol] || $toString.call(this);
    };
    function set_native(func, key, value) {
        Object.defineProperty(func, key, {
            enumerable: false,
            configurable: true,
            writable: true,
            value: value
        });
    };
    delete Function.prototype['toString'];// 删除原型链上的toString方法
    set_native(Function.prototype, "toString", myTostring);//自定义getter方法

    // 嵌套一层，保护自定义同String，否则会被检测到
    set_native(Function.prototype.toString, myFunction_toString_symbol, 'function toString() { [native code] }');
    this.func_set_native = (func) => {
        set_native(func, myFunction_toString_symbol, `function ${myFunction_toString_symbol, func.name || ''}() { [native code] }`);
    };//导出函数到globalthis
}).call(this);

window = global;
window = MyProxy(window);
Object.defineProperties(window, {
    [Symbol.toStringTag]: {
        value: "window",
        configurable: true
    }
})

navigator = MyProxy(class navigator { });

location = MyProxy(class location { });










debugger;

window.tmp = 'tmp';
window.location = window.tmp;