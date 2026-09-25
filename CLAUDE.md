# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install test dependencies
pip install -r requirements_test.txt

# Lint
ruff check .

# Format check
ruff format --check .

# Auto-fix lint + format
ruff check --fix . && ruff format .

# Run tests
pytest

# Run a single test file
pytest tests/test_coordinator.py

# Run a single test by name
pytest tests/test_coordinator.py::test_update_data
```

## Architecture

This is a **Home Assistant custom integration** (`custom_components/duolingo`) that polls the Duolingo API every 20 minutes and exposes sensors for streak and XP.

### Data flow

1. **`config_flow.py`** — UI-only setup; validates a username by calling `DuolingoApi.get_user_identifiers()`, stores `UserIdentifiersDto` (id, name, username) in the config entry.
2. **`coordinator.py`** — `DuolingoDataUpdateCoordinator` inherits `DataUpdateCoordinator`; polls `DuolingoApi.get_user_data()` every 20 min; holds the live `UserDto`.
3. **`entity.py`** — `DuolingoEntity` base; all sensors inherit from it. Translation keys follow `component.duolingo.common.sensors.<alias>` and `component.duolingo.common.courses.<key>`.
4. **`sensor.py` / `binary_sensor.py`** — Concrete entities reading from `coordinator.user`.

### HTTP client note

`api.py` uses the synchronous `requests` library. All API calls **must** be dispatched via `hass.async_add_executor_job()` to avoid blocking the HA event loop — never call them directly from an async context.

### Key types

| Type | File | Role |
|---|---|---|
| `UserDto` | `dto.py` | Full user snapshot returned by the API |
| `UserIdentifiersDto` | `dto.py` | Minimal identity info stored in config entry |
| `DuolingoApi` | `api.py` | Thin HTTP wrapper; `BASE_URL = "https://www.duolingo.com/2017-06-30"` |

### Platforms

`PLATFORMS = ["binary_sensor", "sensor"]` — defined in `const.py`. Add new platforms there and register them in `__init__.py`.

### Translations

Sensor display names come from `translations/en.json` (and `uk.json`). Add new keys under `common.sensors` or `common.courses` in both files when adding sensors.
