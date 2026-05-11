# A3b2 Exit Handoff

## Restore Identity

This handoff belongs to the A conversation buy-point formula project. It is not the B conversation sell/reduce-position formula project.

Current mainline:

```text
A3b2 黄许可 / 黄后重置 / 再缩+时重风险保护验证
```

Hard boundaries:

- Current main formula is not changed.
- Exit and new-chat handoff must not stop downloads.
- Download status is only inspected and recorded.

## Current A3b2 Conclusion

The current A3b2 discussion has moved away from "whether the time threshold is too loose" and toward "whether the recontraction quality is strong enough to support a new release".

Bad samples should currently be interpreted first through:

- `假收缩`
- `趋势已弱`
- `环境扰动`

Current status:

- This content is only a reading rule and candidate observation layer.
- It is not upgraded into a new field.
- It is not written back into the main formula.

## Validation Subchart Structure

`A3b2b1`:

- Main diagnostic layer.
- Only reads the signal-day breakout background.

`A3b2c`:

- Yellow-after-reset explanation layer.
- On the signal day, first read `黄源 / 黄效 / 黄重 / 缩态`.
- Then look back for the latest release source: `回落 / 再缩 / 时重`.
- Representative samples:
  - `000019 2023-08-07` = `回落`
  - `000025 2015-10-20` = `时重`
  - `000037 2015-11-11` = `再缩`

`A3b2d`:

- Strong-after-reset history layer.
- Do not require it to light on the signal day.
- Only look back for the latest pre-signal strong-after release source.
- Representative samples:
  - `000019 2023-08-07` = latest strong-after release source is `再缩`
  - `000037 2015-11-11` = latest strong-after release source is `再缩`
  - `000025 2015-10-20` = no recent pre-signal strong-after release event found

`风险保护 / 市场环境`:

- Last overlay only.
- It must not replace structure-layer judgment.
- `热追` is the first strong prompt.
- `极弱续高` is the second risk image, currently only cross-read through risk protection and market environment.

## Current Closed-Loop Decision

- `A3b2c` and `A3b2d` do not compete for position.
- Validation subchart structure is closed for now.
- Follow-up work is expanded sample review, display micro-adjustment, and explanation compression.
- No new field, no new subchart, and no main formula change for now.

## Download Status Snapshot

Snapshot time: `2026-05-11 14:54 +08:00`

- Active downloader process exists.
- Command includes `--resume-from-manifest --per-stock-timeout 90`.
- Manifest has resumed into a `1310`-item remaining batch.
- Latest confirmed manifest tail around snapshot: `index=55 / total=1310`, `code=603599`, `status=downloaded`.
- CSV count around snapshot: about `4263`.
- Latest CSV around snapshot: `603599_20100101_20260509.csv`.

Logs:

- `D:\我的文档\Documents\New project 3\logs\download-market-data-resume-20260511-143430.out.log`
- `D:\我的文档\Documents\New project 3\logs\download-market-data-resume-20260511-143430.err.log`

Do not stop this process during exit or new-chat handoff. On resume, inspect only.

## Verified Tests

Passed earlier in this session:

- `.venv-py314\Scripts\python.exe -m unittest tests.test_download_market_data -v`
- `.venv-py314\Scripts\python.exe -m unittest tests.test_a3b2b1_backgrounds tests.test_validation_views -v`

## Next Best Step

Resume by doing a quick download-progress check, then continue expanded sample review using the current A3b2 validation-subchart reading order:

```text
A3b2b1 -> A3b2c -> A3b2d -> 风险保护 / 市场环境
```

Do not open a new structural branch unless repeated samples expose a clean, non-overfit missing category.
