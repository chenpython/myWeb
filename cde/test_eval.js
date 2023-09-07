

// global = {};
window = global;
// window = {
//     test: 'dddddddddd'
// };

// wv = {
//     x: 111,
//     y: 2222
// };

window.a = "xxxx";

vm_code_1 = "console.log('window.a: ', window['a']);";
vm_code_2 = "console.log('window.a: ', window.a);";
vm_code_3 = "console.log('a: ', a);";
vm_code_4 = "debugger;"
vm_code_5 = "eval('debugger;')";

vm_code = vm_code_4 + vm_code_1 + vm_code_2 + vm_code_3

eval.call(window, vm_code);

// eval 和 window.eval 的区别
// 1、eval在函数内部执行时，仅代表当前作用域，而window.eval代表全局作用域
// 2、当执行：let eval_ = eval; eval('code')，此时eval与window.eval相等


// 1、eval执行代码 = node新开一个文件执行，共用global；
// 2、eval中的代码能够获取到window是因为在脚本中定义啦window，并且设置在global上面


// 只有 window 与 global 一样时，才可以直接获取变量值

// 方案：
// 重新拷贝一份独立的global -> myGlobal，让window只想myGlobal
// 直接将gloabl值为空，修改的事全局的global
