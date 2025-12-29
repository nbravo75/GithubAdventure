Secret store wrapper and demo

Files added:
- secret_store.py: `get_secret(service, account)`, `set_secret(service, account, secret)`, `ensure_encrypted_backend()`
- wrapper_demo.py: CLI demo to `set`/`get` secrets. `set` enables the encrypted-file backend before storing.

Usage examples:

1) Use environment variable fallback (no packages required):

```bash
export MY_SERVICE_MY_ACCOUNT_SECRET='demo-secret'
python3 wrapper_demo.py get my-service my-account
```

2) Store and read with encrypted-file backend (interactive passphrase prompt):

```bash
# set: will prompt to create an encryption passphrase
python3 wrapper_demo.py set my-service my-account 'demo-secret'
# get:
python3 wrapper_demo.py get my-service my-account
```

Notes:
- For headless/CI usage prefer injecting secrets through your CI provider's secret store and read via env vars.
- The encrypted-file backend will prompt for a passphrase on first use; store that passphrase securely.
