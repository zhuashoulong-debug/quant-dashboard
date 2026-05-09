from __future__ import annotations

import argparse
import json
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd

from formula_lab.data_service import load_daily_with_indicators, stock_from_pool
from formula_lab.stock_pool import normalize_stock_code, read_stock_pool
from formula_lab.validation_views import VALIDATION_VIEWS


HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>公式验证实验室</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>
    :root {
      color-scheme: dark;
      --bg: #111111;
      --panel: #181818;
      --line: #2f3430;
      --text: #e7e1d5;
      --muted: #9c978c;
      --accent: #ffd800;
      --cyan: #00d7d7;
      --magenta: #d300d3;
      --red: #ff4b4b;
      --green: #00d084;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
      font-size: 14px;
    }

    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 310px;
      background: var(--bg);
    }

    .stage {
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      min-width: 0;
      border-right: 1px solid var(--line);
    }

    header {
      height: 52px;
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 0 18px;
      border-bottom: 1px solid var(--line);
      background: #151515;
    }

    .brand {
      font-size: 17px;
      font-weight: 700;
      color: #f2ece2;
      white-space: nowrap;
    }

    .toolbar {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      min-width: 0;
    }

    label {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--muted);
      font-size: 12px;
    }

    input {
      width: 104px;
      height: 30px;
      border: 1px solid #3a3a3a;
      border-radius: 4px;
      background: #0d0d0d;
      color: var(--text);
      padding: 0 8px;
      font: inherit;
    }

    input[type="text"] {
      width: 82px;
    }

    button {
      height: 30px;
      border: 1px solid #595032;
      border-radius: 4px;
      background: #2a2410;
      color: #ffe36c;
      padding: 0 12px;
      font: inherit;
      cursor: pointer;
    }

    button:disabled {
      cursor: wait;
      opacity: 0.62;
    }

    #chart {
      width: 100%;
      height: calc(100vh - 52px);
      min-height: 620px;
    }

    aside {
      display: grid;
      grid-template-rows: auto auto minmax(0, 1fr) auto;
      background: var(--panel);
    }

    .quote {
      padding: 18px;
      border-bottom: 1px solid var(--line);
    }

    .code {
      color: var(--muted);
      font-size: 13px;
    }

    .name {
      margin-top: 4px;
      font-size: 24px;
      font-weight: 700;
      color: #f4ead7;
    }

    .price {
      margin-top: 10px;
      font-size: 38px;
      font-weight: 800;
      color: var(--red);
      line-height: 1;
    }

    .metrics {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1px;
      background: var(--line);
      border-bottom: 1px solid var(--line);
    }

    .metric {
      background: var(--panel);
      padding: 12px 14px;
      min-width: 0;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 4px;
    }

    .metric strong {
      display: block;
      color: var(--text);
      font-size: 17px;
      overflow-wrap: anywhere;
    }

    .diagnostics {
      padding: 14px 18px;
      overflow: auto;
      border-bottom: 1px solid var(--line);
    }

    .diag-title {
      margin: 0 0 10px;
      color: #f4ead7;
      font-size: 14px;
      font-weight: 700;
    }

    .view-tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-bottom: 10px;
    }

    .view-tab {
      height: 28px;
      border: 1px solid #33382f;
      background: #121512;
      color: var(--muted);
      padding: 0 8px;
      text-align: center;
    }

    .view-tab.active {
      border-color: #6d612d;
      background: #29240f;
      color: #ffe36c;
    }

    .diag-desc {
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }

    .diag-grid {
      display: grid;
      gap: 7px;
    }

    .diag-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 46px;
      align-items: center;
      gap: 8px;
      min-height: 26px;
      border-bottom: 1px solid #242824;
    }

    .diag-name {
      color: var(--muted);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .diag-state {
      color: #7f8580;
      text-align: right;
      font-weight: 700;
    }

    .diag-state.on {
      color: var(--green);
    }

    .diag-state.num {
      color: #f3e9c0;
      font-variant-numeric: tabular-nums;
    }

    .log {
      padding: 14px 18px;
      color: var(--muted);
      line-height: 1.7;
      overflow: auto;
    }

    .ok {
      color: var(--green);
    }

    .warn {
      color: #ffbd4a;
    }

    @media (max-width: 980px) {
      .shell {
        grid-template-columns: 1fr;
      }

      aside {
        display: none;
      }

      header {
        height: auto;
        min-height: 58px;
        align-items: flex-start;
        flex-direction: column;
        padding: 12px;
      }

      #chart {
        height: calc(100vh - 112px);
        min-height: 520px;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="stage">
      <header>
        <div class="brand">公式验证实验室</div>
        <form class="toolbar" id="controls">
          <label>代码 <input id="code" type="text" value="002222" maxlength="6" /></label>
          <label>起始 <input id="start" type="text" value="20240101" maxlength="8" /></label>
          <label>结束 <input id="end" type="text" value="" maxlength="8" /></label>
          <button id="load" type="submit">刷新</button>
        </form>
      </header>
      <div id="chart"></div>
    </section>

    <aside>
      <section class="quote">
        <div class="code" id="stockCode">--</div>
        <div class="name" id="stockName">--</div>
        <div class="price" id="closePrice">--</div>
      </section>
      <section class="metrics">
        <div class="metric"><span>PCTB</span><strong id="pctb">--</strong></div>
        <div class="metric"><span>BOLL</span><strong id="boll">--</strong></div>
        <div class="metric"><span>成交额</span><strong id="amount">--</strong></div>
        <div class="metric"><span>日期</span><strong id="lastDate">--</strong></div>
      </section>
      <section class="diagnostics">
        <h2 class="diag-title" id="diagTitle">断点条件</h2>
        <div class="view-tabs" id="viewTabs"></div>
        <p class="diag-desc" id="diagDesc"></p>
        <div class="diag-grid" id="diagnostics"></div>
      </section>
      <section class="log" id="log"></section>
    </aside>
  </main>

  <script>
    const chart = echarts.init(document.getElementById("chart"));
    const controls = document.getElementById("controls");
    const endInput = document.getElementById("end");
    const loadButton = document.getElementById("load");
    const log = document.getElementById("log");
    const diagnostics = document.getElementById("diagnostics");
    const diagTitle = document.getElementById("diagTitle");
    const diagDesc = document.getElementById("diagDesc");
    const viewTabs = document.getElementById("viewTabs");
    let currentRows = [];
    let currentPayload = null;
    let currentRow = null;
    let currentViewId = "overview";

    function todayText() {
      const d = new Date();
      return `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, "0")}${String(d.getDate()).padStart(2, "0")}`;
    }

    function fixed(value, digits = 2) {
      if (value === null || value === undefined || Number.isNaN(value)) return "--";
      return Number(value).toFixed(digits);
    }

    function amountText(value) {
      if (!value && value !== 0) return "--";
      if (value >= 100000000) return `${(value / 100000000).toFixed(2)}亿`;
      if (value >= 10000) return `${(value / 10000).toFixed(2)}万`;
      return fixed(value, 0);
    }

    function setStatus(text, tone = "") {
      log.innerHTML = `<span class="${tone}">${text}</span>`;
    }

    function truthy(value) {
      return value === true || value === 1;
    }

    function conditionRow(field, row) {
      const value = row[field.key];
      if (field.kind === "number") {
        return `
          <div class="diag-row">
            <span class="diag-name" title="${field.label}">${field.label}</span>
            <span class="diag-state num">${fixed(value, field.digits ?? 2)}</span>
          </div>
        `;
      }
      const active = truthy(value);
      return `
        <div class="diag-row">
          <span class="diag-name" title="${field.label}">${field.label}</span>
          <span class="diag-state ${active ? "on" : ""}">${active ? "是" : "否"}</span>
        </div>
      `;
    }

    function activeView() {
      return currentPayload?.views?.find((view) => view.id === currentViewId) || currentPayload?.views?.[0];
    }

    function renderViewTabs() {
      const views = currentPayload?.views || [];
      viewTabs.innerHTML = views.map((view) => `
        <button class="view-tab ${view.id === currentViewId ? "active" : ""}" data-view="${view.id}" type="button">${view.label}</button>
      `).join("");
    }

    function renderDiagnostics(row) {
      const view = activeView();
      diagTitle.textContent = `${view?.label || "断点条件"} ${row.date}`;
      diagDesc.textContent = view?.description || "";
      diagnostics.innerHTML = (view?.fields || []).map((field) => conditionRow(field, row)).join("");
    }

    function renderSide(payload, row) {
      document.getElementById("stockCode").textContent = payload.stock.code;
      document.getElementById("stockName").textContent = payload.stock.name || payload.stock.code;
      document.getElementById("closePrice").textContent = fixed(row.close, 2);
      document.getElementById("pctb").textContent = fixed(row.pctb, 3);
      document.getElementById("boll").textContent = fixed(row.boll_mid, 2);
      document.getElementById("amount").textContent = amountText(row.amount);
      document.getElementById("lastDate").textContent = row.date;
      currentRow = row;
      renderViewTabs();
      renderDiagnostics(row);
    }

    function render(payload) {
      const rows = payload.data;
      currentRows = rows;
      currentPayload = payload;
      const dates = rows.map((row) => row.date);
      const kline = rows.map((row) => [row.open, row.close, row.low, row.high]);
      const volume = rows.map((row) => row.volume);
      const mid = rows.map((row) => row.boll_mid);
      const upper = rows.map((row) => row.boll_upper);
      const lower = rows.map((row) => row.boll_lower);
      const pctb = rows.map((row) => row.pctb);
      const last = rows[rows.length - 1];

      renderSide(payload, last);

      chart.setOption({
        backgroundColor: "#111111",
        animation: false,
        axisPointer: { link: [{ xAxisIndex: "all" }] },
        tooltip: {
          trigger: "axis",
          axisPointer: { type: "cross" },
          backgroundColor: "rgba(24,24,24,0.92)",
          borderColor: "#454545",
          textStyle: { color: "#e7e1d5" },
        },
        grid: [
          { left: 56, right: 24, top: 28, height: "52%" },
          { left: 56, right: 24, top: "64%", height: "12%" },
          { left: 56, right: 24, top: "81%", height: "14%" },
        ],
        xAxis: [
          { type: "category", data: dates, gridIndex: 0, boundaryGap: true, axisLine: { lineStyle: { color: "#444" } }, axisLabel: { color: "#aaa" } },
          { type: "category", data: dates, gridIndex: 1, boundaryGap: true, axisLine: { lineStyle: { color: "#444" } }, axisLabel: { show: false } },
          { type: "category", data: dates, gridIndex: 2, boundaryGap: true, axisLine: { lineStyle: { color: "#444" } }, axisLabel: { color: "#aaa" } },
        ],
        yAxis: [
          { scale: true, gridIndex: 0, splitLine: { lineStyle: { color: "#2b2b2b", type: "dashed" } }, axisLabel: { color: "#aaa" } },
          { scale: true, gridIndex: 1, splitLine: { lineStyle: { color: "#2b2b2b", type: "dashed" } }, axisLabel: { color: "#aaa" } },
          { scale: true, gridIndex: 2, splitLine: { lineStyle: { color: "#2b2b2b", type: "dashed" } }, axisLabel: { color: "#aaa" } },
        ],
        dataZoom: [
          { type: "inside", xAxisIndex: [0, 1, 2], start: 64, end: 100 },
          { type: "slider", xAxisIndex: [0, 1, 2], bottom: 6, height: 18, borderColor: "#333", textStyle: { color: "#aaa" } },
        ],
        series: [
          {
            name: "K线",
            type: "candlestick",
            data: kline,
            itemStyle: {
              color: "#ff4b4b",
              color0: "#00d7d7",
              borderColor: "#ff4b4b",
              borderColor0: "#00d7d7",
            },
          },
          { name: "BOLL", type: "line", data: mid, showSymbol: false, lineStyle: { width: 1, color: "#d8d8d8" } },
          { name: "UPPER", type: "line", data: upper, showSymbol: false, lineStyle: { width: 1, color: "#e4d000" } },
          { name: "LOWER", type: "line", data: lower, showSymbol: false, lineStyle: { width: 1, color: "#d300d3" } },
          { name: "成交量", type: "bar", xAxisIndex: 1, yAxisIndex: 1, data: volume, itemStyle: { color: "#4b9cff" } },
          {
            name: "PCTB",
            type: "line",
            xAxisIndex: 2,
            yAxisIndex: 2,
            data: pctb,
            showSymbol: false,
            lineStyle: { width: 2, color: "#ffd800" },
            markLine: {
              symbol: "none",
              label: { color: "#aaa" },
              lineStyle: { color: "#686868", type: "dashed" },
              data: [{ yAxis: 0 }, { yAxis: 0.5 }, { yAxis: 1 }],
            },
          },
        ],
      }, true);

      setStatus(`已加载 ${rows.length} 根K线；口径：AKShare 前复权 qfq。`, "ok");
    }

    async function loadData(event) {
      event?.preventDefault();
      loadButton.disabled = true;
      setStatus("加载中...");
      const params = new URLSearchParams({
        code: document.getElementById("code").value.trim(),
        start: document.getElementById("start").value.trim(),
        end: endInput.value.trim(),
      });
      try {
        const response = await fetch(`/api/daily?${params}`);
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || response.statusText);
        render(payload);
      } catch (error) {
        setStatus(error.message, "warn");
      } finally {
        loadButton.disabled = false;
      }
    }

    window.addEventListener("resize", () => chart.resize());
    chart.on("click", (params) => {
      if (!currentPayload || !currentRows.length || params.dataIndex === undefined) return;
      const row = currentRows[params.dataIndex];
      if (row) renderSide(currentPayload, row);
    });
    viewTabs.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-view]");
      if (!button || !currentRow) return;
      currentViewId = button.dataset.view;
      renderSide(currentPayload, currentRow);
    });
    controls.addEventListener("submit", loadData);
    endInput.value = todayText();
    loadData();
  </script>
