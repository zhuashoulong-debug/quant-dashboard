# Download Status

Snapshot time: `2026-05-11 14:54 +08:00`

## Rule

The download process must not be stopped because of exit, new chat, or handoff. Only inspect progress and record status.

## Active Command

```powershell
.\.venv-py314\Scripts\python.exe -m scripts.download_market_data --start 20100101 --end 20260509 --cache-root data/raw --workers 1 --sleep 0.25 --retries 2 --retry-sleep 2 --resume-from-manifest --per-stock-timeout 90
```

## Observed Processes

- Downloader process observed: `20348`
- Downloader child/helper process observed: `9488`
- Local formula lab process observed: `9504`
- Local formula lab child/helper process observed: `2532`

Process IDs can change after restart. On resume, identify by command line, not by PID alone.

## Latest Progress Around Snapshot

- Manifest: `D:\我的文档\Documents\New project 3\data\raw\akshare\qfq\daily\download_manifest.jsonl`
- Remaining batch: `1310`
- Latest confirmed tail around snapshot: `index=55 / total=1310`
- Latest confirmed code around snapshot: `603599`
- Latest confirmed status: `downloaded`
- Latest CSV around snapshot: `603599_20100101_20260509.csv`
- CSV count around snapshot: `4263`

## Logs

- `D:\我的文档\Documents\New project 3\logs\download-market-data-resume-20260511-143430.out.log`
- `D:\我的文档\Documents\New project 3\logs\download-market-data-resume-20260511-143430.err.log`

## Resume Check

Use read-only inspection:

```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'scripts.download_market_data|formula_lab.local_server' }
Get-Content .\logs\download-market-data-resume-20260511-143430.out.log -Tail 40
Get-Content .\data\raw\akshare\qfq\daily\download_manifest.jsonl -Tail 5
```

Do not run `Stop-Process` unless the user explicitly asks or a future session deliberately replaces a confirmed-stuck process.
