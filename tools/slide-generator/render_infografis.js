const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright-core");

(async () => {
  const htmlPath = process.argv[2];
  const outPng = process.argv[3];
  let html = fs.readFileSync(htmlPath, "utf8");

  const logoPath = path.join(__dirname, "..", "..", "logo_jbridgecenter.png");
  const logoB64 = fs.readFileSync(logoPath).toString("base64");
  html = html.replace("LOGO_SRC", `data:image/png;base64,${logoB64}`);

  const tmp = htmlPath.replace(/\.html$/, ".rendered.html");
  fs.writeFileSync(tmp, html);

  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 }, deviceScaleFactor: 2 });
  await page.goto("file://" + path.resolve(tmp));
  await page.waitForTimeout(200);
  await page.screenshot({ path: outPng, fullPage: true });
  await browser.close();
  console.log("wrote", outPng);
})();
