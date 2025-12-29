#!/usr/bin/env python3
"""Detect available keyring backends on macOS and show fallback instructions.

Usage: python3 detect_keyring.py
"""
import platform
import shutil
import sys

print("Platform:", platform.system(), platform.release())
if platform.system() == "Darwin":
    try:
        import subprocess

        out = subprocess.check_output(["sw_vers"], text=True)
        print(out.strip())
    except Exception:
        pass

try:
    import keyring

    kr = keyring.get_keyring()
    print("\nDetected keyring backend:")
    print("  repr:", repr(kr))
    print("  type:", type(kr))
except Exception as e:
    print("\nkeyring import failed:", e)
    print("Install dependencies with: pip3 install --user -r requirements.txt")
    sys.exit(0)

# Check if it looks like the macOS Keychain backend
kr_name = type(kr).__name__
kr_module = type(kr).__module__
print("\nBackend class:", kr_name)
print("Backend module:", kr_module)

is_mac_keychain = (
    "OSX" in kr_name
    or "Keychain" in kr_name
    or "macOS" in kr_name
    or "keychain" in kr_module.lower()
)
print("\nIs macOS Keychain detected?", is_mac_keychain)

# Check for encrypted file fallback availability
try:
    from keyrings.alt.file import EncryptedKeyring

    print("\nEncrypted file backend available: keyrings.alt.file.EncryptedKeyring")
    print("To force this backend for this process:")
    print("  export PYTHON_KEYRING_BACKEND=keyrings.alt.file.EncryptedKeyring")
    print("\nNotes:")
    print(" - On first use the EncryptedKeyring will prompt for a passphrase to encrypt the file.")
    print(
        " - For CI or headless usage consider using your platform secret store or CI secret variables."
    )
except Exception:
    print("\nEncrypted file backend (keyrings.alt) not available. Install with:")
    print("  pip3 install --user keyrings.alt")

# Check macOS `security` CLI presence for manual fallback
security_path = shutil.which("security")
print("\nmacOS `security` CLI:", "found at " + security_path if security_path else "not found")
if security_path:
    print(
        "Example: store a generic password:\n  security add-generic-password -a my-account -s my-service -w 'my-secret' -U\nRetrieve it:\n  security find-generic-password -s my-service -w"
    )

print("\nIf an application cannot detect a keyring:")
print(
    " - For Python apps: install `keyring` and optionally `keyrings.alt`, or set `PYTHON_KEYRING_BACKEND` to an encrypted file backend."
)
print(
    " - For Node/Electron: ensure `keytar` is installed and the process has access to Keychain; otherwise use environment secrets or an encrypted file vault."
)
