Keyring detection and fallback helper (macOS)

[![CI](https://github.com/nbravo75/GithubAdventure/actions/workflows/ci.yml/badge.svg)](https://github.com/nbravo75/GithubAdventure/actions/workflows/ci.yml)

Quick Start

1) Install deps

```bash
pip3 install --user -r requirements.txt
```

2) Detect available keyrings

```bash
python3 detect_keyring.py
```

3) Use env var fallback (no prompts)

```bash
export MY_SERVICE_MY_ACCOUNT_SECRET='demo-secret'
python3 wrapper_demo.py get my-service my-account
```

4) Store/read with encrypted-file backend

```bash
# store (first time will create an encrypted keyring file and may prompt)
python3 wrapper_demo.py set my-service my-account 'demo-secret'

# read
python3 wrapper_demo.py get my-service my-account
```

5) Use in your code

```py
from secret_store import get_secret, set_secret, ensure_encrypted_backend

ensure_encrypted_backend()  # optional: enforce encrypted file backend
set_secret('my-service', 'my-account', 's3cr3t')
print(get_secret('my-service', 'my-account'))
```

Files:
- detect_keyring.py: Detects the active Python `keyring` backend and shows fallback options.
- requirements.txt: Python dependencies (`keyring`, `keyrings.alt`).

Quick start:

1) Install dependencies (user-level):

```bash
pip3 install --user -r requirements.txt
```

2) Run the detector:

```bash
python3 detect_keyring.py
```

If your app cannot access the macOS Keychain, either:
- Configure your app to use an encrypted file backend (Python example):

```bash
export PYTHON_KEYRING_BACKEND=keyrings.alt.file.EncryptedKeyring
```

- Or store secrets in your CI/CD secrets manager or environment variables for headless runs.

macOS manual fallback (CLI):

```bash
# store
security add-generic-password -a my-account -s my-service -w 'my-secret' -U
# read
security find-generic-password -s my-service -w
```

Security note: Keep encryption passphrases and secret files protected and out of source control.
