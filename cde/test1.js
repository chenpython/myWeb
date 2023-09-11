const vm = require('vm');


// var a1 = 'test111111';
var window = {a: 'aaaa'};
window.window = window;

const sandbox = window;

vm.createContext(sandbox);



function a_1(){
    debugger;
    console.log('Now enter in test1');
    console.log('In test1 window[a]: ', window['a']);
    console.log('In test1 window.a: ', window.a);
    // console.log('In test1 a1: ', a1);
    // vm_code = 'debugger;console.log("In test1 eval: bbb -> ", bbb);';
    // vm_code = "vm_a2 = 'test1_vm_code';debugger;"
    // eval(vm_code);
    // var vm_code =  'debugger;console.log("设置全局变量bbb");' + 'bbb="bbbbbb";'  + "" + 'eval("debugger;console.log(' + "'bbb -> ', bbb, 'window.a -> ', window.a);" + '");';
    var vm_code = 'debugger;console.log("window.Math -> ", window["Math"]);';
    vm.runInContext(vm_code, sandbox);
    // vm.runInContext('debugger;console.log("bbb -> ", bbb);', sandbox);
    console.log('Now exit from test1');
}

module.exports = {
    test1_a_1: a_1
}
