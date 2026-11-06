// Captures public anvest.in pages (signed out) for the deck exhibits. Nothing is edited after capture.
import { chromium } from '/Users/harsh/anvest/market-ui/node_modules/playwright/index.mjs';
const out = new URL('./capture/', import.meta.url).pathname;
const pages = [['home','/'],['retirement','/retirement-planning'],['wealthmgmt','/wealth-management'],['simulator','/simulator'],['research','/research'],['calculators','/calculators'],['screener','/screener?query=profit_margin%20%3E%200%20AND%20roe%20%3E%2015%20AND%20debt_to_equity%20%3C%201'],['planning','/planning']];
const b = await chromium.launch();
const c = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
for (const [n, p] of pages) {
  const pg = await c.newPage();
  try {
    await pg.goto('https://anvest.in' + p, { waitUntil: 'networkidle', timeout: 60000 });
  } catch (e) { console.log('slow', p); }
  await pg.waitForTimeout(2500);
  await pg.screenshot({ path: out + n + '.png' });
  const t = await pg.evaluate(() => document.body.innerText.slice(0, 900));
  console.log('=== ' + n + ' ' + pg.url() + '\n' + t.replace(/\n+/g, ' | '));
  await pg.close();
}
await b.close();
