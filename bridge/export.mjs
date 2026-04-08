#!/usr/bin/env node
// Bridge script: reads Excalidraw element JSON from stdin, outputs SVG via Playwright.
// Uses a persistent browser page for fast repeated renders.

import { chromium } from "playwright";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const htmlPath = join(__dirname, "index.html");

// Read JSON from stdin
let input = "";
for await (const chunk of process.stdin) {
  input += chunk;
}

const data = JSON.parse(input);
const frames = Array.isArray(data) ? data : [data];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(`file://${htmlPath}`);

// Wait for ExcalidrawLib to be available
await page.waitForFunction(() => window.bridgeReady === true, {
  timeout: 30000,
});

const results = [];
for (const frame of frames) {
  const svg = await page.evaluate(
    async ({ elements, appState, files }) => {
      return await window.renderToSvg(elements || [], appState, files);
    },
    frame,
  );
  results.push(svg);
}

await browser.close();

if (Array.isArray(data)) {
  process.stdout.write(JSON.stringify(results));
} else {
  process.stdout.write(results[0]);
}
