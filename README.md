Keyring detection and fallback helper (macOS)

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
