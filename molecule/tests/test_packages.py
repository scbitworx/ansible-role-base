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


def test_distro_build_package(host):
    """Distro-specific build meta-package must be installed."""
    distro = host.system_info.distribution
    if distro in ("arch", "archlinux"):
        pkg = host.package("base-devel")
    else:
        pkg = host.package("build-essential")
    assert pkg.is_installed
