#!/usr/bin/env python3
"""Demo for `secret_store` wrapper.

Usage:
  python3 wrapper_demo.py set <service> <account> <secret>
  python3 wrapper_demo.py get <service> <account>

The `set` command will force the encrypted-file backend so you can test on disk.
"""
import sys

from secret_store import ensure_encrypted_backend, get_secret, set_secret


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "set":
        if len(argv) != 5:
            print("Usage: wrapper_demo.py set <service> <account> <secret>")
            return 2
        service, account, secret = argv[2], argv[3], argv[4]
        ok = ensure_encrypted_backend()
        if not ok:
            print("Failed to enable encrypted backend; aborting")
            return 1
        if set_secret(service, account, secret, force_encrypted=False):
            print("Secret stored")
            return 0
        else:
            print("Failed to store secret")
            return 1

    if cmd == "get":
        if len(argv) != 4:
            print("Usage: wrapper_demo.py get <service> <account>")
            return 2
        service, account = argv[2], argv[3]
        val = get_secret(service, account)
        if val is None:
            print("No secret found")
            return 1
        print(val)
        return 0

    print("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
