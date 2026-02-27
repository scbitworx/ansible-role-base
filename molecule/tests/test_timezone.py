"""Verify timezone configuration."""


def test_localtime_exists(host):
    """/etc/localtime must exist."""
    assert host.file("/etc/localtime").exists
