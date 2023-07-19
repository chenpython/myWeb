var Location = function Location() {
    throw new Error("Illegal constructor");
};
Object.defineProperties(Location.prototype, {
    [Symbol.toStringTag]: {
        value: "Location",
        configurable: true
    }
});

location = {};
location.__proto__ = Location.prototype;

location = FrameworkProxy(location);

