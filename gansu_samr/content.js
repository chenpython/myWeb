function contentHandler(filePath = '/gansu_samr/home_html') {
    var fs = require('fs');
    var path = require("path");

    var file_path = path.join(path.dirname(__dirname), filePath);
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


    return content
}
module.exports = { contentHandler: contentHandler };