# B Sell v13 Mobile Sync

This is the dedicated GitHub sync namespace for the B dialogue sell/prewarning/reduce formula line.

## Scope

- Current mainline: B sell v13 formula, validation subcharts, manual observation notes, and handoff material.
- Do not place A dialogue buy/yellow-permission work here.
- Do not place unrelated chat handoffs here.

## No-Overwrite Rule

Every desktop handoff must use:

```text
github-mobile-sync/b-sell-v13/handoffs/YYYYMMDD-HHMMSS/
```

Every phone-side update must use:

```text
github-mobile-sync/b-sell-v13/mobile-updates/YYYYMMDD-HHMMSS/
```

Do not overwrite old package folders. If an index points to the latest package, update the index only; keep historical snapshots intact.

## Required Manifest

Each package must include `manifest.md` with:

- source: desktop or phone
- task/mainline: B sell v13
- branch/ref
- included files
- next action
- files that are reference-only and must not overwrite local work
