const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({

        headless: false,
        executablePath: '/Applications/Google Chrome.app/',
        args: ["--app-shell-host-window-size=1600x1239"]


    });
    const page = await browser.newPage();
    await page.goto('http://localhost:8282/publisher/login', {
        waitUntil: 'load'
    });
    await page.screenshot({ path: '../screenshots/cms-local.png' });

    //await browser.close();
})();