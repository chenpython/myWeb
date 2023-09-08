
// 1、测试不同文件之间 var 声明的变量不可以拿到
// 2、在一个脚本中设置了 var window; 那么window只在当前模块中有用
// 3、在脚本中不带var设置window，则认为是给 global加了window属性，window变成了全局变量
// 如何让局部的window拥有global的方法----解决部分环境污染问题？
// 如何让eval中的代码设置的全局变量不设置到全局，但是可以通过变量名直接获取？


console.log('----------start-------------');
var window = {a: 'aaaa'}
Object.defineProperties(window, {
    [Symbol.toStringTag]: {
        value: 'Window',
        configurable: true
    },
    get(target, prop, receiver) {
            return target[prop] || global[prop];
        },
});
console.log(window['a']);
console.log(window.a);
// const test1 = require('./test1');
// const test2 = require('./test2');

// console.log('ready for exeuting test1');
// test1.test1_a_1();

// console.log('ready for exeuting test2');
// test2.test2_a_1();

console.log('-----------ending-----------');

