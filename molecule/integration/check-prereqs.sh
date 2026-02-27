#!/bin/bash
# Check prerequisites for the Vagrant + libvirt integration scenario.
#
# Usage: molecule/integration/check-prereqs.sh
#
# Expects the Molecule toolchain in ~/.virtualenvs/molecule/.
# See README.md for setup instructions.

set -euo pipefail

VENV="$HOME/.virtualenvs/molecule"
PASS=0
FAIL=0

check() {
  local desc="$1"
  shift
  if "$@" &>/dev/null; then
    echo "  [OK]   ${desc}"
    PASS=$((PASS + 1))
  else
    echo "  [MISS] ${desc}"
    FAIL=$((FAIL + 1))
  fi
}

echo "--- Integration scenario prerequisites ---"

# System packages
check "vagrant is installed" command -v vagrant
check "libvirtd is running" systemctl is-active libvirtd

# Vagrant plugin
if vagrant plugin list 2>/dev/null | grep -q vagrant-libvirt; then
  echo "  [OK]   vagrant-libvirt plugin is installed"
  PASS=$((PASS + 1))
else
  echo "  [MISS] vagrant-libvirt plugin is installed"
  echo "         Install with: vagrant plugin install vagrant-libvirt"
  FAIL=$((FAIL + 1))
fi

# Molecule venv
check "molecule venv exists" test -x "${VENV}/bin/molecule"
check "pytest-testinfra is installed" "${VENV}/bin/python" -c "import testinfra"
check "molecule-plugins[vagrant] is installed" "${VENV}/bin/python" -c "import molecule_plugins.vagrant"

echo ""
if [ ${FAIL} -gt 0 ]; then
  echo "--- ${FAIL} missing prerequisite(s). See README.md for setup. ---"
  exit 1
else
  echo "--- All ${PASS} prerequisites satisfied. ---"
fi
