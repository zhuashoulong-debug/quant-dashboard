# B Sell v13 Handoff Summary - 20260511-053439

## Current Mainline

B dialogue is studying the formal sell / prewarning / reduce-position formula for trend stocks. It is independent from A dialogue's buy/yellow-permission line.

## Latest Confirmed Points

- [已确认] B3 validation subchart loaded the new version: `版本线:0.200` appeared in Eastmoney.
- [已确认] B3 variable mismatch was fixed. `300749` now shows `天败 / 强滞 / 强败 / 压` in the funds/confirmation layer.
- [暂不改待验证] `300749` is treated as a top acceleration failure sample where the risk segment can be identified. Do not tighten the main formula just from this single dense case.
- [已确认] B GitHub mobile sync must use `github-mobile-sync/b-sell-v13/` and timestamped snapshots. Do not mix with A dialogue or overwrite old packages.
- [已确认] Missing tools/environment should be handled by `缺什么补什么`, prioritizing quality and efficiency.

## Continue From Here

1. Keep using `B卖点验证3：资金失衡与确认层`.
2. Observe `300502 / 600590 / 600537` in Eastmoney.
3. Decide whether B3 signal density is reasonable or too noisy.
4. If a signal is questionable, diagnose source variables before changing the main formula.

## Important Boundary

Do not resume A dialogue from this package. This package is only for B sell v13.
