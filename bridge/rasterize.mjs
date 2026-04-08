#!/usr/bin/env node
// Rasterize SVG strings to PNG using Playwright's browser.
// Input: JSON array of SVG strings on stdin
// Output: PNG files written to a directory (passed as argv[1])

import { chromium } from "playwright";
import { writeFileSync } from "fs";
import { join } from "path";

const outDir = process.argv[2];
const width = parseInt(process.argv[3] || "1920");
const height = parseInt(process.argv[4] || "1080");

if (!outDir) {
  console.error("Usage: rasterize.mjs <output_dir> [width] [height]");
  process.exit(1);
}

// Read SVG array from stdin
let input = "";
for await (const chunk of process.stdin) {
  input += chunk;
}
const svgs = JSON.parse(input);

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width, height });

for (let i = 0; i < svgs.length; i++) {
  const svg = svgs[i];
  // Render SVG in a full-page HTML with white background
  await page.setContent(`
    <!DOCTYPE html>
    <html>
    <head><style>
      body { margin: 0; background: white; display: flex; align-items: center; justify-content: center; width: ${width}px; height: ${height}px; overflow: hidden; }
      svg { width: ${width}px; height: ${height}px; }
    </style></head>
    <body>${svg}</body>
    </html>
  `, { waitUntil: "networkidle" });

  const buf = await page.screenshot({ type: "png" });
  const fname = join(outDir, `frame_${String(i).padStart(6, "0")}.png`);
  writeFileSync(fname, buf);
}

await browser.close();
process.stdout.write(JSON.stringify({ frames: svgs.length }));
