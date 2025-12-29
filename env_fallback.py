#!/usr/bin/env python3
"""Simple secret getter: prefer environment variable, then platform keyring.

Usage:
  python3 env_fallback.py <service> <account>

Environment variable format checked: <SERVICE>_<ACCOUNT>_SECRET (uppercased)
"""
import os
import sys
from typing import Optional


def get_secret(service: str, account: str) -> Optional[str]:
    import re

    raw = f"{service.upper()}_{account.upper()}_SECRET"
    env_name = re.sub(r"[^A-Z0-9]", "_", raw)
    val = os.environ.get(env_name)
    if val:
        print(f"Using environment secret from {env_name}")
        return val

    try:
        import keyring

        val = keyring.get_password(service, account)
        if val:
            print("Using keyring backend")
            return val
    except Exception:
        pass

    return None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 env_fallback.py <service> <account>")
        sys.exit(2)
    service = sys.argv[1]
    account = sys.argv[2]
    secret = get_secret(service, account)
    if secret is None:
        print("No secret found")
        sys.exit(1)
    print(secret)
