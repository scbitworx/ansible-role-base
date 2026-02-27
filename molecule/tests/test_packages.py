"""Verify base packages are installed."""

import pytest


@pytest.mark.parametrize(
    "binary",
    [
        "/usr/bin/git",
        "/usr/bin/vim",
        "/usr/bin/curl",
    ],
)
def test_base_package_binary_exists(host, binary):
    """Each base package binary must be present."""
    assert host.file(binary).exists
