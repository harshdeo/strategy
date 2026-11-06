// Public, signed-out captures for the appendix product page. Light theme, as a new visitor sees it.
import { chromium } from '/Users/harsh/anvest/market-ui/node_modules/playwright/index.mjs';
const out = new URL('./capture/', import.meta.url).pathname;
const pages = [['t_stock','/stocks/TCS'],['t_ipo','/ipo/jio-platforms-ltd'],['t_mf','/mutual-funds'],['t_bonds','/bonds'],['t_screens','/screeners'],['t_filings','/news'],['t_home','/']];
const b = await chromium.launch();
const c = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
for (const [n, p] of pages) {
  const pg = await c.newPage();
  try { await pg.goto('https://anvest.in' + p, { waitUntil: 'networkidle', timeout: 60000 }); } catch (e) { console.log('slow', p); }
  await pg.waitForTimeout(2500);
  await pg.screenshot({ path: out + n + '.png' });
  console.log(n, pg.url());
  await pg.close();
}
await b.close();
