// Print one HTML file to PDF with the Chromium that ships with market-ui's Playwright.
import { pathToFileURL } from 'node:url';
import { chromium } from '/Users/harsh/anvest/market-ui/node_modules/playwright/index.mjs';
const [input, output] = process.argv.slice(2);
const b = await chromium.launch();
const page = await b.newPage();
await page.goto(pathToFileURL(input).href, { waitUntil: 'networkidle' });
await page.pdf({ path: output, format: 'A4', printBackground: true, preferCSSPageSize: true });
console.log(output);
await b.close();
