"""Verify ansible-pull timer is disabled when base_pull_timer_enabled=false."""


def test_ansible_pull_service_unit_exists(host):
    """Service unit file must still be deployed."""
    f = host.file("/etc/systemd/system/ansible-pull.service")
    assert f.exists
    assert f.is_file


def test_ansible_pull_timer_unit_exists(host):
    """Timer unit file must still be deployed."""
    f = host.file("/etc/systemd/system/ansible-pull.timer")
    assert f.exists
    assert f.is_file


def test_ansible_pull_timer_not_enabled(host):
    """Timer must not be enabled when base_pull_timer_enabled=false."""
    svc = host.service("ansible-pull.timer")
    assert not svc.is_enabled
