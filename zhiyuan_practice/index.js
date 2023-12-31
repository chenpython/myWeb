// 使用纯净 V8 环境运行代码

var fs = require("fs");

const { VM, VMScript } = require("vm2");

const file = `${__dirname}/code.js`;
const windowFile = `${__dirname}/window.js`;    // 引入自定义 window 环境


const vm = new VM();
const script = new VMScript(fs.readFileSync(windowFile) + fs.readFileSync(file), "MyEnvironment");


debugger;

vm.run(script);

debugger;

