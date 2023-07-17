var EventTarget = function EventTarget() { };
Object.defineProperties(EventTarget.prototype, {
    [Symbol.toStringTag]: {
        value: "EventTarget",
        configurable: true
    }
})
EventTarget.prototype.addEventListener = function addEventListener() { };
EventTarget.prototype.dispatchEvent = function dispatchEvent() { };
EventTarget.prototype.removeEventListener = function removeEventListener() { };


var WindowProperties = function WindowProperties() { };
Object.defineProperties(WindowProperties.prototype, {
    [Symbol.toStringTag]: {
        value: "WindowProperties",
        configurable: true
    }
})


WindowProperties.prototype.__proto__ = EventTarget.prototype;


var Window = function Windwo() {
    // 此操作容易被检测到
    throw new Error("Illegal constructor");
};
Object.defineProperties(Window.prototype, {
    [Symbol.toStringTag]: {
        value: "Window",
        configurable: true
    }
})
//////////////////////////////
Window.prototype.PERSISTENT = 1
Window.prototype.TEMPORARY = 0
/////////////////////////////

Window.prototype.__proto__ = WindowProperties.prototype;

window = this;
window.__proto__ = Window.prototype;

Window = FrameworkProxy(Window);
window = FrameworkProxy(window);

debugger;
