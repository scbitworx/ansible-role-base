"""Verify ansible-pull systemd timer and service."""

import pytest


def test_ansible_pull_service_unit_exists(host):
    """Service unit file must exist with mode 0644."""
    f = host.file("/etc/systemd/system/ansible-pull.service")
    assert f.exists
    assert oct(f.mode) == "0o644"


def test_ansible_pull_timer_unit_exists(host):
    """Timer unit file must exist with mode 0644."""
    f = host.file("/etc/systemd/system/ansible-pull.timer")
    assert f.exists
    assert oct(f.mode) == "0o644"


def test_ansible_pull_service_content(host):
    """Service unit must reference ansible-pull-wrapper and be oneshot."""
    f = host.file("/etc/systemd/system/ansible-pull.service")
    assert f.contains("/usr/local/bin/ansible-pull-wrapper")
    assert f.contains("Type=oneshot")


def test_ansible_pull_timer_content(host):
    """Timer unit must contain expected interval and persistence settings."""
    f = host.file("/etc/systemd/system/ansible-pull.timer")
    assert f.contains("OnUnitActiveSec=4h")
    assert f.contains("Persistent=true")
    assert f.contains("timers.target")


def test_ansible_pull_timer_enabled(host):
    """ansible-pull.timer must be enabled."""
    result = host.run("systemctl is-enabled ansible-pull.timer")
    assert result.stdout.strip() == "enabled"


@pytest.mark.vm_only
def test_ansible_pull_timer_running(host):
    """ansible-pull.timer must be actively running (VM only)."""
    svc = host.service("ansible-pull.timer")
    assert svc.is_running
