// hook cookie 方法
(function() {
    // 严谨模式 检查所有错误
    'use strict';
    // document 为要hook的对象 这里是hook的cookie
	var cookieTemp = "";
    Object.defineProperty(document, 'cookie', {
		// hook set方法也就是赋值的方法 
		set: function(val) {
				// 这样就可以快速给下面这个代码行下断点
				// 从而快速定位设置cookie的代码
				console.log('Hook捕获到cookie设置->', val);
                debugger;
				cookieTemp = val;
				return val;
		},
		// hook get 方法也就是取值的方法 
		get: function()
		{
			return cookieTemp;
		}
    });
})();

// hook 指定 cookie 方法
(function() {
    // 严谨模式 检查所有错误
    'use strict';
    // document 为要hook的对象 这里是hook的cookie
	var cookieTemp = "";
    Object.defineProperty(document, 'cookie', {
		// hook set方法也就是赋值的方法 
		set: function(val) {
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
		get: function()
		{
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
var laowang_proxy = function(obj){
    return new Proxy(obj, {
        set(target, prop, value){
            console.log('set -->', target[Symbol.toStringTag], '-->', prop, '-->', value);
            return Reflect.set(...arguments);
        },
        get(target, prop, receiver){
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
