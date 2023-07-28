function contentHandler() {
    var fs = require('fs');
    var path = require("path");

    var file_path = path.join(path.dirname(__dirname), '/fangdichan/home_html');
    var res = fs.readFileSync(file_path, { encoding: 'utf8', flag: 'r' });
    data = res.toString()
    var matches = data.match(/<meta[^>]*content=["']([^"']*)["'][^>]*>/gi);

    // // 提取content值
    var contentValues = matches.map((match) => {
        const contentValueRegex = /content=["']([^"']*)["']/i;
        const result = contentValueRegex.exec(match);
        return result ? result[1] : null;
    });
    var content = contentValues[1]


    matches = data.match(/<script type="text\/javascript"[\s]+r="m">[(\w()\s{}\$=,\[\];\.%-+-<!\\>"|/\?:]+\(\)<\/script>/gim);
    contentValues = matches.map((match) => {
        const contentValueRegex = /\([(\w()\s{}\$=,\[\];\.%-+-<!\\>"|/\?:]+\)\(\)/i;
        const result = contentValueRegex.exec(match);
        return result ? result[0] : null;
    });
    var home_js_code = contentValues[0]

    return [content, home_js_code]
}
module.exports = { contentHandler: contentHandler };

