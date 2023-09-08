
var a2 = 'test222222';

function a_1(){
    debugger;
    console.log('Now enter in test2');
    console.log('In test2 window[a1]: ', window['a1']);
    console.log('In test2 window.a1: ', window.a1);
    console.log('In test2 a1: ', a1);
    vm_code = 'console.log("In test2 eval: a1 -> ", a2);'
    eval( vm_code)
    console.log('Now exit from test2');
}

module.exports = {
    test2_a_1: a_1
}