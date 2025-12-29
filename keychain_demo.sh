#!/bin/bash
# Keychain demo: store and read a generic password using macOS `security` CLI.
# WARNING: running `store` will add an item to your Keychain.

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 store|read <service> <account> [secret]"
  exit 2
fi

cmd="$1"
service="$2"
account="$3"
secret="$4"

case "$cmd" in
  store)
    if [ -z "$account" ] || [ -z "$secret" ]; then
      echo "Usage: $0 store <service> <account> <secret>"
      exit 2
    fi
    security add-generic-password -a "$account" -s "$service" -w "$secret" -U
    echo "Stored secret for service='$service' account='$account'."
    ;;
  read)
    if [ -z "$account" ]; then
      echo "Usage: $0 read <service> <account>"
      exit 2
    fi
    security find-generic-password -s "$service" -a "$account" -w
    ;;
  *)
    echo "Unknown command: $cmd"
    echo "Usage: $0 store|read <service> <account> [secret]"
    exit 2
    ;;
esac
