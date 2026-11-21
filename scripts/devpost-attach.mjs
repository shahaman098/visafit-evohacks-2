#!/usr/bin/env node
/**
 * Attach VisaFit to EvoHacks 2 on Devpost via chrome-agent CDP (:9223).
 *
 * Usage:
 *   node scripts/devpost-attach.mjs              # stop before final Submit
 *   node scripts/devpost-attach.mjs --submit     # click final Submit + screenshot
 *
 * Requires: gate open, signed-in shahaman098 in ~/.chrome-agent/shared,
 * playwright installed (uses npx playwright if needed).
 */
import { chromium } from "playwright";
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const MANAGE =
  "https://devpost.com/submit-to/31721-evohacks-2/manage/submissions";
const ART =
  "/Users/efi/VIP/Sheets/Daily Log sheet/artifacts/2026-11-21/evohacks-2";
const doSubmit = process.argv.includes("--submit");

function gateOpen() {
  try {
    execSync(`bash "${ART}/poll-gate.sh"`, { stdio: "pipe" });
    return true;
  } catch (e) {
    return e.status === 0;
  }
}

async function main() {
  if (!gateOpen()) {
    console.error("BLOCKED: Devpost gate still closed (poll-gate).");
    process.exit(2);
  }

  const browser = await chromium.connectOverCDP("http://127.0.0.1:9223");
  const context = browser.contexts()[0] || (await browser.newContext());
  const page = context.pages()[0] || (await context.newPage());

  await page.goto(MANAGE, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(1500);
  const body = await page.locator("body").innerText();
  if (/Submissions open soon/i.test(body)) {
    console.error("BLOCKED: manage page still says Submissions open soon");
    process.exit(2);
  }

  const submitProject = page.getByRole("link", { name: /Submit a project/i }).or(
    page.getByRole("button", { name: /Submit a project/i })
  );
  if ((await submitProject.count()) === 0) {
    // Sometimes it's "Create a project to submit" or pick existing
    console.log("No Submit a project CTA yet; dumping headings:");
    console.log(body.slice(0, 800));
    process.exit(3);
  }
  await submitProject.first().click();
  await page.waitForTimeout(2000);

  // Pick VisaFit from software list / search
  const visa = page.getByText(/^VisaFit$/i).or(page.getByRole("link", { name: /VisaFit/i }));
  if (await visa.count()) {
    await visa.first().click();
    await page.waitForTimeout(1500);
  } else {
    const search = page.getByPlaceholder(/search/i).first();
    if (await search.count()) {
      await search.fill("VisaFit");
      await page.waitForTimeout(800);
      await page.getByText(/VisaFit/i).first().click();
    }
  }

  // Confirm we're on a submission form
  await page.waitForTimeout(1000);
  const after = await page.locator("body").innerText();
  fs.writeFileSync(path.join(ART, "attach-page.txt"), after.slice(0, 4000));
  console.log("Attach page captured → artifacts/.../attach-page.txt");

  if (!doSubmit) {
    console.log("Dry run complete. Re-run with --submit to press final Submit.");
    process.exit(0);
  }

  const finalBtn = page
    .getByRole("button", { name: /^(Submit|Finish|Submit project)$/i })
    .or(page.getByRole("button", { name: /Submit/i }));
  if ((await finalBtn.count()) === 0) {
    console.error("No final Submit button found");
    process.exit(4);
  }
  await finalBtn.first().click();
  await page.waitForTimeout(3000);
  const shot = path.join(ART, "submitted.png");
  await page.screenshot({ path: shot, fullPage: true });
  fs.writeFileSync(
    path.join(ART, "submitted.txt"),
    await page.locator("body").innerText()
  );
  console.log("Submitted. Screenshot:", shot);
  console.log("URL:", page.url());
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
