const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const base = path.resolve(__dirname, "..");
const timestamp = new Date().toISOString().replace(/[-:]/g, "").replace(".", "").replace("Z", "Z");
const runDir = path.join(base, "outputs", "test_runs", timestamp);
fs.mkdirSync(runDir, { recursive: true });

const allowMock = process.argv.includes("--allow-mock-llm");
const port = process.env.INFORMATION_WORKSPACE_FRONTEND_SMOKE_PORT || "8799";
const env = {
  ...process.env,
  INFORMATION_WORKSPACE_DB_PATH: path.join(runDir, "frontend_smoke.db"),
  INFORMATION_WORKSPACE_OUTPUTS_DIR: path.join(base, "outputs"),
  INFORMATION_WORKSPACE_API_PORT: port,
};
if (allowMock) {
  env.INFORMATION_WORKSPACE_LLM_PROVIDER = "mock";
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForHealth() {
  const deadline = Date.now() + 20000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`http://127.0.0.1:${port}/api/health`);
      if (response.ok) return;
    } catch (_) {
      // keep waiting
    }
    await wait(400);
  }
  throw new Error("backend did not become healthy");
}

async function main() {
  const server = spawn("python3", ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", port], {
    cwd: base,
    env,
    stdio: ["ignore", "pipe", "pipe"],
  });
  const serverLog = [];
  server.stdout.on("data", (chunk) => serverLog.push(chunk.toString()));
  server.stderr.on("data", (chunk) => serverLog.push(chunk.toString()));
  try {
    await waitForHealth();
    const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
    const launchOptions = fs.existsSync(chromePath)
      ? { headless: true, executablePath: chromePath }
      : { headless: true };
    const browser = await chromium.launch(launchOptions);
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const dialogAnswers = [
      "Frontend Smoke Topic",
      "Organize frontend smoke materials around evidence",
      true,
      true,
      true,
    ];
    page.on("dialog", async (dialog) => {
      const answer = dialogAnswers.shift();
      if (dialog.type() === "prompt") await dialog.accept(String(answer || "Frontend smoke"));
      else if (dialog.type() === "confirm") {
        if (answer === false) await dialog.dismiss();
        else await dialog.accept();
      } else {
        await dialog.accept();
      }
    });

    await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "networkidle" });
    await page.screenshot({ path: path.join(runDir, "01-dashboard.png"), fullPage: true });

    await page.click('button[data-view="upload"]');
    await page.fill("#singleTitle", "Frontend smoke upload material");
    await page.fill("#singleContent", "This synthetic frontend smoke material validates that upload, auto-process, material search, Event creation, Topic refresh, and export buttons call real backend APIs.");
    await page.fill("#singleSourceName", "Frontend Smoke");
    await page.check("#uploadAutoProcess");
    if (allowMock) await page.check("#uploadMockLlm");
    await page.click("#singleUploadForm button[type='submit']");
    await page.waitForFunction(() => document.querySelector("#uploadResult").textContent.includes("run"));

    await page.click('button[data-view="materials"]');
    await page.click("#searchMaterials");
    await page.waitForSelector(".select-material");
    await page.check(".select-material");
    await page.click(".open-material");
    await page.waitForSelector("#materialDetail .source-text");
    await page.screenshot({ path: path.join(runDir, "02-material-detail.png"), fullPage: true });

    await page.click("#createTopicFromSelected");
    await page.waitForSelector("#topicDetail h3");
    await page.click(".refresh-topic");
    await page.waitForTimeout(1000);
    await page.click(".confirm-topic");
    await page.waitForTimeout(500);
    await page.click(".export-topic");

    await page.click('button[data-view="materials"]');
    await page.click("#createEventFromSelected");
    await page.waitForSelector("#eventDetail h3");
    await page.screenshot({ path: path.join(runDir, "03-event-topic.png"), fullPage: true });

    await browser.close();
    const summaryPath = path.join(runDir, "frontend_smoke_summary.md");
    fs.writeFileSync(
      summaryPath,
      [
        "# Frontend Smoke Summary",
        "",
        `- Created: ${new Date().toISOString()}`,
        `- URL: http://127.0.0.1:${port}/`,
        `- allow_mock_llm: ${allowMock}`,
        `- Database: ${env.INFORMATION_WORKSPACE_DB_PATH}`,
        "- Result: PASSED",
        "",
        "## Screenshots",
        "",
        "- 01-dashboard.png",
        "- 02-material-detail.png",
        "- 03-event-topic.png",
        "",
        "Mock LLM mode is test-only and does not satisfy final DeepSeek READY validation.",
      ].join("\n"),
      "utf8",
    );
    console.log(JSON.stringify({ summary_path: summaryPath, run_dir: runDir }, null, 2));
  } finally {
    server.kill("SIGTERM");
    fs.writeFileSync(path.join(runDir, "server.log"), serverLog.join(""), "utf8");
  }
}

main().catch((error) => {
  const summaryPath = path.join(runDir, "frontend_smoke_summary.md");
  fs.writeFileSync(
    summaryPath,
    `# Frontend Smoke Summary\n\n- Created: ${new Date().toISOString()}\n- Result: FAILED\n- Error: ${error.stack || error.message}\n`,
    "utf8",
  );
  console.error(error);
  process.exit(1);
});
