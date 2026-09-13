# Changelog

All notable changes to `ha-glinet-router` are recorded here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.0] - 2026-09-13

### Changed
- Refactored the integration to depend on the standalone `glinet` PyPI
  package instead of the previously vendored
  `custom_components/glinet_router/api/` subpackage. The protocol layer is
  now `glinet[auth]==0.0.1` (the `[auth]` extra pulls in `passlib`) and
  all Home Assistant-specific code stays in this repository.
- The integration no longer imports `aiohttp` directly. `ClientError` is
  re-exported by `glinet` as `glinet.ClientError` and imported from there.
- Documentation: `docs/router-api.md` and `docs/modem-api.md` moved to
  the library repository (where the protocol layer now lives); added
  `docs/library.md` pointing at the new library docs and explaining when
  to edit the library versus the integration.

### Removed
- Vendored `custom_components/glinet_router/api/` directory and its
  contents (`client.py`, `const.py`, `exceptions.py`, `models.py`,
  `utils.py`, `modules/`). All of this now lives in the standalone
  `glinet` package.
- Library-specific tests moved to the library repository; only
  Home-Assistant-specific tests remain here.
- Stubbed `aiohttp` and `passlib` modules from `tests/conftest.py`
  (no longer needed — both are installed as real dependencies via the
  `glinet` package).

### Fixed
- **Session-table eviction spam.** `fetch_all_data()` no longer calls
  `refresh_session_token()` on every poll. The proactive refresh is now
  gated on `self.router_api.logged_in`, so a still-valid `sid` is reused
  across polls. This stops the router from logging
  `gl-ngx-session: session more than 5, clean the last inactive` once
  per `scan_interval` and, as a user-visible side effect, stops HA from
  evicting the browser session from the router's web UI. Reported by
  a Flint 3 (GL-BE9300) user on firmware `IPQ5332/AP-MI01.6`. Expired
  sessions are still recovered lazily through the existing reactive path
  in `_invoke_api()` (`_token_error` / `_connect_error` flags).

### Notes
- This is the first release published against the standalone library.
  From a user's perspective the structural split is invisible; the only
  behavioural change is the session-eviction fix above.

## [1.6.x] and earlier

See the git history for changes prior to the library split.
