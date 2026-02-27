"""Verify timezone and locale configuration."""


def test_localtime_exists(host):
    """/etc/localtime must exist."""
    assert host.file("/etc/localtime").exists


def test_locale_conf(host):
    """/etc/locale.conf must set LANG."""
    f = host.file("/etc/locale.conf")
    assert f.exists
    assert f.contains("LANG=en_US.UTF-8")
