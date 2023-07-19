var Document = function Document() { };
Object.defineProperties(Document.prototype, {
    [Symbol.toStringTag]: {
        value: "Document",
        configurable: true
    }
});

document = {};
document.__proto__ = Document.prototype;

//////////////////////////////////////////////////////
document.cookie = "";
document.referrer = location?.href || "";
document.getElementById = function getElementById(id) {
    debugger;
    return null;
};
document.addEventListener = function addEventListener(type, listener, option, useCapture) {
    debugger;
};
//////////////////////////////////////////////////////

document = FrameworkProxy(document);

