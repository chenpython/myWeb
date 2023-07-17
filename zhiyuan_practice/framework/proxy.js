function FrameworkProxy(obj) {
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