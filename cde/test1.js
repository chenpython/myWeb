
var a1 = 'test111111';
var window = {
    a1: a1
};

function a_1(){
    // debugger;
    console.log('Now enter in test1');
    console.log('In test1 window[a1]: ', window['a1']);
    console.log('In test1 window.a1: ', window.a1);
    console.log('In test1 a1: ', a1);
    vm_code = 'console.log("In test1 eval: a1 -> ", a1);'
    eval( vm_code)
    console.log('Now exit from test1');
}

module.exports = {
    test1_a_1: a_1
}