</body>
</html>
"""


def _json_value(value: object) -> object:
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    if hasattr(value, "item"):
        return value.item()
    return value


def _records(data: pd.DataFrame) -> list[dict[str, object]]:
    return [
        {key: _json_value(value) for key, value in row.items()}
        for row in data.to_dict(orient="records")
    ]


class FormulaLabHandler(BaseHTTPRequestHandler):
    pool_path: Path
    cache_root: Path

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html(HTML)
            return
        if parsed.path == "/api/health":
            self._send_json({"ok": True, "date": date.today().isoformat()})
            return
        if parsed.path == "/api/stocks":
            self._handle_stocks()
            return
        if parsed.path == "/api/daily":
            self._handle_daily(parse_qs(parsed.query))
            return
        self.send_error(HTTPStatus.NOT_FOUND, "not found")

    def log_message(self, format: str, *args: object) -> None:
        return

    def _handle_stocks(self) -> None:
        stocks = read_stock_pool(self.pool_path)
        self._send_json({"stocks": [stock.__dict__ for stock in stocks]})

    def _handle_daily(self, query: dict[str, list[str]]) -> None:
        try:
            code = normalize_stock_code(query.get("code", ["002222"])[0])
            start = query.get("start", ["20240101"])[0]
            end = query.get("end", [date.today().strftime("%Y%m%d")])[0]
            refresh = query.get("refresh", ["0"])[0] in {"1", "true", "yes"}
            stock = stock_from_pool(self.pool_path, code)
            data = load_daily_with_indicators(
                stock=stock,
                start_date=start,
                end_date=end,
                cache_root=self.cache_root,
                refresh=refresh,
            )
            self._send_json(
                {
                    "stock": stock.__dict__,
                    "source": "akshare.stock_zh_a_hist",
                    "adjust": "qfq",
                    "views": VALIDATION_VIEWS,
                    "data": _records(data),
                }
            )
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _send_html(self, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local formula validation lab.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=52410)
    parser.add_argument("--pool", default=r"D:\数据包.xlsx")
    parser.add_argument("--cache-root", default="data/raw")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    handler = type(
        "ConfiguredFormulaLabHandler",
        (FormulaLabHandler,),
        {
            "pool_path": Path(args.pool),
            "cache_root": Path(args.cache_root),
        },
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"formula lab listening on http://{args.host}:{args.port}/")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
