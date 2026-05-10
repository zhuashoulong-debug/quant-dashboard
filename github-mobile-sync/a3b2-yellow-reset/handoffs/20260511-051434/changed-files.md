# Changed Files Summary

## Important Logic Changes

```text
formula_lab/a3b2b1.py
formula_lab/local_server.py
formula_lab/validation_views.py
formula_lab/data_service.py
```

Summary:

- Added time-ordered yellow reset context fields.
- Added `yellow_reset_heat_chase_watch` validation-only observation.
- Added `风险保护` validation view.
- Fixed local lab JSON output for non-finite numbers.
- Added cache-covering reuse for short date requests.

## Tests

```text
tests/test_a3b2b1_backgrounds.py
tests/test_validation_views.py
tests/test_local_server_market_environment.py
tests/test_data_service.py
```

Latest checks:

```text
python -m unittest tests.test_data_service tests.test_download_market_data tests.test_local_server_market_environment tests.test_market_environment tests.test_validation_views
```

Result:

```text
18 tests OK
```

Earlier risk-protection checks:

```text
22 tests OK
```

## Documentation And Rules

```text
collaboration-guidelines.md
long-term-anchors.md
current-checkpoint.md
next-session-resume.md
yellow-reset-risk-protection-candidate-note.md
github-mobile-sync/
```

Notes:

- `退出` 和 `新建会话` 都不能停止下载进程。
- GitHub 同步包必须独立命名，不能覆盖，不能混用 A/B 对话主线。
- `new-chat-handoff.md` 是混合编码历史文件，只参考最新追加段落。