import os
import tempfile

import keyring

from secret_store import get_secret, set_secret


def test_env_var_precedence():
    service = "my-service"
    account = "my-account"
    env_name = f"{service.upper()}_{account.upper()}_SECRET".replace("-", "_")
    os.environ[env_name] = "env-secret"
    try:
        val = get_secret(service, account)
        assert val == "env-secret"
    finally:
        os.environ.pop(env_name, None)


def test_encrypted_backend_set_get():
    service = "ci-service"
    account = "ci-account"
    secret = "ci-topsecret"

    # Use EncryptedKeyring with a programmatic passphrase and temp file path
    from keyrings.alt.file import EncryptedKeyring

    kr = EncryptedKeyring()
    kr.keyring_key = "test-passphrase"
    fd, path = tempfile.mkstemp(prefix="test_keyring_", suffix=".cfg")
    os.close(fd)
    try:
        kr.file_path = path
        keyring.set_keyring(kr)
        ok = set_secret(service, account, secret, force_encrypted=False)
        assert ok is True
        val = get_secret(service, account, use_env=False)
        assert val == secret
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
