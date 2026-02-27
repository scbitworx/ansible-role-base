"""Verify timezone and locale configuration."""


def test_localtime_is_symlink(host):
    """/etc/localtime must be a symlink to the correct timezone."""
    f = host.file("/etc/localtime")
    assert f.exists
    assert f.is_symlink
    assert f.linked_to == "/usr/share/zoneinfo/America/New_York"


def test_locale_conf(host):
    """/etc/locale.conf must set LANG."""
    f = host.file("/etc/locale.conf")
    assert f.exists
    assert f.contains("LANG=en_US.UTF-8")
