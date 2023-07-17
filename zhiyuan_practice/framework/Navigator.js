var Navigator = function Navigator() {
    throw new Error("Illegal constructor");
};
Object.defineProperties(Navigator.prototype, {
    [Symbol.toStringTag]: {
        value: "Navigator",
        configurable: true
    }
});


//  plugins 只能用 Navigator 的实例调用，无法从原型调用，但是 plugins 属于原型的属性
Navigator.prototype.plugins = [];

navigator = {};
navigator.__proto__ = Navigator.prototype;

for (var prototype_ in Navigator.prototype) {
    navigator[prototype_] = Navigator.prototype[prototype_];
    Navigator.prototype.__defineGetter__(prototype_, function () {
        throw new Error("Illegal constructor");
    })
}; // Navigator 的属性均只能在


