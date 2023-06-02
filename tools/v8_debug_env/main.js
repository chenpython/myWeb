// 使用纯净 V8 环境运行代码

var fs = require("fs");

const {VM} = require("vm2");
const vm = new VM();

path = '/home/feng/workspace/myWeb/js/阿里滑块验证js'
var data = fs.readFileSync(path, 'utf-8');

debugger;

vm.run(data);

debugger;
