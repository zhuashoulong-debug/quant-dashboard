# New Chat Handoff - 2026-05-12

Copy the startup prompt below into the next conversation.

## Startup Prompt

```text
## 
缁х画鈥滃ぇA鏁版嵁婧?/ A鑲′簯绔洖娴嬪熀鍑嗏€濋」鐩€傝鍏堣鍙栨湰椤圭洰涓婁笅鏂囧拰瑙勫垯锛?
- 鏈湴椤圭洰鏍圭洰褰曪細C:\Users\Administrator\Documents\Codex\2026-05-11\new-chat-3\ashare_downloader_project
- 椤圭洰瑙勫垯锛欳:\Users\Administrator\Documents\Codex\2026-05-11\new-chat-3\AGENTS.md
- 浜戠鍩哄噯璇存槑锛欳:\Users\Administrator\Documents\Codex\2026-05-11\new-chat-3\ashare_downloader_project\docs\cloud-canonical-ashare-baseline.md
- 浜戠鍗歌浇宸ヤ綔娴侊細C:\Users\Administrator\Documents\Codex\2026-05-11\new-chat-3\ashare_downloader_project\docs\cloud-offload-workflow.md
- 鏈氦鎺ユ枃妗ｏ細C:\Users\Administrator\Documents\Codex\2026-05-11\new-chat-3\ashare_downloader_project\docs\new-chat-handoff-2026-05-12.md

浜戠涓绘満锛?5.32.63.104
榛樿鐢ㄦ埛锛歝odex
SSH key锛欳:\Users\Administrator\Documents\Codex\cloud-keys\a3b2-vultr-rsa
浜戠椤圭洰锛?opt/projects/ashare_downloader_project/current
浜戠鍏变韩鈥滃ぇA鏁版嵁婧愨€漵kill锛?opt/projects/_shared/codex-skills/daa-data-source-current
浜戠 qfq 鍓嶅鏉?canonical 鏁版嵁鏍圭洰褰曪細/data/ashare/canonical

閲嶈纭鍒欙細

- 浜戠 A鑲″洖娴嬨€佸叕寮忛獙璇併€佸€欓€夌瓫閫夈€佹牱鏈鐩橀粯璁や娇鐢?/data/ashare/canonical銆?- 榛樿浠锋牸鍙ｅ緞鏄?qfq 鍓嶅鏉冦€?- 涓嶈娣风敤 qfq 鍓嶅鏉冨拰 none 涓嶅鏉冩暟鎹€?- 涓嶈閲嶅鍚姩鍏ㄩ噺涓嬭浇锛涜ˉ鏁版嵁浼樺厛澶嶇敤鎴栨墿灞?/data/ashare/canonical銆?- 涓嶈鍋滄銆侀噸鍚垨鏀瑰姩 tmux session: ashare-qfq-full銆?- 涓嶈鏀瑰姩 /opt/a3b2/formula-project锛岄櫎闈炴垜鏄庣‘瑕佹眰銆?- 寮€濮嬮噸浠诲姟鍓嶅厛妫€鏌ワ細df -h /data銆乫ree -h銆乼mux ls銆?- 濡傞噰鐢ㄥ叡浜?skill 鐨勬柊寤鸿浼氭敼鍙樿矾寰勩€佸鏉冨彛寰勩€佽鐩栨暟鎹€侀噸寤虹绾挎垨鍋滄鍚庡彴浠诲姟锛屽繀椤诲厛闂垜纭銆?
璇峰厛鍙妫€鏌?cloud_status.ps1 鎴栦簯绔?tmux 鐘舵€侊紝鐒跺悗缁х画褰撳墠浠诲姟銆?```

## Current State

- 澶鏁版嵁婧愰」鐩凡鎼ソ鏈湴涓庝簯绔伐浣滄祦銆?- 浜戠浠ｇ爜鐩綍锛歚/opt/projects/ashare_downloader_project/current`
- 浜戠 canonical 鏁版嵁鐩綍锛歚/data/ashare/canonical`
- 浜戠鍏变韩 skill锛歚/opt/projects/_shared/codex-skills/daa-data-source-current`
- A3b2 椤圭洰鍙鍏ュ彛锛歚/opt/a3b2/formula-project`
- A3b2 瀹為檯蹇収锛歚/opt/a3b2/formula-project-20260512-055524`

## Canonical Data Paths

- Daily qfq: `/data/ashare/canonical/normalized/market_layer/full_kline_qfq/daily`
- Weekly qfq: `/data/ashare/canonical/normalized/market_layer/full_kline_qfq/weekly`
- Monthly qfq: `/data/ashare/canonical/normalized/market_layer/full_kline_qfq/monthly`
- Manifest: `/data/ashare/canonical/manifests/full_kline_manifest.json`

## Local Control Scripts

Run from:

```text
C:\Users\Administrator\Documents\Codex\2026-05-11\new-chat-3\ashare_downloader_project
```

Useful scripts:

- `cloud_status.ps1`
- `cloud_sync_code.ps1`
- `cloud_run_tests.ps1`
- `cloud_sync_daa_skill.ps1`
- `cloud_fetch_outputs.ps1`
- `cloud_start_full_kline_tmux.ps1`

## Running Jobs

Latest read-only check shows:

```text
tmux session: ashare-qfq-full
status: running
```

Do not stop it unless the user explicitly approves.

## Completed Work

- Built the six-layer A-share data-source project.
- Added iwencai cookie/pywencai path and structured outputs.
- Added theme/condition/pattern selection planning and structured theme combo query.
- Exported readable Excel for `浜哄舰鏈哄櫒浜?+ 涓濇潌`.
- Added cloud offload scripts and cloud status checks.
- Deleted local none/unadjusted full K-line dataset.
- Established cloud canonical qfq baseline at `/data/ashare/canonical`.
- Published safe shared `daa-data-source` skill to cloud with versioned releases.
- Restored A3b2 project path as read-only.

## Next Best Steps

1. Check `ashare-qfq-full` progress without stopping it.
2. Once qfq full download completes, verify daily/weekly/monthly counts and manifest failures.
3. Build a failed-symbol retry/repair workflow against `/data/ashare/canonical`.
4. Use canonical qfq data for A3b2 formula validation and any other A-share backtest.

## GitHub Sync

Dedicated GitHub handoff folder:

```text
zhuashoulong-debug/quant-dashboard
handoffs/ashare_downloader_project/2026-05-12-new-chat-3/
```

Recommended GitHub handoff files:

- `handoffs/ashare_downloader_project/2026-05-12-new-chat-3/README.md`
- `handoffs/ashare_downloader_project/2026-05-12-new-chat-3/manifest.json`
- `handoffs/ashare_downloader_project/2026-05-12-new-chat-3/new-chat-handoff-2026-05-12.md`

Keep this local handoff file and the GitHub copy in sync when the stage summary changes.
