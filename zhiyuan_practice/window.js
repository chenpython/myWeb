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