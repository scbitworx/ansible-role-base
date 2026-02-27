#!/bin/bash
# Run the Vagrant integration scenario with the Molecule venv.
#
# Activates the venv and exports MOLECULE_VAGRANT_PLUGIN_DIR for
# molecule.yml to reference (workaround for molecule 25.2.0+ regression).
#
# Usage:
#   molecule/integration/run.sh test          # full test
#   molecule/integration/run.sh converge      # converge only
#   molecule/integration/run.sh verify        # verify only
#   molecule/integration/run.sh destroy       # destroy VM
#
# See: https://github.com/ansible-community/molecule-plugins/issues/301

set -euo pipefail

VENV="$HOME/.virtualenvs/molecule"

if [ ! -f "${VENV}/bin/activate" ]; then
  echo "ERROR: Molecule venv not found at ${VENV}"
  echo "       See README.md for setup instructions."
  exit 1
fi

# shellcheck source=/dev/null
source "${VENV}/bin/activate"

# Workaround: molecule 25.2.0+ no longer wires driver module paths into
# ANSIBLE_LIBRARY. Export for molecule.yml config_options.defaults.library.
export MOLECULE_VAGRANT_PLUGIN_DIR
MOLECULE_VAGRANT_PLUGIN_DIR="$(python3 -c \
  'import molecule_plugins.vagrant, os; print(os.path.dirname(molecule_plugins.vagrant.__file__))' \
  2>/dev/null || true)"

# Workaround: Docker's nftables FORWARD chain (policy drop) blocks virbr0
# traffic, preventing VMs from reaching the internet. Ensure forwarding
# rules exist for the libvirt default network bridge.
if command -v nft &>/dev/null; then
  if ! sudo nft list chain ip filter FORWARD 2>/dev/null | grep -q 'iif "virbr0" accept'; then
    echo "Adding nftables FORWARD rules for virbr0..."
    sudo nft insert rule ip filter FORWARD iif virbr0 accept
    sudo nft insert rule ip filter FORWARD oif virbr0 ct state established,related accept
  fi
fi

ACTION="${1:?Usage: run.sh <test|converge|verify|destroy>}"
shift

exec molecule "${ACTION}" -s integration "$@"
