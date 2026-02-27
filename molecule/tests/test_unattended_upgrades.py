"""Verify unattended-upgrades configuration (Debian/Ubuntu only)."""

import pytest


def _skip_unless_debian(host):
    """Skip test if not running on Debian/Ubuntu."""
    if host.system_info.distribution not in ("ubuntu", "debian"):
        pytest.skip("Unattended-upgrades only applies to Debian/Ubuntu")


def test_unattended_upgrades_installed(host):
    """unattended-upgrades package must be installed."""
    _skip_unless_debian(host)
    result = host.run("dpkg -l unattended-upgrades")
    assert result.rc == 0


def test_50unattended_upgrades_config_exists(host):
    """50unattended-upgrades config file must exist."""
    _skip_unless_debian(host)
    f = host.file("/etc/apt/apt.conf.d/50unattended-upgrades")
    assert f.exists


def test_50unattended_upgrades_content(host):
    """Config must contain security origins and disable auto-reboot."""
    _skip_unless_debian(host)
    f = host.file("/etc/apt/apt.conf.d/50unattended-upgrades")
    assert f.contains("security")
    assert f.contains('Automatic-Reboot "false"')


def test_20auto_upgrades_config_exists(host):
    """20auto-upgrades config file must exist."""
    _skip_unless_debian(host)
    f = host.file("/etc/apt/apt.conf.d/20auto-upgrades")
    assert f.exists
