#!/usr/bin/env python3
"""Simple secret store wrapper: prefer env var, then keyring, with optional encrypted-file fallback.

Functions:
- get_secret(service, account): returns secret or None
- set_secret(service, account, secret, force_encrypted=False): store secret
- ensure_encrypted_backend(): switch keyring backend to keyrings.alt.file.EncryptedKeyring

This module keeps the API minimal so apps can import and use it.
"""
import os
import re
from typing import Optional


def _env_name(service: str, account: str) -> str:
    raw = f"{service.upper()}_{account.upper()}_SECRET"
    return re.sub(r"[^A-Z0-9]", "_", raw)


def get_secret(service: str, account: str, use_env: bool = True) -> Optional[str]:
    """Get a secret: environment variable first (if enabled), then keyring backend.

    Returns the secret string or None.
    """
    if use_env:
        name = _env_name(service, account)
        val = os.environ.get(name)
        if val:
            # caller may rely on detection string
            print(f"Using environment secret from {name}")
            return val

    try:
        import keyring

        val = keyring.get_password(service, account)
        if val:
            print("Using keyring backend")
            return val
    except Exception:
        # keyring not installed or error happened
        pass

    return None


def ensure_encrypted_backend() -> bool:
    """Attempt to set the keyring backend to EncryptedKeyring from keyrings.alt.

    Returns True if successful, False otherwise.
    """
    try:
        import keyring
        from keyrings.alt.file import EncryptedKeyring

        keyring.set_keyring(EncryptedKeyring())
        return True
    except Exception:
        return False


def set_secret(service: str, account: str, secret: str, force_encrypted: bool = False) -> bool:
    """Store a secret via the configured keyring backend.

    If `force_encrypted` is True, attempt to switch to the encrypted-file backend.
    Returns True on success, False on failure.
    """
    try:
        import keyring
    except Exception:
        return False

    if force_encrypted:
        ok = ensure_encrypted_backend()
        if not ok:
            return False

    try:
        keyring.set_password(service, account, secret)
        return True
    except Exception:
        return False


__all__ = ["get_secret", "set_secret", "ensure_encrypted_backend"]
