const vm = require('vm');





function a_1(){
    // var a1 = 'test111111';
    var window = Object.assign({a: 'aaaa'}, global);
    window.window = window;
    window['test1111'] = 'test1111';

    const sandbox = window;

    vm.createContext(sandbox);

    console.log('Now enter in test1');
    console.log('In test1 window[a]: ', window['a']);
    console.log('In test1 window.a: ', window.a);
    // console.log('In test1 a1: ', a1);
    // vm_code = 'debugger;console.log("In test1 eval: bbb -> ", bbb);';
    // vm_code = "vm_a2 = 'test1_vm_code';debugger;"
    // eval(vm_code);
    // var vm_code =  'debugger;console.log("设置全局变量bbb");' + 'bbb="bbbbbb";'  + "" + 'eval("debugger;console.log(' + "'bbb -> ', bbb, 'window.a -> ', window.a);" + '");';
    // var vm_code = 'debugger;function aaa(){xxx=111};function bbb(){return xxx+1}; aaa();console.log(bbb());';
    // vm.runInContext(vm_code, sandbox);
    // vm.runInContext('debugger;console.log("bbb -> ", bbb);', sandbox);
    console.log('Now exit from test1');
}

module.exports = {
    test1_a_1: a_1
}
