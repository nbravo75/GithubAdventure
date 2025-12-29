# Changelog

## v0.1.0 (2025-12-28)

Initial release of keyring fallback utilities.

- Detection: `detect_keyring.py` to inspect Python keyring backend and macOS `security` CLI.
- Fallbacks: `env_fallback.py` preferring environment secrets; guidance for `PYTHON_KEYRING_BACKEND`.
- Wrapper: `secret_store.py` exposing `get_secret`/`set_secret` with encrypted-file backend support.
- Demos: `wrapper_demo.py` (set/get using wrapper) and `keychain_demo.sh` (macOS Keychain CLI).
- Dependencies: `requirements.txt` including `keyring`, `keyrings.alt`, `pycryptodome`, `pytest`.
- CI: GitHub Actions workflow `.github/workflows/ci.yml` running tests on push/PR to `main`.
- Tests: `tests/test_secret_store.py` covering env precedence and encrypted backend set/get.
